import json,pathlib,re,concurrent.futures
from html.parser import HTMLParser
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round92-input.json'));exec((r/'check_round92_incremental.py').read_text().split('p=json.load(open(root/')[0])
class Images(HTMLParser):
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='img':
   u=d.get('data-src') or d.get('src','');alt=d.get('alt','')
   if 'logo' in str(d).lower() or len(self.items)<3:self.items.append((u,alt))
def one(i):
 c=json.load(open(r/f"website-cache/{rows[i]['id']}.json"));u=c['requested_url']
 try:
  _,_,b=get(u);s=b.decode('utf8','replace');p=Images();p.items=[];p.feed(s);v={'index':i,'url':u,'images':p.items[:25],'css_assets':list(dict.fromkeys(re.findall(r'[^\s\"\'<>]*logo[^\s\"\'<>]*\.(?:svg|png)',s,re.I)))[:15]};return v
 except Exception as e:return {'index':i,'error':str(e)}
v=list(concurrent.futures.ThreadPoolExecutor(6).map(one,[7,42,55,60,81]));(r/'round92-extra-assets.json').write_text(json.dumps(v,indent=2)+'\n')
for x in v:print(json.dumps(x))
