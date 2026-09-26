"""JEV classification of covered_position strings into seniority buckets.

Usage: python3 classify_positions.py <filings.sqlite> <out.sqlite> [workers]
Resumable via out.sqlite `positions` table. AI_GATEWAY_API_KEY must be set.
"""
import json, os, queue, select, sqlite3, subprocess, sys, threading

JEV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'node_modules/@jkudish/jev-mcp/dist/index.js')
BATCH = 32
PURPOSE = ("Each item is the former government position a registered lobbyist "
           "disclosed on a US federal lobbying filing ('covered position'). "
           "Classify the MOST SENIOR role listed into one bucket.")

CLASSES = [
    {'id': 'member_of_congress',
     'description': 'Former U.S. Senator or U.S. Representative — the person served as an elected Member of Congress.'},
    {'id': 'congressional_leadership',
     'description': 'Senior aide to congressional leadership or a committee: chief of staff, staff director, counsel, parliamentarian, or other senior role for House/Senate leadership or a committee.'},
    {'id': 'executive_branch',
     'description': 'White House or executive-branch official: White House, Executive Office of the President, cabinet/department political staff.'},
    {'id': 'agency',
     'description': 'Federal agency or regulator staff: career or policy staff at a federal agency, regulator, or independent board.'},
    {'id': 'congressional_staff',
     'description': 'Other congressional staffer: House/Senate member-office staff such as legislative director/assistant, press, counsel not tied to leadership.'},
    {'id': 'military',
     'description': 'Military officer or senior DoD civilian.'},
    {'id': 'other_gov',
     'description': 'Other government role: courts, state/local government, or other public role.'},
    {'id': 'unclear',
     'description': 'Unclear or not a real government role: vague text, N/A, or not an actual government position.'},
]

# reuse the worker shape from classify_topics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify_topics import JevWorker  # noqa: E402


def main():
    db_path, out_path = sys.argv[1], sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    import classify_topics
    classify_topics.CLASSES = CLASSES
    classify_topics.PURPOSE = PURPOSE

    src = sqlite3.connect(db_path)
    out = sqlite3.connect(out_path)
    out.execute('''CREATE TABLE IF NOT EXISTS positions(
        position TEXT PRIMARY KEY, bucket TEXT, top_p REAL,
        margin REAL, confidence REAL, decision TEXT)''')
    out.commit()

    done = {r[0] for r in out.execute('select position from positions')}
    todo = [d for (d,) in src.execute(
        "select distinct covered_position from lobbyists "
        "where covered_position is not null and covered_position != '' "
        "and covered_position not in ('N/A','n/a','NA')")
        if d and d not in done]
    print(f'distinct positions: {len(done)+len(todo)}, todo: {len(todo)}', flush=True)

    jobs, results = queue.Queue(), queue.Queue()
    batches = []
    for i in range(0, len(todo), BATCH):
        descs = todo[i:i + BATCH]
        items = [{'id': str(j), 'text': t[:1200]} for j, t in enumerate(descs)]
        batches.append((items, descs))
    for b in batches:
        jobs.put(b)
    for _ in range(workers):
        jobs.put(None)

    ws = [JevWorker(i, jobs, results) for i in range(workers)]
    for w in ws:
        w.start()

    n_done, n_err = 0, 0
    while n_done + n_err < len(batches):
        status, payload = results.get()
        if status == 'ok':
            rows = [(d_, t, p_, m, c, dec) for d_, t, p_, m, c, dec in payload if d_]
            out.executemany(
                'insert or replace into positions values(?,?,?,?,?,?)', rows)
            out.commit()
        else:
            items, descs, err = payload
            n_err += 1
            print(f'ERR batch: {err} — requeuing {len(descs)}', flush=True)
            jobs.put((items, descs))
            if n_err > len(batches) // 10 + 20:
                break
            continue
        n_done += 1
        if n_done % 25 == 0:
            print(f'{n_done}/{len(batches)} batches', flush=True)

    for w in ws:
        w.join(timeout=5)
    print('DONE', out.execute('select count(*) from positions').fetchone()[0])


if __name__ == '__main__':
    main()
