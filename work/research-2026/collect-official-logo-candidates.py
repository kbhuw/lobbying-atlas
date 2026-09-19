import sys
import json,pathlib,urllib.request,urllib.parse,concurrent.futures,datetime
from html.parser import HTMLParser
R=pathlib.Path(__file__).resolve().parent
class Assets(HTMLParser):
 def __init__(self):super().__init__();self.a=[]
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if t=='img' and 'logo' in ' '.join(str(v) for v in d.values()).lower():self.a.append({'kind':'logo','url':d.get('src') or d.get('data-src'),'alt':d.get('alt',''),'class':d.get('class','')})
  if t=='link' and 'icon' in d.get('rel','').lower():self.a.append({'kind':'site_icon','url':d.get('href'),'rel':d.get('rel')})
def run(x):
 try:
  req=urllib.request.Request(x['website'],headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=20) as r:html=r.read(3000000).decode('utf-8','replace');final=r.url
  h=Assets();h.feed(html);seen=set();a=[]
  for v in h.a:
   if not v['url']:continue
   u=urllib.parse.urljoin(final,v['url'])
   if not u.startswith('https://') or u in seen or any(w in u.lower() for w in ['default-favicon','wordpress-logo','wix-favicon','gravatar']):continue
   seen.add(u);a.append({**v,'url':u})
  return {**x,'fetched_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'page_url':final,'candidates':a[:15]}
 except Exception as e:return {**x,'error':str(e),'candidates':[]}
start=int(sys.argv[1]) if len(sys.argv)>1 else 0
limit=int(sys.argv[2]) if len(sys.argv)>2 else 24
output=R/f'official-root-logo-{start}-{start+limit}.json'
queue=json.load(open(R/'verified-root-logo-queue.json'))[start:start+limit]
out=[]
with concurrent.futures.ThreadPoolExecutor(4) as pool:
 for x in pool.map(run,queue):out.append(x);print(x['name'],len(x['candidates']),x.get('error',''),flush=True);output.write_text(json.dumps(out,indent=2))
