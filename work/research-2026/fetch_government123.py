import json,pathlib,requests,concurrent.futures,re
from bs4 import BeautifulSoup
p=pathlib.Path('work/research-2026');d=p/'government123-root-cache';d.mkdir(exist_ok=True)
xs=json.load(open(p/'government119-input.json'))[250:260]
def f(x):
 s=x['primary_sources'][0];u=s['url']
 try:
  a=requests.get(u,timeout=25);t=(' '.join(pg.extract_text() or '' for pg in __import__('pypdf').PdfReader(__import__('io').BytesIO(a.content)).pages) if a.content.startswith(b'%PDF') else BeautifulSoup(a.content,'html.parser').get_text(' ',strip=True));(d/(x['id']+'.txt')).write_text(t)
  pat={'fb4f193197dde185':'Google Client Services','de18c106fae2b481':'Cyclo','09111778693f8980':'Energy Fuels Resources'}.get(x['id'],x['profile']['name'].split(' (')[0]);pat=re.sub(r'[^a-zA-Z ]','',pat).split();pattern=r'\W*'.join(pat[:3]);matches=list(re.finditer(pattern,t,re.I))
  return dict(id=x['id'],name=x['profile']['name'],url=u,status=a.status_code,excerpts=[t[max(0,m.start()-120):m.end()+450] for m in matches[:3]])
 except Exception as e:return dict(id=x['id'],error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:out=list(ex.map(f,xs))
(p/'government123-root-fetch.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
