import requests,concurrent.futures,json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
urls=['https://www.ecolab.com/','https://www.lilly.com/','https://www.emirates.com/','https://investor.kodak.com/']
def f(u):
 try:
  r=requests.get(u,timeout=20);s=BeautifulSoup(r.text,'html.parser');a=[]
  for el in s.select('img'):
   if 'logo' in str(el).lower():a.append({k:el.get(k) for k in ['src','alt','class']})
  return dict(url=u,status=r.status_code,images=a[:15])
 except Exception as e:return dict(url=u,error=str(e))
x=list(concurrent.futures.ThreadPoolExecutor(4).map(f,urls));Path('work/research-2026/featured57-logo-candidates.json').write_text(json.dumps(x,indent=2));print(json.dumps(x,indent=2))
