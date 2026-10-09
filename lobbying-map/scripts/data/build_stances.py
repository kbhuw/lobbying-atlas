"""Infer org stances on named bills via the Vercel AI Gateway.

Filings never state positions, so for each heavily-lobbied bill we send the
model the bill's name plus every top-spender org that mentioned it (with a
verbatim sample line) and ask it to explain the bill and bucket each org as
supports / opposes / watching. Output feeds the stance boards in the app.

Usage: AI_GATEWAY_API_KEY=... python3 build_stances.py <out.json.gz> [max_bills]
Resumable: checkpoints into <out>.ckpt.json so re-runs skip finished bills.
"""
import collections, gzip, json, os, re, sqlite3, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_notable import BILL_RE, ACT_RE, ok_bill, bill_key, clean_name, norm  # noqa: E402

ROOT = '/home/ubuntu/repos/lobbying-atlas'
FILINGS = f'{ROOT}/work/filings-detail/filings-2024-2026.sqlite'
ENTITY_MAP = f'{ROOT}/work/filings-detail/entity-map.json'
MODEL = 'openai/gpt-5-mini'
API = 'https://ai-gateway.vercel.sh/v1/chat/completions'
TOP_ORGS = 600          # orgs by reported spend eligible for stance buckets
MAX_ORGS_PER_BILL = 18
MAX_BILLS_DEFAULT = 350

PROMPT = """You are analyzing US federal lobbying disclosures. Lobbying filings NEVER state whether a filer supports or opposes a bill — they only list what was lobbied on. Infer the likely stance from the filing language and your knowledge of what the bill does and who each organization is.

Bill or law being lobbied: {bill}

Organizations that lobbied on it, with a verbatim filing line from each:
{orgs}

Rules:
- "supports"/"opposes" only when the language or the org's well-known interest makes it clear (e.g. "repeal of X" lobbied by X's beneficiaries = oppose the repeal; a drugmaker on the Inflation Reduction Act drug-negotiation provisions = opposes).
- If the filing says "issues related to", "monitoring", "implementation of", or the bill is a must-pass vehicle (NDAA, appropriations, budget reconciliation) where orgs lobby for carve-outs rather than for/against the bill itself, use "watching".
- When uncertain, use "watching" — never guess opposition.

Return ONLY JSON: {{"name": "common name for this bill", "about": "one plain-English sentence: what this bill would do", "positions": [{{"org": "<exact org name from the list>", "stance": "supports"|"opposes"|"watching", "why": "<=12 words, plain English"}}]}}"""


def call_model(bill, org_lines):
    body = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'user', 'content': PROMPT.format(
            bill=bill, orgs='\n'.join(org_lines))}],
        'max_completion_tokens': 16000,
        'response_format': {'type': 'json_object'},
    }).encode()
    last = None
    for _ in range(2):
        req = urllib.request.Request(
            API, data=body,
            headers={'Authorization': f'Bearer {os.environ["AI_GATEWAY_API_KEY"]}',
                     'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=180) as r:
            out = json.load(r)
        text = out['choices'][0]['message'].get('content') or ''
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            last = e
            m = re.search(r'\{.*\}', text, re.S)
            if m:
                try:
                    return json.loads(m.group(0))
                except json.JSONDecodeError:
                    pass
    raise last


def main():
    out_path = sys.argv[1]
    max_bills = int(sys.argv[2]) if len(sys.argv) > 2 else MAX_BILLS_DEFAULT
    ckpt_path = out_path + '.ckpt.json'

    db = sqlite3.connect(FILINGS)
    db.row_factory = sqlite3.Row
    try:
        entity_map = {norm(e['name']): e['group_id']
                      for e in json.load(open(ENTITY_MAP)).values()}
    except FileNotFoundError:
        entity_map = {}

    # org totals -> top spenders
    totals = collections.Counter()
    for name, inc, exp in db.execute(
            'select client_name, income, expenses from filings'):
        totals[name] += (inc or 0) + (exp or 0)
    top = {c for c, _ in totals.most_common(TOP_ORGS)}

    # bill -> org -> {count, sample}
    bill_orgs = collections.defaultdict(dict)
    for (desc, cname) in db.execute(
            '''select a.description, f.client_name from activities a
               join filings f on f.doc_id=a.doc_id
               where a.description is not null'''):
        if cname not in top:
            continue
        seen = set()
        for m in BILL_RE.findall(desc):
            m = re.sub(r'\s+', ' ', m).replace(' .', '.').strip(' .')
            if m:
                seen.add(bill_key(m) or m)
        for m in ACT_RE.findall(desc):
            m = ok_bill(m)
            if m:
                seen.add(bill_key(m))
        for k in seen:
            ent = bill_orgs[k].setdefault(cname, {'n': 0, 'sample': '', 'name': ''})
            ent['n'] += 1
            if not ent['sample']:
                ent['sample'] = re.sub(r'\s+', ' ', desc).strip()[:300]
    # keep a display name per bill key
    bill_names = collections.defaultdict(collections.Counter)
    for (desc,) in db.execute('select description from activities where description is not null'):
        for m in BILL_RE.findall(desc):
            m = re.sub(r'\s+', ' ', m).replace(' .', '.').strip(' .')
            if m:
                bill_names[bill_key(m)][m] += 1
        for m in ACT_RE.findall(desc):
            m = ok_bill(m)
            if m:
                bill_names[bill_key(m)][m] += 1

    # bills ranked by distinct top-org count
    ranked = sorted(bill_orgs.items(), key=lambda kv: -len(kv[1]))
    ranked = [(k, v) for k, v in ranked if len(v) >= 2][:max_bills]
    print(f'{len(ranked)} bills to classify', flush=True)

    done = {}
    if os.path.exists(ckpt_path):
        done = json.load(open(ckpt_path))
    print(f'{len(done)} already done', flush=True)

    def work(k, orgs):
        name = bill_names[k].most_common(1)[0][0]
        org_items = sorted(orgs.items(), key=lambda kv: -totals[kv[0]])[:MAX_ORGS_PER_BILL]
        lines = [f'- {clean_name(c)}: "{v["sample"]}"' for c, v in org_items]
        try:
            r = call_model(name, lines)
        except Exception as e:
            return k, None, repr(e)
        return k, r, None

    todo = [(k, v) for k, v in ranked if k not in done]
    with ThreadPoolExecutor(6) as ex:
        for i, (k, r, err) in enumerate(ex.map(lambda kv: work(*kv), todo)):
            if r:
                done[k] = r
            else:
                print('ERR', bill_names[k].most_common(1)[0][0], err, flush=True)
            if i % 10 == 0:
                json.dump(done, open(ckpt_path, 'w'))
    json.dump(done, open(ckpt_path, 'w'))

    # assemble output
    bills_out = []
    orgs_out = collections.defaultdict(
        lambda: {'supports': [], 'opposes': [], 'watching': []})
    for k, orgs in ranked:
        r = done.get(k)
        if not r or 'positions' not in r:
            continue
        entry = {'key': k, 'name': r.get('name') or bill_names[k].most_common(1)[0][0],
                 'about': r.get('about', ''),
                 'supports': [], 'opposes': [], 'watching': []}
        by_name = {c: v for c, v in orgs.items()}
        clean_lookup = {clean_name(c): c for c in by_name}
        for p in r['positions']:
            stance = p.get('stance')
            o = p.get('org', '')
            cname = clean_lookup.get(o) or o
            if stance not in entry:
                continue
            disp = clean_name(cname)
            gid = entity_map.get(norm(cname))
            entry[stance].append({'org': disp, 'why': p.get('why', ''),
                                  'id': gid})
            slot = {'bill': entry['name'], 'why': p.get('why', '')}
            orgs_out[gid or disp][stance].append(slot)
        entry['org_count'] = len(by_name)
        bills_out.append(entry)

    # orgs keyed by directory group id where resolvable, else display name
    out = {'bills': sorted(bills_out, key=lambda b: -b['org_count']),
           'orgs': dict(orgs_out)}
    with gzip.open(out_path, 'wt') as fp:
        json.dump(out, fp)
    n_pos = sum(len(b['supports']) + len(b['opposes']) + len(b['watching'])
                for b in bills_out)
    print(f'wrote {out_path}: {len(bills_out)} bills, {len(orgs_out)} orgs, {n_pos} positions')


if __name__ == '__main__':
    main()
