import requests,json,pathlib,concurrent.futures
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));ids=['9eeab96f1385f7b7','b9221b5fcb39b8ce','2add3941d22f2b59','845079aaa42780aa','8a2e6d6dd4d7d840','da69aa23f81788bb','516bd55c85531ef5','7a2b6fc649b88c84','db5e15d515e7daf2']
def get(i):
 v=p[i];u=v['website']
 try:
  x=requests.get(u,timeout=12);(r/f'featured192-{i}.html').write_bytes(x.content);s=BeautifulSoup(x.text,'html.parser')
  for t in s(['script','style','nav','header']):t.decompose()
  text=s.get_text(' ',strip=True);return dict(id=i,name=v['name'],url=x.url,status=x.status_code,text=text)
 except Exception as e:return dict(id=i,name=v['name'],error=str(e))
a=list(concurrent.futures.ThreadPoolExecutor(6).map(get,ids));(r/'featured192-evidence.json').write_text(json.dumps(a,indent=2))
for x in a:print(json.dumps({**x,'text':x.get('text','')[:2600]},ensure_ascii=False))
