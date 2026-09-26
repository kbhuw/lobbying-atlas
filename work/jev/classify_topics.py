"""JEV topic classification of distinct activity descriptions.

Usage: python3 classify_topics.py <filings.sqlite> <topics.json> <out.sqlite> [workers]
Resumable: out.sqlite's `desc_topics` table checkpoints every batch; re-run to continue.
Each worker owns its own jev-mcp server subprocess (AI_GATEWAY_API_KEY must be set).
"""
import json, os, queue, select, sqlite3, subprocess, sys, threading

JEV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'node_modules/@jkudish/jev-mcp/dist/index.js')
BATCH = 32
PURPOSE = ("Label each lobbying-filing issue description with the single policy "
           "topic it is about. Descriptions come verbatim from LDA filings.")


class JevWorker(threading.Thread):
    def __init__(self, wid, jobs, results):
        super().__init__(daemon=True)
        self.wid, self.jobs, self.results = wid, jobs, results
        self.seq = 0
        self.p = None

    def start_proc(self):
        if self.p:
            self.p.terminate()
        self.p = subprocess.Popen(['node', JEV], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                  text=True, bufsize=1)
        self.request('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {},
                                    'clientInfo': {'name': 'lobbying-atlas', 'version': '1'}})
        self.p.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n')
        self.p.stdin.flush()

    def request(self, method, params):
        self.seq += 1
        self.p.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': self.seq,
                                       'method': method, 'params': params}) + '\n')
        self.p.stdin.flush()
        while True:
            if not select.select([self.p.stdout], [], [], 300)[0]:
                raise TimeoutError(method)
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError('jev server ended')
            r = json.loads(line)
            if r.get('id') == self.seq:
                if 'error' in r:
                    raise RuntimeError(r['error'])
                return r['result']

    def run(self):
        self.start_proc()
        while True:
            try:
                batch = self.jobs.get(timeout=3)
            except queue.Empty:
                break
            if batch is None:
                break
            items, descs = batch
            try:
                res = self.request('tools/call', {'name': 'jev_classify', 'arguments': {
                    'items': items, 'classes': CLASSES, 'purpose': PURPOSE}})
                text = res['content'][0]['text']
                data = json.loads(text)
                byid = {str(r.get('id')): r for r in data.get('results', [])}
                self.results.put(('ok', [
                    (descs[int(rid)] if int(rid) < len(descs) else None,
                     r.get('classification'), r.get('top_probability'),
                     r.get('margin'), r.get('confidence'), r.get('decision'))
                    for rid, r in byid.items()]))
            except Exception as e:
                self.results.put(('err', (items, descs, repr(e))))
        self.p.terminate()


def main():
    db_path, topics_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    global CLASSES
    CLASSES = json.load(open(topics_path))

    src = sqlite3.connect(db_path)
    out = sqlite3.connect(out_path)
    out.execute('''CREATE TABLE IF NOT EXISTS desc_topics(
        description TEXT PRIMARY KEY, topic TEXT, top_p REAL,
        margin REAL, confidence REAL, decision TEXT)''')
    out.commit()

    done = {r[0] for r in out.execute('select description from desc_topics')}
    todo = [d for (d,) in src.execute(
        'select distinct description from activities where description is not null')
        if d and d not in done]
    print(f'distinct: {len(done)+len(todo)}, done: {len(done)}, todo: {len(todo)}', flush=True)

    jobs, results = queue.Queue(), queue.Queue()
    batches = []
    for i in range(0, len(todo), BATCH):
        descs = todo[i:i + BATCH]
        items = [{'id': str(j), 'text': t[:1800]} for j, t in enumerate(descs)]
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
            rows = [(d, t, p, m, c, dec) for d, t, p, m, c, dec in payload if d]
            out.executemany(
                'insert or replace into desc_topics values(?,?,?,?,?,?)', rows)
            out.commit()
        else:
            items, descs, err = payload
            n_err += 1
            print(f'ERR batch: {err} — requeuing {len(descs)}', flush=True)
            # requeue with fresh ids
            jobs.put((items, descs))
            if n_err > len(batches) // 10 + 20:
                print('too many errors, stopping', flush=True)
                break
            continue
        n_done += 1
        if n_done % 50 == 0:
            print(f'{n_done}/{len(batches)} batches ({n_done*BATCH} items)', flush=True)

    for w in ws:
        w.join(timeout=5)
    print(f'DONE classified={out.execute("select count(*) from desc_topics").fetchone()[0]}',
          flush=True)


if __name__ == '__main__':
    main()
