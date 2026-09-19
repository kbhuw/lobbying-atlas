import json,requests,bs4,concurrent.futures,re,io
from pypdf import PdfReader
r='work/research-2026/';rows=json.load(open(r+'featured96-first-followup.json'))+json.load(open(r+'featured96-middle-followup.json'))
def f(d):
 u=d['official_url']
 try:
  z=requests.get(u,timeout=25);t='\n'.join(p.extract_text() or '' for p in PdfReader(io.BytesIO(z.content)).pages) if 'pdf' in z.headers.get('Content-Type','') else bs4.BeautifulSoup(z.text,'html.parser').get_text(' ',strip=True)
  snippets=[t[max(0,m.start()-100):m.end()+250] for m in re.finditer('United States|Union Pacific|Unified Patents|nonprofit|non-profit|Four Corners|United Airlines|100.00',t,re.I)][:12]
  return dict(id=d['id'],url=u,status=z.status_code,text=t[:400000],snippets=snippets)
 except Exception as e:return dict(id=d['id'],url=u,error=str(e))
out=list(concurrent.futures.ThreadPoolExecutor(6).map(f,rows));open(r+'featured96-extra-fetch.json','w').write(json.dumps(out,indent=2));print(json.dumps([{k:v for k,v in x.items() if k!='text'} for x in out],indent=2))
