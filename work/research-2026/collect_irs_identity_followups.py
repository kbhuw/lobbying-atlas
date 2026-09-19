import json,concurrent.futures,urllib.request,urllib.parse,re,hashlib,time
from pathlib import Path
from bs4 import BeautifulSoup
w=Path('work/research-2026');p=json.loads((w/'reviewed.json').read_text());rs=json.loads((w/'remaining-irs-website-checks.json').read_text());cache=w/'irs-identity-followup-cache';cache.mkdir(exist_ok=True);jobs=[]
for r in rs:
 if r['result']!='fetched' or p[r['id']].get('ownership')!='Unknown':continue
 root=urllib.parse.urlparse(r['resolved_url']);html=(w/'remaining-irs-web-cache'/f"{r['id']}.html").read_text();s=BeautifulSoup(html,'html.parser');choices=[]
 for a in s.find_all('a',href=True):
  u=urllib.parse.urljoin(r['resolved_url'],a['href']).split('#')[0];up=urllib.parse.urlparse(u);label=a.get_text(' ',strip=True).lower();path=up.path.lower()
  if up.scheme not in ['https','http'] or up.netloc!=root.netloc or u.rstrip('/')==r['resolved_url'].rstrip('/') or up.query or re.search(r'\.(pdf|png|jpg|svg|zip)$',path):continue
  rank=0 if label in ['contact','contact us','about','about us','who we are'] else 1 if re.search(r'/(about|contact|who-we-are|financials|annual-reports)(/|$)',path) else 9
  if rank<9:choices.append((rank,u))
 urls=list(dict.fromkeys(u for _,u in sorted(choices)))[:3]
 for n,u in enumerate(urls):jobs.append((r,n,u))
def run(job):
 r,n,u=job;d={'id':r['id'],'name':r['name'],'ein':r['ein'],'url':u,'cache_file':f"{r['id']}-{n}.html"}
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (compatible; public-record-research)'}),timeout=12) as resp:
   if 'text/html' not in resp.headers.get('content-type',''):raise ValueError('Not HTML')
   html=resp.read(2000000).decode('utf-8','replace');d['resolved_url']=resp.url
  (cache/d['cache_file']).write_text(html);d['sha256']=hashlib.sha256(html.encode()).hexdigest();s=BeautifulSoup(html,'html.parser')
  for t in s(['script','style']):t.decompose()
  text=s.get_text(' ',strip=True);e=r['ein'];d['ein_match']=bool(re.search(r'(?<!\d)'+e[:2]+r'[-\s]?'+e[2:]+r'(?!\d)',html));d['city_mentioned']=r['city'].lower() in text.lower();d['result']='fetched'
 except Exception as exc:d.update(result='error',error=str(exc))
 return d
start=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:results=list(ex.map(run,jobs))
(w/'irs-identity-followup-results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'pages':len(results),'fetched':sum(r['result']=='fetched' for r in results),'seconds':round(time.monotonic()-start,1),'ein_matches':[r for r in results if r.get('ein_match')]},indent=2))
