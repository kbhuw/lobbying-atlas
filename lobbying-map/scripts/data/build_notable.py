"""Build notable.json.gz — "worth a look" rollups for the UI.

Sections:
  revolving_door: lobbyists who reported a former government position,
                  ranked by the total spend on the filings they appear on.
  foreign:        clients headquartered outside the US (or activities
                  flagged as foreign-entity issues), ranked by spend.

Inputs:
  filings sqlite (work/filings-detail/filings-2024-2026.sqlite)
  desc-topics sqlite (work/jev/desc-topics.sqlite)   — JEV topic labels
  positions sqlite (work/jev/positions.sqlite)       — JEV job-bucket labels
  topics.json (work/jev/topics.json)                 — slug -> label

Usage: python3 build_notable.py <out.json.gz>
"""
import gzip, json, re, sqlite3, sys, collections

ROOT = '/home/ubuntu/repos/lobbying-atlas'
FILINGS = f'{ROOT}/work/filings-detail/filings-2024-2026.sqlite'
DESCS = f'{ROOT}/work/jev/desc-topics.sqlite'
POSITIONS = f'{ROOT}/work/jev/positions.sqlite'
TOPICS = f'{ROOT}/work/jev/topics.json'

ABBR = [
    (r'(?<![A-Za-z])Reps\.?(?=\s+[A-Z])', 'Representatives '),
    (r'(?<![A-Za-z])Rep\.?(?=\s+[A-Z])', 'Representative '),
    (r'(?<![A-Za-z])Sens\.?(?=\s+[A-Z])', 'Senators '),
    (r'(?<![A-Za-z])Sen\.?(?=\s+[A-Z])', 'Senator '),
    (r'\bLD\b', 'Legislative Director'),
    (r'\bLA\b', 'Legislative Assistant'),
    (r'\bLC\b', 'Legislative Correspondent'),
    (r'\bSA\b', 'Staff Assistant'),
    (r'\bCoS\b', 'Chief of Staff'),
    (r'\bDep\b\.?', 'Deputy'),
    (r'\bSr\b\.?', 'Senior'),
    (r'\bDir\b\.?', 'Director'),
    (r'\bAsst\b\.?', 'Assistant'),
    (r'\bLegis\.\s*', 'Legislative '),
    (r'\bLeg\b\.\s*', 'Legislative '),
    (r'\bProf\.\s*', 'Professional '),
    (r'\bComm\b\.?', 'Committee'),
    (r'\bCmte\b\.?', 'Committee'),
    (r'\bAdmin\b\.?', 'Administration'),
    (r'\bMgr\b\.?', 'Manager'),
    (r'\bCong\b\.?', 'Congressional'),
    (r'\bAmb\b\.?', 'Ambassador'),
    (r'\bSec\b\.?', 'Secretary'),
    (r'\bGen\b\.?', 'General'),
    (r'\bDept\b\.?', 'Department'),
    (r'\bU\.?S\.?\s+', 'US '),
    (r'\s+', ' '),
]

def clean_position(raw):
    """Most-informative clause of a messy covered_position string, expanded."""
    parts = [p.strip(' .;') for p in re.split(r';', raw or '') if p.strip()]
    if not parts:
        return ''
    senior = ['Member of Congress', 'Senator', 'Representative', 'Ambassador',
              'Secretary', 'Chief of Staff', 'Staff Director', 'Counsel',
              'Advisor', 'Director', 'Assistant', 'Special Assistant']
    def score(p):
        t = p
        for pat, rep in ABBR:
            t = re.sub(pat, rep, t)
        for i, kw in enumerate(senior):
            if kw.lower() in t.lower():
                return -i
        return len(senior)
    best = sorted(parts, key=score)[0]
    best = re.sub(r',?\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}.*$', '', best)
    best = re.sub(r',?\s*\d{4}\s*[-–]\s*(present|\d{4}).*$', '', best)
    for pat, rep in ABBR:
        best = re.sub(pat, rep, best)
    best = re.sub(r'\s*\(\s*[^)]*$', '', best)
    return best.strip(' ,.-–(')[:140]

BILL_RE = re.compile(
    r'\b(?:H\.?\s?R\.?|S\.?|H\.?\s?J\.?\s?Res\.?|S\.?\s?J\.?\s?Res\.?|'
    r'H\.?\s?Con\.?\s?Res\.?|S\.?\s?Con\.?\s?Res\.?|H\.?\s?Res\.?|'
    r'S\.?\s?Res\.?)\s*\.?\s*#?\s*\d+\b')
ACT_RE = re.compile(r'\b([A-Z][A-Za-z0-9&\'\-]*(?:\s+[A-Za-z0-9&\'\-,\(\)]+){0,7}?\s+Act)\b')
STOP_ACTS = {'the act', 'this act', 'such act', 'the clayton act', 'lobbying act'}

def extract_bills(texts, n=6):
    """Most-mentioned bill numbers and named Acts across a client's descriptions."""
    c = collections.Counter()
    for t, weight in (texts.items()):
        for m in BILL_RE.findall(t):
            c[re.sub(r'\s+', ' ', m).replace(' .', '.').strip(' .')] += weight
        for m in ACT_RE.findall(t):
            m = m.strip()
            if m.lower() in STOP_ACTS or len(m) > 70:
                continue
            c[m] += weight
    return [b for b, _ in c.most_common(n)]

def pick_says(texts, n=3, width=190):
    """A few verbatim filing descriptions, trimmed for display."""
    out = []
    for t, _ in texts.most_common(40):
        t = re.sub(r'\s+', ' ', t).strip(' ;,.')
        if len(t) < 25:
            continue
        if len(t) > width:
            cut = t[:width]
            cut = cut[:max(cut.rfind(';'), cut.rfind(','), cut.rfind(' and '), width - 30)]
            t = cut.rstrip(' ;,.') + '…'
        if t and all(t.lower() != o.lower() for o in out):
            out.append(t)
        if len(out) >= n:
            break
    return out

def clean_name(name):
    if name == name.upper() and len(name) > 4:
        name = name.title()
        small = r'\b(And|Of|The|For|In|On|At|De|La|Da|Di|Van|Von)\b'
        name = re.sub(small, lambda m: m.group(0).lower(), name)
        name = name[:1].upper() + name[1:]
        name = re.sub(r'\bIi\b', 'II', name)
        name = re.sub(r'\bIii\b', 'III', name)
        name = re.sub(r'\bIv\b', 'IV', name)
        name = re.sub(r'\bUs\b\.?', 'US', name)
        name = re.sub(r"'S\b", "'s", name)
        name = re.sub(r'\bLlc\b', 'LLC', name)
        name = re.sub(r'\bInc\b\.?', 'Inc.', name)
    return name.strip()

def main(out_path):
    f = sqlite3.connect(FILINGS)
    d = sqlite3.connect(DESCS)
    p = sqlite3.connect(POSITIONS)
    topics = {t['id']: t['label'] for t in json.load(open(TOPICS))}
    pos_bucket = {r[0]: r[1] for r in p.execute('select position, bucket from positions')}
    desc_topic = {r[0]: r[1] for r in d.execute('select description, topic from desc_topics')}

    # one pass: doc -> client, and doc -> topic counts
    doc_client, client_docs, client_total = {}, collections.Counter(), collections.Counter()
    for doc, client, amt in f.execute(
            'select doc_id, client_name, coalesce(income,0)+coalesce(expenses,0) from filings'):
        doc_client[doc] = client
        if client:
            client_docs[client] += 1
            client_total[client] += amt or 0
    doc_topics, client_topics = {}, collections.defaultdict(collections.Counter)
    for doc, desc in f.execute('select doc_id, description from activities where description is not null'):
        t = desc_topic.get(desc)
        if not t:
            continue
        doc_topics.setdefault(doc, collections.Counter())[t] += 1
        c = doc_client.get(doc)
        if c:
            client_topics[c][t] += 1

    # second pass: verbatim description counts, only for clients we'll display
    keep = set(sorted(client_total, key=lambda c: -client_total[c])[:220])
    keep |= {r[0] for r in f.execute(
        "select client_name from filings where client_country is not null"
        " and client_country not in ('USA','US','United States','')"
        " group by client_name")}
    client_texts = collections.defaultdict(collections.Counter)
    for doc, desc in f.execute('select doc_id, description from activities where description is not null'):
        c = doc_client.get(doc)
        if c in keep:
            client_texts[c][desc] += 1

    def topic_labels(counter, n=4):
        return [topics.get(t, t) for t, _ in counter.most_common(n)]

    # --- revolving door -----------------------------------------------------
    # dedupe amount per (lobbyist, doc): the doc's full amount counts once
    by_name = collections.defaultdict(lambda: {'total': 0.0, 'docs': set(),
                                               'positions': collections.Counter(),
                                               'clients': collections.defaultdict(float)})
    q = '''select l.first_name||' '||l.last_name, l.covered_position,
                  f.doc_id, f.client_name,
                  coalesce(f.income,0)+coalesce(f.expenses,0)
           from lobbyists l join filings f on f.doc_id=l.doc_id
           where l.covered_position is not null and l.covered_position!=''
             and l.covered_position not in ('N/A','n/a','NA')'''
    for name, pos, doc, client, amt in f.execute(q):
        e = by_name[name.strip().casefold()]
        e.setdefault('display', name.strip())
        e['positions'][pos] += 1
        if doc not in e['docs']:
            e['docs'].add(doc)
            e['total'] += amt
            if client:
                e['clients'][client] += amt

    rows = []
    for _key, e in by_name.items():
        name = e['display']
        # most senior bucket across the person's position strings
        buckets = [pos_bucket.get(pos, 'other') for pos in e['positions']]
        order = ['member_of_congress', 'congressional_leadership',
                 'executive_branch', 'agency', 'congressional_staff',
                 'military', 'other_gov', 'unclear']
        bucket = sorted(buckets, key=lambda b: order.index(b) if b in order else 99)[0]
        best_pos = max(e['positions'].items(), key=lambda kv: kv[1])[0]
        tc = collections.Counter()
        for doc in e['docs']:
            tc.update(doc_topics.get(doc, {}))
        rows.append({
            'name': clean_name(name),
            'bucket': bucket,
            'former': clean_position(best_pos),
            'total': round(e['total']),
            'filings': len(e['docs']),
            'clients': [clean_name(c) for c, _ in sorted(e['clients'].items(), key=lambda kv: -kv[1])[:4]],
            'topics': topic_labels(tc),
        })
    rows.sort(key=lambda r: -r['total'])
    revolving = rows[:150]

    # --- foreign-linked clients --------------------------------------------
    frows = f.execute('''select client_name, client_country, count(*),
                        sum(coalesce(income,0)+coalesce(expenses,0))
                        from filings
                        where client_country is not null
                          and client_country not in ('USA','US','United States','')
                        group by 1,2 order by 4 desc limit 100''').fetchall()
    foreign = []
    for client, country, n, amt in frows:
        descs = [r[0] for r in f.execute(
            'select a.description from activities a join filings fi on fi.doc_id=a.doc_id'
            ' where fi.client_name=? and a.description is not null limit 40', (client,))]
        tc = collections.Counter()
        for desc in descs:
            r = d.execute('select topic from desc_topics where description=?', (desc,)).fetchone()
            if r:
                tc[r[0]] += 1
        foreign.append({'client': clean_name(client), 'country': country, 'filings': n,
                        'total': round(amt or 0),
                        'topics': [topics.get(t, t) for t, _ in tc.most_common(4)],
                        'bills': extract_bills(client_texts.get(client, collections.Counter())),
                        'says': pick_says(client_texts.get(client, collections.Counter()), 2)})

    # --- biggest spenders: company -> what it lobbied on --------------------
    spenders = [{
        'client': clean_name(c),
        'total': round(client_total[c]),
        'filings': client_docs[c],
        'topics': topic_labels(client_topics[c]),
        'bills': extract_bills(client_texts.get(c, collections.Counter())),
        'says': pick_says(client_texts.get(c, collections.Counter()), 2),
    } for c in sorted(client_total, key=lambda c: -client_total[c])[:200]]

    out = {
        'revolving_door': revolving,
        'foreign': foreign,
        'spenders': spenders,
        'stats': {
            'lobbyists_former_gov': len(by_name),
            'former_members': sum(1 for r in rows if r['bucket'] == 'member_of_congress'),
        },
    }
    with gzip.open(out_path, 'wt') as fp:
        json.dump(out, fp)
    print(f'wrote {out_path}: {len(revolving)} insiders, {len(foreign)} foreign clients')


if __name__ == '__main__':
    main(sys.argv[1])
