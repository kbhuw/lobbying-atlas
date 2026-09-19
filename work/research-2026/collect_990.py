"""Join IRS EIN identities to filed websites and missions; no name guessing."""
import json,gzip,pathlib,urllib.request,datetime,time,threading,concurrent.futures,html,re
from html.parser import HTMLParser
root=pathlib.Path('work/research-2026');out=root/'tax-return-evidence';out.mkdir(exist_ok=True)
lock=threading.Lock();next_request=0
class Fields(HTMLParser):
 def __init__(self):super().__init__();self.key=None;self.values={}
 def handle_starttag(self,t,a):
  d=dict(a);k=d.get('id','')
  if t=='span' and any('/'+v+'[' in k for v in ['WebsiteAddressTxt','MissionDesc','ActivityOrMissionDesc','EIN','BusinessNameLine1Txt','TaxYr']):self.key=k.split('/')[-1].split('[')[0] if k.split('/')[-1].split('[')[0] not in self.values else None
 def handle_endtag(self,t):
  if t=='span':self.key=None
 def handle_data(self,d):
  if self.key:self.values[self.key]=self.values.get(self.key,'')+d

def get(u):
 global next_request
 with lock:
  delay=max(0,next_request-time.monotonic());next_request=max(next_request,time.monotonic())+.65
 if delay:time.sleep(delay)
 r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'LobbyingAtlasResearch/1.0'}),timeout=18);b=r.read(3000000)
 return gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b

def run(item):
 id,p=item;ein=p['registry']['id'];dst=out/(id+'.json')
 if dst.exists():
  try:
   saved=json.loads(dst.read_text())
   if saved.get('parser_version')==2:return saved
  except (ValueError,OSError):pass
 result={'parser_version':2,'id':id,'ein':ein,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'unavailable'}
 try:
  api='https://projects.propublica.org/nonprofits/api/v2/organizations/'+str(int(ein))+'.json';d=json.loads(get(api));org=d['organization'];oid=org.get('latest_object_id');result['organization_name']=org['name'];result['api_source']=api
  if oid:
   url='https://projects.propublica.org/nonprofits/full_text/'+oid+'/IRS990';parser=Fields();parser.feed(get(url).decode('utf-8','replace'));v=parser.values
   result.update(source_url=url,fields=v)
   if v.get('EIN') and re.sub(r'\D','',v['EIN']).zfill(9)!=ein.zfill(9):result['status']='identity_conflict'
   elif v.get('WebsiteAddressTxt'):
    raw=v['WebsiteAddressTxt'].strip();result['filed_website']=raw;result['status']='filing_website_found'
  else:result['reason']='No current electronic return located by API'
 except Exception as e:result['error']=type(e).__name__+': '+str(e).split('?')[0]
 temp=dst.with_suffix('.tmp');temp.write_text(json.dumps(result,ensure_ascii=False,indent=2));temp.replace(dst);return result
cs=json.load(gzip.open('lobbying-map/public/data/directory-v3.json.gz'))['companies'];profiles=json.load(open('work/organization-research/registry-profiles.json'));sample={c['id'] for c in json.load(open(root/'sample.json'))};ids={c['id'] for c in cs if c['years'].get('2026')};items=sorted([(k,v) for k,v in profiles.items() if k in ids and v['registry']['type']=='IRS'],key=lambda x:x[0] not in sample)
counts={};n=0
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(run,items):
  n+=1;counts[r['status']]=counts.get(r['status'],0)+1
  (root/'tax-progress.json').write_text(json.dumps({'processed':n,'total':len(items),'counts':counts,'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
  if n%25==0:print(n,counts,flush=True)
