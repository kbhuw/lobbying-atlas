"""Publish sourced annotations and a complete, resumable per-entry research queue."""
import collections, datetime, gzip, json, pathlib, sqlite3, unicodedata
from organization_names import display

project = pathlib.Path(__file__).resolve().parents[2]
root = project.parent / 'work/organization-research'
data = json.load(gzip.open(project / 'public/data/directory-v2.json.gz'))
profiles = json.loads((project / 'research/profiles.json').read_text())
overlay=project/'research/reviewed-2026.json'
if overlay.exists():profiles.update(json.loads(overlay.read_text()))
elif overlay.with_suffix('.json.gz').exists():profiles.update(json.load(gzip.open(overlay.with_suffix('.json.gz'))))
ids = {c['id'] for c in data['companies']}
assert not profiles.keys() - ids, 'Annotation refers to a missing directory entry'

def exact(s):
    return ' '.join(unicodedata.normalize('NFKC', s).upper().split())

clients = collections.defaultdict(list)
db = root / 'research.sqlite'
if db.exists():
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
        conn.row_factory = sqlite3.Row
        for row in conn.execute('SELECT * FROM lda_clients ORDER BY effective_date DESC, id DESC'):
            if row['description'] and row['description'].strip():
                clients[exact(row['name'])].append(dict(row))

# House bulk descriptions complement the rate-limited API. Match disclosed
# spelling only; never use corporate stem matching for this source join.
bulk = collections.defaultdict(dict)
def signed_iso(value, fallback=''):
    if not value:return fallback
    for fmt in ('%m/%d/%Y %I:%M:%S %p','%m/%d/%Y','%Y-%m-%d','%m/%d/%Y %H:%M:%S'):
        try:return datetime.datetime.strptime(value,fmt).date().isoformat()
        except ValueError:pass
    return fallback
bulkdb=root/'bulk-profiles.sqlite'
if bulkdb.exists():
    with sqlite3.connect(f'file:{bulkdb}?mode=ro',uri=True) as conn:
        conn.row_factory=sqlite3.Row
        for record in conn.execute("SELECT * FROM descriptions WHERE trim(description)!=''"):
            r=dict(record);key=exact(r['name']);desc=' '.join(r['description'].split())
            r['description']=desc;r['date']=signed_iso(r.get('signed_date'),signed_iso(r.get('effective_date'),r.get('report_year') or ''))
            old=bulk[key].get(desc)
            if old is None or r['date']>old['date']:bulk[key][desc]=r
registry_path=root/'registry-profiles.json'
registries=json.loads(registry_path.read_text()) if registry_path.exists() else {}
# Related foundations can share names and addresses; withhold these joins pending individual identity review.
holds_path=project/'research/registry-match-holds.json'
holds=json.loads(holds_path.read_text()) if holds_path.exists() else {}
registries={k:v for k,v in registries.items() if k not in holds}
taxpath=project/'research/registry-websites.json'
taxsites=json.loads(taxpath.read_text()) if taxpath.exists() else {}
counts = collections.Counter()
queue = []
for c in data['companies']:
    # Display the disclosed spelling; matching normalization must never erase it.
    c['name'] = display(min(c['aliases'], key=lambda s: (len(s), s)))
    p = profiles.get(c['id'])
    if not p and c['id'] in registries:
        p=dict(registries[c['id']]);p['name']=c['name']
    if p:
        assert p['status'] in ('sourced', 'unresolved', 'registry_matched')
        assert p['sources'] and p['description'] and p['as_of']
        assert all(s['url'].startswith('https://') and s['claim'] for s in p['sources'])
        if p['ownership'] == 'Publicly traded':
            exchanges = ('NASDAQ:', 'NYSE:', 'NYSE AMERICAN:', 'OTC:', 'CBOE:', 'ASX:', 'NSE:', 'BUDAPEST:', 'EURONEXT:', 'XETRA:', 'SIX:', 'HKEX:', 'TSX:', 'KOSPI:')
            assert p['status']=='registry_matched' or any(exchange in s['claim'].upper() for s in p['sources'] for exchange in exchanges)
        c['name'] = p['name']
    else:
        rows = {r['id']:r for a in c['aliases'] for r in clients.get(exact(a), [])}
        rows = sorted(rows.values(), key=lambda r:(r['effective_date'] or '',r['id']), reverse=True)
        if rows:
            r = rows[0]
            p = dict(name=c['name'], description=' '.join(r['description'].split()), kind='Unknown', ownership='Unknown', website='', status='self_reported', featured=False, as_of=r['checked_at'][:10], checked_at=r['checked_at'][:10], legal_form='', notes='Self-reported LDA client description, matched by exact disclosed name. Identity and ownership have not been independently checked. Multiple clients can share a name.', sources=[dict(label=f"LDA client {r['id']}", url=r['source_url'], claim='Self-reported description; client effective date '+str(r['effective_date']))], other_descriptions=[dict(description=x['description'], url=x['source_url'], effective_date=x['effective_date']) for x in rows[1:]])
    # Add the newest available bulk description without promoting it to
    # individually sourced research or overwriting a researched identity.
    observations={r['description']:r for a in c['aliases'] for r in bulk.get(exact(a),{}).values()}
    observations=sorted(observations.values(),key=lambda r:r['date'],reverse=True)
    if observations and (not p or p['status'] in ('self_reported','registry_matched')):
        r=observations[0]
        source=dict(label='House disclosure — '+r['source_member'],url=r['source_url'],claim='Self-reported '+r['source_field']+' in '+r['source_member']+'; signed '+str(r.get('signed_date') or 'date unavailable')+'.')
        if p and p['status']=='registry_matched':
            p['disclosed_description']=r['description'];p['sources']=p['sources']+[source]
        elif not p:
            p=dict(name=c['name'],description=r['description'],kind='Unknown',ownership='Unknown',website='',status='self_reported',featured=False,as_of=r['date'],checked_at=r['extracted_at'][:10],legal_form='',notes='Self-reported description from a House lobbying disclosure, matched by disclosed name. Identity and ownership have not been independently checked. The description may be historical.',sources=[source])
        else:
            # API client descriptions have no last-modified date, so retain
            # them as the displayed text and expose dated filing history below.
            p['as_of']=p['checked_at']
        p['other_descriptions']=[dict(description=x['description'],url=x['source_url'],effective_date=x['date'],member=x['source_member']) for x in observations[:5] if x['description']!=p['description']]
    if p and not p.get('website') and c['id'] in taxsites and p['status']=='registry_matched':
        tax=taxsites[c['id']];p['website']=tax['website'];p['website_status']='filed';p['sources']=p['sources']+[tax['website_source']]
    if p:
        c['profile'] = p
    status = p['status'] if p else 'pending'
    counts[status] += 1
    queue.append(dict(id=c['id'], name=c['name'], aliases=c['aliases'], status=status))

data['research'] = dict(total=len(ids), counts=dict(counts), updated=datetime.datetime.now(datetime.timezone.utc).isoformat(), definition='Sourced profiles have individual research. Registry matches use legal name and city/state automatically and remain a separate evidence tier. Self-reported descriptions come from filings. Historical identity questions and unknown fields may remain.')
(project/'research/publication-metadata.json').write_text(json.dumps(data['research'],indent=2)+'\n')
with gzip.GzipFile(filename=str(project/'public/data/directory-v3.json.gz'), mode='wb', mtime=0) as f:
    f.write(json.dumps(data,ensure_ascii=False,separators=(',',':')).encode())
root.mkdir(parents=True,exist_ok=True)
(root/'queue.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in sorted(queue,key=lambda r:r['name'].casefold())))
(root/'research-progress.json').write_text(json.dumps(data['research'],indent=2)+'\n')
output=project.parent/'outputs/organization-annotations'
output.mkdir(parents=True,exist_ok=True)
(output/'profiles.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2)+'\n')
(output/'progress.json').write_text(json.dumps(data['research'],indent=2)+'\n')
print(json.dumps(data['research'],indent=2))
