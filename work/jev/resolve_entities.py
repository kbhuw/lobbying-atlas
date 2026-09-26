"""Resolve unmatched filing client names to directory groups using JEV jev_find.

Step 1: token-overlap shortlist of candidate directory names per unmatched client.
Step 2: jev_find picks the same entity (or 'absent').
Output: entity-map-jev.json {norm_name: {name, group_id, match: 'jev', confidence}}
Only writes matches where exists_verdict is 'answered'/'partial' with top prob >= 0.6.
"""
import gzip, json, re, sys, unicodedata, collections

sys.path.insert(0, 'lobbying-map/scripts/data')
from build_lobbying_index import norm  # noqa: E402

STOP = {'THE', 'INC', 'LLC', 'CORP', 'CORPORATION', 'COMPANY', 'CO', 'LTD', 'LP',
        'LLP', 'AND', 'OF', 'USA', 'US', 'U S', 'DBA', 'FKA', 'AKA', 'FORMERLY',
        'HOLDINGS', 'GROUP', 'INTERNATIONAL', 'AMERICAN', 'NATIONAL', 'SERVICES',
        'SYSTEMS', 'INCORPORATED', 'ASSOCIATION', 'ASSOC', 'UNIVERSITY', 'FOUNDATION'}


def tokens(s):
    return [t for t in norm(s).split() if t not in STOP and len(t) > 1]


def main():
    workdir = sys.argv[1]  # work/filings-detail
    repo = sys.argv[2]     # repo root

    import sqlite3
    em = json.load(open(f'{workdir}/entity-map.json'))
    dbf = sqlite3.connect(f'{workdir}/filings-2024-2026.sqlite')
    unmatched = [norm(n) for (n,) in dbf.execute(
        'select distinct client_name from filings where client_name is not null')
        if norm(n) and norm(n) not in em]

    # directory: name -> group_id, plus token inverted index over names+aliases
    db = json.loads(gzip.open(f'{repo}/lobbying-map/research/directory-base.json.gz')
                    .read().decode())
    groups = db['companies'] if isinstance(db, dict) and 'companies' in db else db
    print('groups:', len(groups))
    name2group = {}   # display/alias name -> group_id
    inv = collections.defaultdict(set)  # token -> group ids
    for g in groups:
        gid = g.get('id') or g.get('group_id')
        names = set([g.get('name', '')] + g.get('aliases', []))
        for nm in names:
            if not nm:
                continue
            name2group[nm] = gid
            for t in tokens(nm):
                inv[t].add(gid)

    group_names = collections.defaultdict(list)
    for nm, gid in name2group.items():
        group_names[gid].append(nm)
    df = {t: len(g) for t, g in inv.items()}
    jobs = []
    for nname in unmatched:
        ts = sorted(set(tokens(nname)), key=lambda t: df.get(t, 0))
        rare = [t for t in ts if 0 < df.get(t, 0) <= 5000][:4]
        cand_ids = collections.Counter()
        for t in rare:
            for gid in inv[t]:
                cand_ids[gid] += 1
        if not cand_ids:
            continue
        top = [gid for gid, _ in cand_ids.most_common(40)]
        cands = [{'id': gid, 'text': '; '.join(group_names[gid][:4])} for gid in top]
        if cands:
            jobs.append({'name': nname, 'candidates': cands})

    json.dump(jobs, open(f'{workdir}/entity-jobs.json', 'w'))
    print(f'unmatched: {len(unmatched)}, with candidates: {len(jobs)}')


if __name__ == '__main__':
    main()
