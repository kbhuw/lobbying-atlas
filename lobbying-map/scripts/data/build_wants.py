"""One plain-English 'what they want' sentence per top spender.

Reads notable.json.gz (spenders: topics + named bills) and stances.json.gz
(AI-inferred supports/opposes/watching per org) and asks the model to write a
single no-jargon sentence describing what each company actually wants from
Washington. Output feeds the landing table — one sentence, that's it.

Usage: AI_GATEWAY_API_KEY=... python3 build_wants.py <out.json.gz>
Resumable: checkpoints into <out>.ckpt.json.
"""
import gzip, json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', '..', 'public', 'data', 'lobbying')
MODEL = 'openai/gpt-5-mini'
API = 'https://ai-gateway.vercel.sh/v1/chat/completions'

PROMPT = """You write for a public website that explains federal lobbying to ordinary people.

Company: {name}
Reported lobbying spend 2024–2026: {total}
Topics they lobbied on: {topics}
Bills named in their filings: {bills}
AI-inferred positions from their filings: {stances}

Write ONE sentence, max 28 words, starting "Wants to" (or "Wants"), saying in plain everyday English what this company or group is trying to get out of Washington. No bill numbers, no jargon, no lobbying terms. Concrete and specific — e.g. "Wants to keep the law that shields apps from lawsuits over user posts, and stop bills that would force kid-safety defaults on Instagram."
If it is an industry group, say whose interests it serves.
Return ONLY JSON: {{"want": "..."}}"""


def call(prompt):
    body = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_completion_tokens': 2000,
        'response_format': {'type': 'json_object'},
    }).encode()
    last = None
    for _ in range(2):
        req = urllib.request.Request(
            API, data=body,
            headers={'Authorization': f'Bearer {os.environ["AI_GATEWAY_API_KEY"]}',
                     'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=120) as r:
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
    ckpt = out_path + '.ckpt.json'
    notable = json.load(gzip.open(os.path.join(DATA, 'notable.json.gz')))
    try:
        stances = json.load(gzip.open(os.path.join(DATA, 'stances.json.gz')))
    except FileNotFoundError:
        stances = {'orgs': {}}

    done = json.load(open(ckpt)) if os.path.exists(ckpt) else {}
    rows = notable['spenders']
    todo = [r for r in rows if (r.get('org') or r['client']) not in done]
    print(f'{len(rows)} spenders, {len(done)} already done', flush=True)

    def work(r):
        key = r.get('org') or r['client']
        st = stances['orgs'].get(key) or stances['orgs'].get(r['client']) or {}
        bits = []
        for bucket, word in (('opposes', 'likely opposes'),
                             ('supports', 'likely supports')):
            for x in (st.get(bucket) or [])[:4]:
                bits.append(f"{word} {x['bill']} ({x.get('why','')})")
        watch = [x['bill'] for x in (st.get('watching') or [])[:4]]
        if watch:
            bits.append('working on ' + '; '.join(watch))
        p = PROMPT.format(
            name=r['client'],
            total=f"${r['total']:,}",
            topics=', '.join(r.get('topics') or []),
            bills='; '.join((r.get('bills') or [])[:6]),
            stances='; '.join(bits) or 'none inferred',
        )
        try:
            res = call(p)
            return key, res.get('want', '')
        except Exception as e:
            print('ERR', r['client'], repr(e), flush=True)
            return key, None

    with ThreadPoolExecutor(6) as ex:
        for i, (k, v) in enumerate(ex.map(work, todo)):
            if v:
                done[k] = v
            if i % 10 == 0:
                json.dump(done, open(ckpt, 'w'))
    json.dump(done, open(ckpt, 'w'))
    with gzip.open(out_path, 'wt') as fp:
        json.dump(done, fp)
    print(f'wrote {out_path}: {len(done)} wants')


if __name__ == '__main__':
    main()
