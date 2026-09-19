import sqlite3,pathlib,json,unicodedata,hashlib,gzip,collections,datetime,re,csv,io,shutil
root=pathlib.Path(__file__).resolve().parent
site=root.parent.parent/'lobbying-map';out=root.parent.parent/'outputs'/'federal-lobbying-directory';out.mkdir(parents=True,exist_ok=True)
public=site/'public'/'data';(public/'reports').mkdir(parents=True,exist_ok=True)
from cleaning import norm,key,date,period,latest_groups
db=sqlite3.connect(root/'directory.sqlite');db.row_factory=sqlite3.Row
db.execute('BEGIN')
expected=json.loads((root/'year-counts.json').read_text()) if (root/'year-counts.json').exists() else {}
coverage=[]
for y in range(1999,2027):
 n=db.execute('select count(*) from filings where year=?',(y,)).fetchone()[0];e=expected.get(str(y),0)
 coverage.append({'year':y,'expected':e,'actual':n,'status':'verified' if e and n==e else 'incomplete'})
complete=all(c['status']=='verified' for c in coverage)
companies={};groups={};records={};bad=[]
for raw in db.execute('select * from filings'):
 r=dict(raw);c=norm(r['client']);rid=r['id'];r['posted_iso']=date(r['posted']);r['current']=False
 if not c:bad.append({'id':rid,'reason':'missing client name'});continue
 cid=key(c);co=companies.setdefault(cid,{'id':cid,'name':c,'years':{},'issues':[]})
 if co['name']!=c:raise ValueError('Organization identifier collision')
 records[rid]=r
ambiguous=0
groups=latest_groups(records.values())
for g,(_,rs) in groups.items():
 ids=[r['id'] for r in rs]
 if len(ids)>1:ambiguous+=1
 # A tied active/no-activity pair is not treated as confirmed active.
 isactive=all('No Activity' not in records[i]['kind'] for i in ids)
 for i in ids:records[i]['current']=True
 if isactive:
  c=companies[g[0]];ys=str(g[2]);c['years'][ys]=c['years'].get(ys,0)+1
companies={k:v for k,v in companies.items() if v['years']}
issues=sqlite3.connect(root/'issues.sqlite');issue_names={}
if (root/'issue-codes.json').exists():issue_names={i['value']:i['name'] for i in json.loads((root/'issue-codes.json').read_text())}
for name,y,code in issues.execute('select client,year,code from issues'):
 cid=key(name)
 if cid in companies and str(y) in companies[cid]['years']:
  companies[cid]['issues'].append(issue_names.get(code,code))
for c in companies.values():c['issues']=sorted(set(c['issues']))
# Gzip shards keep downloads small and asset counts bounded.
shards=collections.defaultdict(lambda:collections.defaultdict(list));filing_count=0
for r in records.values():
 cid=key(r['client'])
 if cid not in companies:continue
 shards[cid[:2]][cid].append({k:r[k] for k in ['id','registrant','kind','amount','year','posted','posted_iso','current']});filing_count+=1
for prefix,content in shards.items():
 for rs in content.values():rs.sort(key=lambda r:(r['year'],r['posted_iso'],r['id']),reverse=True)
 (public/'reports'/(prefix+'.json.gz')).write_bytes(gzip.compress(json.dumps(content,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
result={'companies':sorted(companies.values(),key=lambda c:c['name']),'coverage':coverage,'records':sum(c['actual'] for c in coverage),'complete':complete,'status':'All 28 reporting-year totals match the LDA API' if complete else 'Archive indexing in progress — coverage is not yet complete','updated':datetime.datetime.now(datetime.timezone.utc).date().isoformat(),'ambiguous_latest_groups':ambiguous}
(public/'index.json.gz').write_bytes(gzip.compress(json.dumps(result,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
(public/'index.json').unlink(missing_ok=True)
report={'coverage':coverage,'complete':complete,'indexed_filings':sum(c['actual'] for c in coverage),'directory_organizations':len(companies),'directory_report_records':filing_count,'ambiguous_latest_groups':ambiguous,'missing_client_rows':bad,'identity_rule':'NFKC, uppercase, collapse whitespace; preserve punctuation. Exact name groups, not resolved corporate entities.','activity_rule':'Most recently posted filing per disclosed client name, registrant name, year, and reporting period. Exclude registrations and latest No Activity. Mixed tied statuses do not establish activity.','updated':result['updated']}
(out/'validation.json').write_text(json.dumps(report,indent=2))
with gzip.open(out/'company-years.csv.gz','wt',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['company_id','disclosed_name','reporting_year','active_reporting_relationships','issue_areas_all_indexed_years'])
 for c in result['companies']:
  for y,n in sorted(c['years'].items()):w.writerow([c['id'],("'"+c['name']) if c['name'].startswith(('=','+','-','@')) else c['name'],y,n,'; '.join(c['issues'])])
(out/'README.md').write_text(f'''# Federal lobbying directory\n\nStatus: {'COMPLETE' if complete else 'INCOMPLETE - acquisition in progress'}. Retrieved {result['updated']}.\n\n{len(records):,} indexed filings; {len(companies):,} disclosed-name groups with activity. Coverage reconciliation is in validation.json.\n\nSource: https://lda.gov/filings/public/filing/search/ and https://lda.gov/api/v1/filings/ . Issue labels supplemented by official House bulk files at https://disclosurespreview.house.gov/ .\n\nYear means reporting year, not submission year. All report versions are retained. Latest-per-name/registrant/period activity determines inclusion. {ambiguous:,} latest-posting ties are preserved; mixed activity/no-activity ties do not establish activity. Matching names is not proof of corporate identity; aliases, mergers, and same-name organizations are not manually resolved. Organizations are not classified as businesses versus nonprofits.\n\nCSV names starting with spreadsheet formula characters have a protective apostrophe; the database preserves the normalized disclosed name. Dollar strings are preserved as reported, not summed. Missing amounts remain missing. Issue labels cover available bulk history and may include prior versions. No inference of support, opposition, meetings, or outcomes is made.\n\nThe database contains filings (report metadata), companies, company_years, and source_queries. Join filings.company_id to companies.id. A null company_id means the disclosed client did not qualify for the activity directory. Original disclosures are at https://lda.gov/filings/public/filing/ID/print/ using the filing ID. Full report text is linked, not embedded.\n\nSenate Office of Public Records cannot vouch for the data or analyses derived from these data after the data have been retrieved from LDA.gov.\n''')
print(json.dumps({k:v for k,v in report.items() if k not in ['coverage','missing_client_rows']},indent=2))

if complete:
 db.commit()
 deliver=sqlite3.connect(out/'directory.sqlite')
 db.backup(deliver)
 deliver.executescript('DROP TABLE IF EXISTS companies; DROP TABLE IF EXISTS company_years; CREATE TABLE companies(id TEXT PRIMARY KEY,disclosed_name TEXT,issues_all_years TEXT); CREATE TABLE company_years(company_id TEXT,year INTEGER,active_reporting_relationships INTEGER,PRIMARY KEY(company_id,year)); CREATE TABLE IF NOT EXISTS source_queries(query_key TEXT PRIMARY KEY,url TEXT,retrieved_at TEXT);')
 deliver.executemany('INSERT OR REPLACE INTO coverage(year,expected,actual,status) VALUES(?,?,?,?)',[(c['year'],c['expected'],c['actual'],c['status']) for c in coverage])
 deliver.executemany('INSERT INTO companies VALUES(?,?,?)',[(c['id'],c['name'],json.dumps(c['issues'])) for c in companies.values()])
 deliver.executemany('INSERT INTO company_years VALUES(?,?,?)',[(c['id'],int(y),n) for c in companies.values() for y,n in c['years'].items()])
 deliver.execute('ALTER TABLE filings ADD COLUMN company_id TEXT')
 deliver.execute('ALTER TABLE filings ADD COLUMN posted_iso TEXT')
 deliver.execute('ALTER TABLE filings ADD COLUMN is_latest INTEGER')
 deliver.create_function('directory_company',1,lambda name:key(name) if key(name) in companies else None)
 deliver.create_function('record_posted',2,lambda rid,posted:records.get(rid,{}).get('posted_iso') or date(posted))
 deliver.create_function('record_latest',1,lambda rid:int(records.get(rid,{}).get('current',False)))
 deliver.execute('UPDATE filings SET company_id=directory_company(client),posted_iso=record_posted(id,posted),is_latest=record_latest(id)')
 deliver.execute('CREATE INDEX filings_company_year ON filings(company_id,year)')
 deliver.execute('CREATE INDEX company_years_year ON company_years(year)')
 for p in (root/'search-pages').glob('*.json'):
  d=json.loads(p.read_text())
  if 'url' in d:deliver.execute('INSERT OR REPLACE INTO source_queries VALUES(?,?,?)',(p.stem,d['url'],d['retrieved_at']))
 deliver.commit();print('SQLITE CHECK',deliver.execute('PRAGMA quick_check').fetchone()[0]);deliver.close()
