import requests,json,pathlib,concurrent.futures
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));rows=json.load(open(r/'featured113-input.json'))[2:5]
def get(v):
 u=p[v['id']]['sources'][0]['url'];q=requests.get(u,timeout=20);(r/('featured113-'+v['id']+'.html')).write_text(q.text);s=BeautifulSoup(q.text,'html.parser').get_text(' ',strip=True);return dict(id=v['id'],url=u,status=q.status_code,text=s[:1900])
a=list(concurrent.futures.ThreadPoolExecutor(3).map(get,rows));(r/'featured113-originals.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
