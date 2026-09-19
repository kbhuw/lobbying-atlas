import json,pathlib,urllib.request,urllib.parse,concurrent.futures,datetime,re,html
from html.parser import HTMLParser
root=pathlib.Path('work/research-2026');cache=root/'website-cache';cache.mkdir(exist_ok=True)
class Page(HTMLParser):
 def __init__(self,name):super().__init__();self.name_tokens=[t for t in re.findall('[a-z0-9]+',name.lower()) if len(t)>3 and t not in ['company','corporation','association','global','national','american','group','international']];self.candidates=[];self.text=[];self.skip=0;self.jsonld=False;self.ld=[]
 def handle_starttag(self,t,attrs):
  a={k:(v or "") for k,v in attrs}
  if t in ['script','style']:self.skip+=1
  if t=='script' and a.get('type')=='application/ld+json':self.jsonld=True
  if t=='img' and re.search('logo', ' '.join(a.get(k,'') for k in ['alt','class','id','src']),re.I):
   if a.get('src') and any(t in (a.get('alt','')+' '+urllib.parse.urlparse(a['src']).path.rsplit('/',1)[-1]).lower() for t in self.name_tokens):self.candidates.append((0,a['src'],'logo'))
  if t=='link' and 'icon' in a.get('rel','').lower() and a.get('href'):self.candidates.append((2,a['href'],'site_icon'))
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
  if t=='script':self.jsonld=False
 def handle_data(self,d):
  if self.jsonld:self.ld.append(d)
  if not self.skip and d.strip():self.text.append(d.strip())
def get(u,maxbytes=2000000):
 req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (compatible; LobbyingAtlasResearch/1.0)'})
 with urllib.request.urlopen(req,timeout=12) as r:
  final=r.geturl();mime=r.headers.get('Content-Type','');encoding=r.headers.get('Content-Encoding','').lower();data=r.read(maxbytes)
 if encoding=='gzip' or data[:2]==b'\x1f\x8b':
  import gzip
  data=gzip.decompress(data)
 elif encoding=='deflate':
  import zlib
  data=zlib.decompress(data)
 elif encoding=='br':
  import subprocess
  data=subprocess.run(['node','-e',"const z=require('node:zlib');const fs=require('node:fs');process.stdout.write(z.brotliDecompressSync(fs.readFileSync(0)));"],input=data,capture_output=True,check=True,timeout=12).stdout
 return final,mime,data[:maxbytes]
def one(item):
 id,p=item;u=p['website'];out={'id':id,'requested_url':u,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  final,mime,b=get(u);out.update(final_url=final,http_status=200);page=Page(p['name']);page.feed(b.decode('utf-8','replace'));out['text']=' '.join(page.text)[:16000]
  for raw in page.ld:
   for m in re.findall(r'"logo"\s*:\s*"([^"\n]+)"',raw):page.candidates.append((-1,m,'logo'))
   for m in re.findall(r'"logo"\s*:\s*\{[^}]*?"url"\s*:\s*"([^"\n]+)"',raw):page.candidates.append((-1,m,'logo'))
  out['asset_candidates']=[]
  for _,asset,kind in sorted(page.candidates)[:6]:
   asset=urllib.parse.urljoin(final,html.unescape(asset).replace('\\/','/'))
   if 'static.parastorage.com/client/pfavico.ico' in asset or '/core/misc/favicon.ico' in asset:continue
   if re.search(r'(facebook|linkedin|twitter|youtube|instagram|pinterest|tiktok)',urllib.parse.urlparse(asset).path.rsplit('/',1)[-1],re.I):continue
   if 'favicon' in asset.lower() or 'apple-touch-icon' in asset.lower():kind='site_icon'
   if not asset.startswith('https://') or asset in [x['url'] for x in out['asset_candidates']]:continue
   out['asset_candidates'].append({'url':asset,'kind':kind})
   if 'logo_url' not in out:
    try:
     dest,typ,img=get(asset,1000000)
     if typ.startswith('image/') and len(img)>80:out.update(logo_url=asset,logo_kind=kind,logo_source_url=final,logo_http_status=200,logo_content_type=typ)
    except Exception:pass
 except Exception as e:out['error']=str(e)
 (cache/(id+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2));return id,out

picks={'5ca555baae6f6562':1,'bbbe4af96e3a3e1f':1,'39f205d843979043':1,'c21a3097170b30ad':1,'e6c2ff067fa71b4f':2,'90c8d0e5deea1986':1,'edddefb3697ae3b2':2,'ccfc61e7c7170cb5':1,'5f5b877d8f31effe':0,'6e5047e48521e474':0,'651e184395f4649b':1,'cdf335ed4b78f4a4':2,'01647984247c304c':1}
audit=[];ex=json.load(open(root/'dotgov/branding-exclusions.json'))
for k,i in picks.items():
 f=cache/(k+'.json');v=json.load(open(f));a=v['asset_candidates'][i]
 try:
  dest,typ,img=get(a['url'],1000000);assert typ.startswith('image/') and len(img)>80
  v.update(logo_url=a['url'],logo_kind=a['kind'],logo_content_type=typ,logo_http_status=200,logo_source_url=v['final_url']);f.write_text(json.dumps(v,indent=2)+'\n');ex.pop(k,None);audit.append({'id':k,'selected':a,'http_status':200})
 except Exception as e:audit.append({'id':k,'error':str(e)})
(root/'dotgov/branding-exclusions.json').write_text(json.dumps(ex,indent=2)+'\n');(root/'dotgov/branding-repairs.json').write_text(json.dumps(audit,indent=2)+'\n');print(len(audit),'checked')
