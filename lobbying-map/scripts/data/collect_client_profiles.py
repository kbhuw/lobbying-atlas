"""Resumable public LDA client-description collection. No classification by name."""
import pathlib,os,json,time,urllib.request,urllib.error,sqlite3,datetime,fcntl,hashlib
project=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(os.environ.get('LOBBYING_RESEARCH_DIR',str(project.parent/'work/organization-research')));root.mkdir(parents=True,exist_ok=True)
lock=(root/'collector.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
(root/'pages').mkdir(exist_ok=True)
c=sqlite3.connect(root/'research.sqlite');c.execute('PRAGMA journal_mode=WAL');c.execute('CREATE TABLE IF NOT EXISTS lda_clients(id INTEGER PRIMARY KEY,name TEXT,description TEXT,state TEXT,country TEXT,government INTEGER,effective_date TEXT,source_url TEXT,checked_at TEXT)');c.execute('CREATE TABLE IF NOT EXISTS collector_state(key TEXT PRIMARY KEY,value TEXT)');c.commit()
row=c.execute("SELECT value FROM collector_state WHERE key='next'").fetchone()
u=json.loads(row[0]) if row else 'https://lda.gov/api/v1/clients/?format=json&page_size=25&ordering=id'
last=0
while u:
 time.sleep(max(0,5.5-(time.monotonic()-last)));last=time.monotonic()
 try:
  with urllib.request.urlopen(u,timeout=60) as r:raw=r.read()
  d=json.loads(raw);assert isinstance(d['results'],list)
 except Exception as e:
  print('RETRY',type(e).__name__,str(e),flush=True);time.sleep(65);continue
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 records=[{k:v for k,v in r.items() if k!='registrant'} for r in d['results']]
 (root/'pages'/(hashlib.sha256(u.encode()).hexdigest()+'.json')).write_text(json.dumps({'url':u,'retrieved_at':now,'count':d['count'],'next':d['next'],'results':records}))
 for r in records:
  c.execute('INSERT OR REPLACE INTO lda_clients VALUES(?,?,?,?,?,?,?,?,?)',(r['id'],r['name'],r.get('general_description'),r.get('state_display'),r.get('country_display'),r.get('client_government_entity'),r.get('effective_date'),r['url'],now))
 u=d['next'];c.execute("INSERT OR REPLACE INTO collector_state VALUES('next',?)",(json.dumps(u),));c.commit()
 n=c.execute('SELECT count(*) FROM lda_clients').fetchone()[0]
 status={'collected_client_records':n,'expected_client_records':d['count'],'complete':not u,'last_success':now,'next':u,'scope':'LDA self-reported descriptions; independent research is a separate queue'}
 temp=root/'collector-progress.tmp';temp.write_text(json.dumps(status,indent=2));temp.replace(root/'collector-progress.json')
 print(n,'/',d['count'],'COMPLETE' if not u else '',flush=True)
print('COLLECTION COMPLETE',flush=True)
