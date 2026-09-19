import pathlib,sqlite3,json,gzip,collections,uuid
from cleaning import period,date
root=pathlib.Path(__file__).resolve().parents[2]
public=root/'public'/'data'
out=root/'outputs'/'federal-lobbying-directory'
d=json.loads(gzip.decompress((public/'index.json.gz').read_bytes()));r=json.loads((out/'validation.json').read_text())
assert d['complete'] and r['complete'], 'Incomplete year coverage'
assert len(d['coverage'])==28 and all(x['actual']==x['expected'] for x in d['coverage'])
db=sqlite3.connect(out/'directory.sqlite')
assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
assert db.execute('select count(*) from filings').fetchone()[0]==sum(x['expected'] for x in d['coverage'])
assert not db.execute('select 1 from filings where id is null or id="" or client is null limit 1').fetchone()
assert not db.execute('select 1 from filings f left join source_queries q on q.query_key=f.query_key where q.query_key is null limit 1').fetchone()
assert all(date(p) for (p,) in db.execute('select distinct posted from filings')), 'Unparsed posting date'
assert all(period(k) or k.startswith('Registration') for (k,) in db.execute('select distinct kind from filings')), 'Unknown report type'
companies={c['id']:c for c in d['companies']}
assert len(companies)==len(d['companies'])==r['directory_organizations']
assert len({c['name'] for c in companies.values()})==len(companies)
assert all(c['years'] and all(1999<=int(y)<=2026 and n>0 for y,n in c['years'].items()) for c in companies.values())
seen=set();report_count=0
for p in (public/'reports').glob('*.json.gz'):
 shard=json.loads(gzip.decompress(p.read_bytes()))
 for cid,rs in shard.items():
  assert cid in companies and cid.startswith(p.name[:2]);seen.add(cid)
  ids=set()
  for row in rs:
   uuid.UUID(row['id']);assert row['id'] not in ids;ids.add(row['id']);assert row['posted_iso'],row
  report_count+=len(rs)
assert seen==set(companies)
assert report_count==r['directory_report_records']
assert db.execute('select count(*) from filings where company_id is not null').fetchone()[0]==report_count
assert not db.execute('select 1 from filings f left join companies c on c.id=f.company_id where f.company_id is not null and c.id is null limit 1').fetchone()
print(json.dumps({'status':'PASS','filings':sum(x['actual'] for x in d['coverage']),'organizations':len(companies),'company_report_records':report_count,'verified_years':28,'shards':256},indent=2))
