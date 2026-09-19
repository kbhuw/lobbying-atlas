import requests,json,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));ids=['4dcb3fae7e3746c6','bacf49a629b5b072','cdff23807d2964b1','1abd7999f38e0640','f77f39918fef04d6','f54164f1192e877f']
def f(i):
 u=p[i]['website'];out=dict(id=i,name=p[i]['name'],url=u)
 try:
  a=requests.get(u,timeout=12);path=r/f'featured179-{i}.html';path.write_text(a.text);s=BeautifulSoup(a.text,'html.parser');out.update(http_status=a.status_code,url=a.url,cache_path=str(path.resolve()),title=s.title.get_text() if s.title else '',candidates=[dict(alt=t.get('alt'),url=urljoin(a.url,t.get('src',''))) for t in s.find_all('img') if any(k in str(t).lower() for k in ['logo','wordmark',p[i]['name'].split()[0].lower()])][:8])
 except Exception as e:out.update(error=type(e).__name__)
 return out
with concurrent.futures.ThreadPoolExecutor(6) as ex:out=list(ex.map(f,ids))
(r/'featured179-logo-candidates.json').write_text(json.dumps(out,indent=2));print(json.dumps([{**v,'candidates':[{**a,'url':a['url'][:250]} for a in v.get('candidates',[])]} for v in out],indent=2))
