import json,pathlib,requests,concurrent.futures
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');d=r/'verified-sites132-root-cache';d.mkdir(exist_ok=True)
x=json.load(open(r/'verified-sites132-root-input.json'))
def f(x):
 u=x['profile']['website']
 try:
  a=requests.get(u,timeout=20);s=BeautifulSoup(a.content,'html.parser')
  for t in s(['script','style','noscript']):t.decompose()
  text=s.get_text(' ',strip=True);(d/(x['id']+'.txt')).write_text(text);(d/(x['id']+'.html')).write_bytes(a.content)
  return dict(id=x['id'],name=x['profile']['name'],url=u,final_url=a.url,status=a.status_code,text=text[:1900],links=[{'label':l.get_text(' ',strip=True),'url':l.get('href')} for l in s.find_all('a',href=True) if any(w in l.get_text(' ',strip=True).lower() for w in ['about','mission','history','who we'])][:8])
 except Exception as e:return dict(id=x['id'],url=u,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:y=list(ex.map(f,x))
(r/'verified-sites132-root-fetch.json').write_text(json.dumps(y,indent=2));print(json.dumps(y))
