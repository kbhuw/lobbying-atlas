from zoneinfo import ZoneInfo
import string
import urllib.request,urllib.parse,json,pathlib,hashlib,gzip,time,datetime as dt,sqlite3,threading,concurrent.futures
from lxml import html
root=pathlib.Path(__file__).resolve().parent
(root/'search-pages').mkdir(exist_ok=True)
lock=threading.Lock(); pace=threading.Lock(); last=[0.0]
db=sqlite3.connect(root/'directory.sqlite',check_same_thread=False)
db.execute('PRAGMA journal_mode=WAL')
db.execute('CREATE TABLE IF NOT EXISTS filings(id TEXT PRIMARY KEY, registrant TEXT, client TEXT, kind TEXT, amount TEXT, year INTEGER, posted TEXT, query_key TEXT)')
db.execute('CREATE TABLE IF NOT EXISTS coverage(year INTEGER PRIMARY KEY, expected INTEGER, actual INTEGER, status TEXT)')
db.commit()
def request(params):
 url='https://lda.gov/filings/public/filing/search/?'+urllib.parse.urlencode(dict(search='search',**params))
 key=hashlib.sha256(url.encode()).hexdigest();p=root/'search-pages'/(key+'.html.gz')
 if p.exists():b=gzip.decompress(p.read_bytes())
 else:
  for attempt in range(6):
   try:
    with pace:
     time.sleep(max(0,1.0-(time.monotonic()-last[0])));last[0]=time.monotonic()
    with urllib.request.urlopen(url,timeout=90) as r:b=r.read()
    if b'<table' not in b and b'No Reports' not in b and b'No reports' not in b: # zero-result page still has table in standard form
     if b'searchResults' not in b and b'Search LD-1' not in b:raise ValueError('unexpected response')
    p.write_bytes(gzip.compress(b));(root/'search-pages'/(key+'.json')).write_text(json.dumps({'url':url,'retrieved_at':dt.datetime.now(dt.timezone.utc).isoformat()}));break
   except Exception as e:
    print('RETRY',params,repr(e),flush=True);time.sleep(min(60,5*2**attempt))
  else:raise RuntimeError('request failed '+url)
 doc=html.fromstring(b)
 rows=[]
 for tr in doc.xpath('//table[@id="searchResults"]/tbody/tr'):
  cells=tr.xpath('./td');a=tr.xpath('.//a[contains(@href,"/print/")]')
  if len(cells)!=6 or not a:raise ValueError('unexpected row')
  t=[' '.join(c.itertext()).strip() for c in cells];t=[' '.join(x.split()) for x in t]
  fid=a[0].get('href').split('/filing/')[1].split('/')[0]
  rows.append((fid,t[0],t[1],t[2],t[3],int(t[4]),t[5],key))
 limited=b'Too Many Results' in b
 if True:
  with lock:db.executemany('INSERT OR IGNORE INTO filings VALUES(?,?,?,?,?,?,?,?)',rows);db.commit()
 return limited,len(rows),{r[0] for r in rows}
def walk(year,start=None,end=None,amount=None):
 p={'report_year':year}
 if start:p.update(report_dt_posted_from=start.strftime('%m/%d/%Y'),report_dt_posted_to=end.strftime('%m/%d/%Y'))
 if amount:p.update(report_amount_reported_min=amount[0],report_amount_reported_max=amount[1])
 limited,n,ids=request(p)
 if not limited:return n
 if not start:return walk(year,dt.date(1900,1,1),dt.date(2026,9,5))
 days=(end-start).days
 if days:
  mid=start+dt.timedelta(days=days//2)
  return walk(year,start,mid)+walk(year,mid+dt.timedelta(days=1),end)
 api='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'format':'json','page_size':1,'filing_year':year,'filing_dt_posted_after':dt.datetime.combine(start,dt.time.min,ZoneInfo('America/New_York')).isoformat(),'filing_dt_posted_before':dt.datetime.combine(end,dt.time.max,ZoneInfo('America/New_York')).isoformat()})
 countfile=root/'search-pages'/('count-v2-'+str(year)+'-'+start.isoformat()+'.json')
 if countfile.exists(): expected=json.loads(countfile.read_text())['count']
 else:
  for attempt in range(5):
   try:
    time.sleep(4.2)
    with urllib.request.urlopen(api,timeout=60) as r:d=json.load(r)
    countfile.write_text(json.dumps(d));expected=d['count'];break
   except Exception:time.sleep(30)
  else:raise RuntimeError('Could not verify day count')
 for letter in 'aeiortnslcudpmhgbfywvkjxzq0123456789&-':
  if len(ids)==expected:break
  _,_,found=request(dict(p,client=letter));ids.update(found)
 if len(ids)!=expected:
  for letter in 'aeiortnslcudpmhgbfywvkjxzq':
   if len(ids)==expected:break
   _,_,found=request(dict(p,registrant=letter));ids.update(found)
 if len(ids)!=expected:raise RuntimeError('day mismatch '+str(p)+' '+str(len(ids))+'/'+str(expected))
 print('DAY VERIFIED',year,start,len(ids),flush=True)
 return len(ids)
def run(year):
 try:
  counts_path=root/'year-counts.json'
  expected=json.loads(counts_path.read_text()).get(str(year)) if counts_path.exists() else None
  with lock: actual=db.execute('SELECT count(*) FROM filings WHERE year=?',(year,)).fetchone()[0]
  if expected and actual==expected:
   print('YEAR ALREADY VERIFIED',year,actual,flush=True);return
  n=walk(year)
  with lock:
   actual=db.execute('SELECT count(*) FROM filings WHERE year=?',(year,)).fetchone()[0]
   db.execute('INSERT INTO coverage(year,actual,status) VALUES(?,?,?) ON CONFLICT(year) DO UPDATE SET actual=excluded.actual,status=excluded.status',(year,actual,'search_complete'));db.commit()
  print('YEAR DONE',year,n,actual,flush=True)
 except Exception as e:
  with lock:
   db.execute('INSERT INTO coverage(year,status) VALUES(?,?) ON CONFLICT(year) DO UPDATE SET status=excluded.status',(year,'ERROR '+str(e)));db.commit()
  print('YEAR ERROR',year,repr(e),flush=True)
if __name__=='__main__':
 import sys
 years=[int(y) for y in sys.argv[1:]] or list(range(2026,1998,-1))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(run,years))
 print('FINISHED',flush=True)
