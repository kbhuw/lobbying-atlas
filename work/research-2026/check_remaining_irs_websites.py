import json,concurrent.futures,urllib.request,re,hashlib,time
from pathlib import Path
w=Path('work/research-2026');rows=json.loads((w/'remaining-unique-irs-candidates.json').read_text());out=w/'remaining-irs-website-checks.json';cache=w/'remaining-irs-web-cache';cache.mkdir(exist_ok=True)
def run(r):
 d={k:v for k,v in r.items() if k!='evidence'}
 try:
  req=urllib.request.Request(r['website'],headers={'User-Agent':'Mozilla/5.0 (compatible; public-record-research)'})
  with urllib.request.urlopen(req,timeout=15) as resp:s=resp.read(2500000).decode('utf-8','replace');d['resolved_url']=resp.url
  (cache/(r['id']+'.html')).write_text(s);d['sha256']=hashlib.sha256(s.encode()).hexdigest();e=r['ein'];pattern=r'(?<!\d)'+e[:2]+r'[-\s]?'+e[2:]+r'(?!\d)';hits=list(re.finditer(pattern,s));d['ein_matches']=[s[max(0,m.start()-200):m.end()+200] for m in hits];d['result']='fetched';d['city_mentioned']=r['city'].lower() in s.lower()
 except Exception as exc:d['result']='error';d['error']=str(exc)
 return d
start=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
 results=list(ex.map(run,rows))
out.write_text(json.dumps(results,indent=2)+'\n');hits=[r for r in results if r.get('ein_matches')];print(json.dumps({'total':len(results),'fetched':sum(r['result']=='fetched' for r in results),'seconds':round(time.monotonic()-start,1),'ein_matches':hits},indent=2))
