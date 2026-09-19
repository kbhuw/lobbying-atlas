import requests,concurrent.futures,json,pathlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
r=pathlib.Path('work/research-2026')
def run(u):
 try:
  q=requests.get(u,timeout=20);s=BeautifulSoup(q.text,'html.parser');a=[dict(url=urljoin(q.url,x.get('src','')),alt=x.get('alt','')) for x in s.select('img') if 'logo' in str(x).lower()];return dict(url=u,status=q.status_code,assets=a[:12])
 except Exception as e:return dict(url=u,error=str(e))
urls=['https://www.azdel.com/','https://www.hanwhaenergyusa.com/','https://www.tidesmedical.com/']
a=list(concurrent.futures.ThreadPoolExecutor(5).map(run,urls));(r/'featured112-assets.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
