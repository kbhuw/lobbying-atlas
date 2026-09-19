import json,re,requests,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
p=Path('work/research-2026');a=json.loads((p/'featured47-first10-reviewed.json').read_text())+json.loads((p/'featured47-followups-reviewed.json').read_text());urls={r['legal_name_url'] for r in a if r['decision']=='propose'};out=p/'featured47-source-cache';out.mkdir(exist_ok=True)
def fetch(u):
 import hashlib
 f=out/(hashlib.sha256(u.encode()).hexdigest()[:16]+'.json')
 try:
  r=requests.get(u,timeout=20,headers={'User-Agent':'Mozilla/5.0'});s=BeautifulSoup(r.content,'html.parser') if 'pdf' not in r.headers.get('content-type','') else None
  if s:
   for e in s(['style','script','noscript']):e.decompose()
  d={'url':u,'final_url':r.url,'status':r.status_code,'text':s.get_text(' ',strip=True) if s else '', 'pdf':s is None}
 except Exception as e:d={'url':u,'error':str(e)}
 f.write_text(json.dumps(d,ensure_ascii=False));return {'url':u,'path':str(f),'status':d.get('status'),'text_len':len(d.get('text',''))}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:rows=list(ex.map(fetch,urls))
(out/'index.json').write_text(json.dumps(rows,indent=2));print(rows)
