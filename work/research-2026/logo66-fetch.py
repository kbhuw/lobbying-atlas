import requests,concurrent.futures,json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
urls=['https://www.hpe.com/us/en/newsroom/media-assets.html','https://corporate.homedepot.com/','https://www.hoffman-dev.com/','https://hoeckerenergy.com/']
def get(u):
 try:
  r=requests.get(u,timeout=20);s=BeautifulSoup(r.text,'html.parser');a=[]
  for t in s.find_all(['img','link','a']):
   v=t.get('src') or t.get('href') or ''; z=str(t)
   if 'logo' in z.lower() or 'icon' in z.lower():a.append({'url':urljoin(r.url,v),'tag':z[:500]})
  return {'source':u,'status':r.status_code,'assets':a[:25]}
 except Exception as e:return {'source':u,'error':str(e)}
x=list(concurrent.futures.ThreadPoolExecutor(4).map(get,urls));Path('work/research-2026/logo66-candidates.json').write_text(json.dumps(x,indent=2));print(json.dumps(x))
