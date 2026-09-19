import requests,json,pathlib,concurrent.futures
from bs4 import BeautifulSoup
urls=['https://lda.gov/filings/public/filing/161b154b-f1bb-4e5e-adf7-8ae21b9f6b1c/print/','https://lda.gov/filings/public/filing/d0d45c40-65d5-4b33-bf03-49bc5133081a/print/','https://lda.gov/api/v1/clients/56104/?format=json','https://www.cx2.com/privacy','https://www.cx2.com/']
def f(u):
 try:
  z=requests.get(u,timeout=25);b=BeautifulSoup(z.text,'html.parser');return dict(url=u,status=z.status_code,text=b.get_text(' ',strip=True),images=[dict(src=i.get('src'),alt=i.get('alt')) for i in b.find_all('img')])
 except Exception as e:return dict(url=u,error=str(e))
a=list(concurrent.futures.ThreadPoolExecutor(5).map(f,urls));pathlib.Path('work/research-2026/featured105-root-fetch.json').write_text(json.dumps(a,indent=2))
for z in a:print(z['url'],z.get('status'),z.get('text','')[:2200],z.get('images',[])[:5])
