import requests,json,pathlib,re,concurrent.futures
from bs4 import BeautifulSoup
from urllib.parse import urljoin
p=pathlib.Path('work/research-2026/government129-root-cache');jobs=[]
for host in ['www.okc.gov','www.fortworthtexas.gov','www.usoma.us']:
 s=BeautifulSoup((p/(host+'.html')).read_text(),'html.parser')
 for l in s.find_all('link',rel='stylesheet'):
  if 'client_style' in l['href'] or host=='www.usoma.us':jobs.append((host,urljoin('https://'+host,l['href'])))
 if host=='www.usoma.us':jobs.append((host,'https://www.usoma.us/assets/dist/site/asset/bundle.js?v=260830-223642'))
def f(job):
 host,u=job;r=requests.get(u,timeout=25);s=r.text;(p/(host+('.js' if 'bundle.js' in u else '.css'))).write_text(s);return {'host':host,'url':u,'status':r.status_code,'matches':re.findall(r'.{0,100}(?:header-site-logo|logo\.svg|logo-sticky|logo\.png).{0,230}',s)[:8]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:x=list(ex.map(f,jobs))
(p/'asset-discovery.json').write_text(json.dumps(x,indent=2));print(json.dumps(x))
