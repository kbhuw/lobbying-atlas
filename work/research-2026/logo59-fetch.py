import requests,concurrent.futures,json
from bs4 import BeautifulSoup
from pathlib import Path
urls=['https://firehawkaerospace.com/','https://fireflyspace.com/','https://www.firstkeyhomes.com/','https://www.fisherinvestments.com/en-us']
def f(u):
 try:
  r=requests.get(u,timeout=20);s=BeautifulSoup(r.text,'html.parser');return dict(url=u,status=r.status_code,images=[dict(src=e.get('src'),alt=e.get('alt')) for e in s.select('img') if 'logo' in str(e).lower()][:15])
 except Exception as e:return dict(url=u,error=str(e))
x=list(concurrent.futures.ThreadPoolExecutor(4).map(f,urls));Path('work/research-2026/logo59-candidates.json').write_text(json.dumps(x,indent=2));print(json.dumps(x,indent=2))
