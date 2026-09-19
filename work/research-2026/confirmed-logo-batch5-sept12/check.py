import pathlib,json,urllib.request,concurrent.futures,re
from bs4 import BeautifulSoup
b=pathlib.Path('work/research-2026/confirmed-logo-batch5-sept12');c=b/'websites';c.mkdir(exist_ok=True);q=json.loads((b/'website-queue.json').read_text())
def run(r):
 z=dict(r)
 try:
  with urllib.request.urlopen(urllib.request.Request(r['website'],headers={'User-Agent':'Mozilla/5.0'}),timeout=12) as f:raw=f.read(1800000);z['resolved_url']=f.url
  soup=BeautifulSoup(raw,'html.parser');z['title']=soup.title.get_text(' ',strip=True) if soup.title else '';candidates=[]
  for i in soup.find_all('img'):
   context=' '.join(str(p.get('class',''))+' '+str(p.get('id',''))+' '+p.name for p in [i]+list(i.parents)[:4]);label=str(i.get('alt',''));src=next((i.get(a) for a in ['data-src','data-lazy-src','src'] if i.get(a) and not i.get(a).startswith('data:')),None)
   if not src or not re.search(r'logo|brand',context+' '+label+' '+src,re.I):continue
   score=10+30*bool(re.search(r'header|navbar-brand|site-logo|logo-header|site-branding',context,re.I))-50*bool(re.search(r'partner|sponsor|diamond_member|social',context+' '+label+' '+src,re.I))
   candidates.append(dict(src=src,alt=label,score=score,context=context[:200]))
  z['logo_candidates']=sorted(candidates,key=lambda c:c['score'],reverse=True)[:8]
  (c/(r['id']+'.html')).write_bytes(raw)
  for t in soup(['script','style']):t.decompose()
  txt=soup.get_text(' ',strip=True);(c/(r['id']+'.txt')).write_text(txt);term=re.sub(r'\b(incorporated|corporation|corp|inc|plc|limited|ltd)\b','',r['name'],flags=re.I).strip(' .,');n=txt.lower().find(term.lower());z['name_context']=txt[max(0,n-100):n+len(term)+230] if n>=0 else '';z['status']='fetched'
 except Exception as e:z.update(status='error',error=str(e))
 return z
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:r=list(ex.map(run,q))
(b/'website-results.json').write_text(json.dumps(r,indent=2));print('Checked',len(r),'Fetched',sum(z['status']=='fetched' for z in r))
