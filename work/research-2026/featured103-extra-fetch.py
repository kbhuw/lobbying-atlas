import requests,concurrent.futures,json,pathlib
from bs4 import BeautifulSoup
urls=['https://lda.gov/filings/public/filing/4b97cbd4-c7ab-496b-b66b-861a9a0abfb9/print/','https://lda.gov/filings/public/filing/27f91145-050d-4595-b23d-1709097801d1/print/','https://www.americangaming.org/about/','https://www.coaspire.com/news','https://www.clarios.com/privacy-policy/clarios-privacy-en']
def f(u):
 try:
  x=requests.get(u,timeout=25);b=BeautifulSoup(x.text,'html.parser');imgs=[dict(src=i.get('src'),alt=i.get('alt')) for i in b.find_all('img') if 'logo' in str(i).lower()];t=b.get_text(' ',strip=True);return dict(url=u,status=x.status_code,text=t,images=imgs)
 except Exception as e:return dict(url=u,error=str(e))
a=list(concurrent.futures.ThreadPoolExecutor(5).map(f,urls));pathlib.Path('work/research-2026/featured103-extra-fetch.json').write_text(json.dumps(a,indent=2))
for x in a:
 print(x['url'],x.get('status'),x.get('error',''));t=x.get('text','');print(t[:5000] if 'lda.gov' in x['url'] else str(x.get('images'))[:2000])
