import requests,concurrent.futures,json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
urls=['https://www.metmuseum.org/','https://www.mta.info/','https://mission22.com/','https://msu.edu/','https://www.nrmchospital.org/','https://www2.miamination.com/']
def scan(u):
 try:
  r=requests.get(u,timeout=25);s=BeautifulSoup(r.text,'html.parser');a=[]
  for x in s.find_all(['img','source']):
   st=str(x)
   if 'logo' in st.lower():a.append({'src':urljoin(r.url,x.get('src') or x.get('data-src') or ''),'alt':x.get('alt'),'tag':st[:600]})
  return {'url':u,'status':r.status_code,'assets':a[:15]}
 except Exception as e:return {'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:out=list(ex.map(scan,urls))
json.dump(out,open('work/research-2026/logo75-candidates.json','w'),indent=2)
for x in out:print(json.dumps(x))
