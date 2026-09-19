import json,concurrent.futures,pathlib,requests,hashlib
from bs4 import BeautifulSoup
p=pathlib.Path('work/research-2026/featured48-source-cache');p.mkdir(exist_ok=True)
a=json.load(open('work/research-2026/featured48-next20-reviewed.json'))
u=sorted(set(q['url'] for x in a if x['decision']=='propose' for q in x.get('exactQuotes',[]) if not q['url'].endswith('.zip'))|{'https://www.cantor.com/','https://www.caliber.com/','https://www.californiacity-ca.gov/'})
def get(u):
 try:
  r=requests.get(u,timeout=35);s=BeautifulSoup(r.text,'html.parser'); [x.decompose() for x in s(['script','style'])];t=s.get_text(' ',strip=True)
  d={'url':u,'status':r.status_code,'final_url':r.url,'text':t};f=p/(hashlib.sha256(u.encode()).hexdigest()[:12]+'.json');f.write_text(json.dumps(d));return {'url':u,'status':r.status_code,'length':len(t),'path':str(f)}
 except Exception as e:return {'url':u,'error':str(e)}
r=list(concurrent.futures.ThreadPoolExecutor(max_workers=8).map(get,u));(p/'index.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
