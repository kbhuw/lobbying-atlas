import json,pathlib,urllib.request,concurrent.futures,re
from bs4 import BeautifulSoup
w=pathlib.Path('work/research-2026');d=json.loads((w/'reviewed.json').read_text());out=w/'public-evidence-sept12';out.mkdir(exist_ok=True)
rows=[dict(id=k,profile=v) for k,v in d.items() if v.get('review_outcome')=='partial' and v.get('ownership')=='Publicly traded' and any(s.get('label')=='Organization evidence' for s in v.get('sources',[]))]
(out/'before.json').write_text(json.dumps(rows,indent=2))
def run(r):
 v=r['profile'];s=next(s for s in v['sources'] if s.get('label')=='Organization evidence');z=dict(id=r['id'],name=v['name'],source=s)
 try:
  req=urllib.request.Request(s['url'],headers={'User-Agent':'Mozilla/5.0 public-record research'})
  with urllib.request.urlopen(req,timeout=18) as f:raw=f.read(5000000);z['resolved_url']=f.url
  if raw.startswith(b'%PDF'):raise ValueError('PDF requires separate extraction')
  soup=BeautifulSoup(raw,'html.parser')
  for t in soup(['script','style']):t.decompose()
  txt=soup.get_text(' ',strip=True);(out/(r['id']+'.txt')).write_text(txt)
  matches=list(re.finditer(r'NYSE|NASDAQ|Nasdaq|New York Stock Exchange|ticker|trading symbol',txt,re.I));z['snippets']=[txt[max(0,m.start()-160):m.end()+200] for m in matches[:8]];z['status']='fetched'
 except Exception as e:z.update(status='error',error=str(e))
 return z
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:result=list(ex.map(run,rows))
(out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
