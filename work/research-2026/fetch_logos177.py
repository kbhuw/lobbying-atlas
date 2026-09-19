import requests,json,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));ids=['637ee6da544718e8','bfda149345238558','61c5e79dec150ee9','8eb63bd96b889b00','c559f9dfd4462405','51d419e4454a4af3']
def f(i):
 u=p[i]['website'];out=dict(id=i,name=p[i]['name'],url=u)
 try:
  a=requests.get(u,timeout=12);path=r/f'featured177-{i}.html';path.write_text(a.text);s=BeautifulSoup(a.text,'html.parser');out.update(http_status=a.status_code,url=a.url,cache_path=str(path.resolve()),title=s.title.get_text() if s.title else '',candidates=[dict(alt=t.get('alt'),url=urljoin(a.url,t.get('src',''))) for t in s.find_all('img') if any(k in str(t).lower() for k in ['logo','wordmark',p[i]['name'].split()[0].lower()])][:8])
 except Exception as e:out.update(error=type(e).__name__)
 return out
with concurrent.futures.ThreadPoolExecutor(6) as ex:out=list(ex.map(f,ids))
(r/'featured177-logo-candidates.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
