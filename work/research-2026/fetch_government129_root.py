import requests,json,pathlib,concurrent.futures
from bs4 import BeautifulSoup
from urllib.parse import urljoin
p=pathlib.Path('work/research-2026/government129-root-cache');p.mkdir(exist_ok=True)
urls=['https://www.fortworthtexas.gov/','https://www.okc.gov/','https://www.usoma.us/en','https://www.tonopah-solar.com/']
def f(u):
 try:
  r=requests.get(u,timeout=25);s=BeautifulSoup(r.content,'html.parser');key=u.split('/')[2];(p/(key+'.html')).write_bytes(r.content);(p/(key+'.txt')).write_text(s.get_text(' ',strip=True));imgs=[{'url':urljoin(r.url,i.get('src','')),'alt':i.get('alt','')} for i in s.find_all('img') if 'logo' in str(i).lower() or 'seal' in str(i).lower()];return dict(url=u,final_url=r.url,status=r.status_code,title=str(s.title),images=imgs)
 except Exception as e:return dict(url=u,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:x=list(ex.map(f,urls))
pathlib.Path('work/research-2026/government129-root-fetch.json').write_text(json.dumps(x,indent=2));print(json.dumps(x))
