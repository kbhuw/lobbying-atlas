import json,pathlib,requests,concurrent.futures
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));c=json.load(open(r/'sbir-unresolved-candidates.json'));out=r/'sbir207-sites';out.mkdir(exist_ok=True)
a=[x for x in c if p[x['id']]['review_outcome']!='confirmed' and not x['same_domain'] and any(y['Company Website'] for y in x['records'])]
def fetch(x):
 u=next(y['Company Website'] for y in x['records'] if y['Company Website']);u='https://'+u.split('://')[-1]
 try:
  z=requests.get(u,timeout=12);(out/(x['id']+'.html')).write_text(z.text);s=BeautifulSoup(z.text,'html.parser')
  for t in s(['script','style']):t.decompose()
  return dict(id=x['id'],name=x['name'],url=u,final_url=z.url,status=z.status_code,text=s.get_text(' ',strip=True)[:18000],images=[dict(src=t.get('src'),alt=t.get('alt')) for t in s.find_all('img')][:30])
 except Exception as e:return dict(id=x['id'],name=x['name'],url=u,error=str(e)[:200])
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:res=list(ex.map(fetch,a))
(r/'sbir207-sites.json').write_text(json.dumps(res,indent=2)+'\n')
for x in res:print(x['id'],x['name'],x.get('status'),x.get('final_url'),x.get('text','')[:200])
