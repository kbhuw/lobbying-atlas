import json,pathlib,urllib.request,urllib.parse,concurrent.futures,re
from bs4 import BeautifulSoup
b=pathlib.Path('work/research-2026/confirmed-logo-batch-sept12');o=b/'recovery';o.mkdir(exist_ok=True);q=[r for r in json.loads((b/'per-organization-results.json').read_text()) if r['result'] in {'needs_better_asset_extraction','wrong_or_ambiguous_logo_candidate'}]
def run(r):
 z=dict(r)
 try:
  with urllib.request.urlopen(urllib.request.Request(r['source'],headers={'User-Agent':'Mozilla/5.0'}),timeout=15) as f:raw=f.read(2500000);base=f.url
  (o/(r['id']+'.html')).write_bytes(raw);s=BeautifulSoup(raw,'html.parser');c=[]
  for i in s.find_all(['img','svg']):
   context=' '.join(str(p.get('class',''))+' '+str(p.get('id',''))+' '+p.name for p in [i]+list(i.parents)[:4]);label=str(i.get('alt',''))+' '+str(i.get('aria-label',''))
   if not re.search(r'logo|brand|header',context+' '+label+' '+str(i.attrs),re.I):continue
   if i.name=='svg':
    c.append({'inline_svg':True,'label':label,'context':context[:220]});continue
   src=next((i.get(a) for a in ['data-src','data-lazy-src','src'] if i.get(a) and not i.get(a).startswith('data:')),None)
   if src:c.append({'url':urllib.parse.urljoin(base,src),'label':label,'context':context[:220]})
  z.update(status='fetched',candidates=c[:25],resolved_url=base)
 except Exception as e:z.update(status='error',error=str(e))
 (o/(r['id']+'.json')).write_text(json.dumps(z,indent=2));return z
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:rr=list(ex.map(run,q))
(o/'results.json').write_text(json.dumps(rr,indent=2));print('Recovered',sum(r['status']=='fetched' for r in rr),'of',len(rr))
