import json,urllib.request,concurrent.futures,re,datetime
from html.parser import HTMLParser
from pathlib import Path
p=Path('work/research-2026');q=json.load(open(p/'nea-ownership-candidate-queue.json'));urls=sorted({u for x in q for u in x['candidate_investor_urls']})
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[];self.links=[]
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t=='a':self.links.append(dict(a).get('href',''))
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.parts.append(s)
def get(u):
 a={'url':u,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(u,timeout=20) as r:b=r.read().decode();a['http_status']=r.status
  h=Parser();h.feed(b);a['text']=' '.join(' '.join(h.parts).split());a['external_links']=[x for x in h.links if x.startswith('http') and not any(y in x for y in ['nea.com','linkedin.com','twitter.com','facebook.com','instagram.com'])];m=re.search(r'Company Status\s+(.{0,60})',a['text']);a['status_excerpt']=m.group(1) if m else None
 except Exception as e:a['error']=str(e)
 return a
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:a=list(ex.map(get,urls))
(p/'nea-ownership-pages.json').write_text(json.dumps(a,indent=2)+'\n')
for x in a:print(x['url'].rsplit('/',1)[-1],x.get('status_excerpt'),x.get('external_links'),x.get('error',''))
