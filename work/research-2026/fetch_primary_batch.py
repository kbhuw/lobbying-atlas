import requests,bs4,json,concurrent.futures,sys,io,pathlib
from pypdf import PdfReader
n=sys.argv[1];r=pathlib.Path('work/research-2026');rows=sum([json.load(open(r/f'featured{n}-{s}.json')) for s in ['first10','middle10']],[])
def fetch(d):
 u=d['official_url'];o=dict(id=d['id'],url=u)
 try:
  res=requests.get(u,timeout=25);o.update(status=res.status_code,final_url=res.url)
  t=' '.join(p.extract_text() or '' for p in PdfReader(io.BytesIO(res.content)).pages) if res.content.startswith(b'%PDF') else bs4.BeautifulSoup(res.text,'html.parser').get_text(' ',strip=True)
  o['text']=t[:180000]
 except Exception as e:o['error']=str(e)
 return o
out=list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(fetch,rows));(r/f'featured{n}-primary-fetch.json').write_text(json.dumps(out,indent=2)+'\n');print([(x['id'],x.get('status'),len(x.get('text','')),x.get('error','')) for x in out])
