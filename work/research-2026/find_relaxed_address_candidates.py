import json,pathlib,re,unicodedata
root=pathlib.Path(__file__).resolve().parents[2];base=root/'work/research-2026';p=json.load(open(base/'reviewed.json'));qs=json.load(open(base/'remaining-work-by-evidence.json'))['queues'];regs={x['id']:x for x in json.load(open(base/'registration-evidence-queue.json'))};out=[]
def norm(s):
 s=unicodedata.normalize('NFKD',s.upper());s=''.join(c for c in s if not unicodedata.combining(c));s=re.sub(r'[^A-Z0-9 ]',' ',s)
 for a,b in [('STREET','ST'),('AVENUE','AVE'),('ROAD','RD'),('BOULEVARD','BLVD'),('SUITE','STE'),('PARKWAY','PKWY'),('DRIVE','DR'),('NORTHWEST','NW'),('SOUTHWEST','SW'),('SOUTHEAST','SE'),('NORTHEAST','NE'),('NORTH','N'),('SOUTH','S'),('EAST','E'),('WEST','W'),('SAINT','ST'),('MOUNT','MT')]:s=re.sub(r'\b'+a+r'\b',b,s)
 s=re.sub(r'\bP O BOX\b','PO BOX',s);return ' '.join(s.split())
def contains(text,phrase):return re.search(r'(?<![A-Z0-9])'+re.escape(phrase)+r'(?![A-Z0-9])',text)
for x in qs['find_new_address_or_legal_evidence']:
 if p[x['id']]['review_outcome']=='confirmed':continue
 d=json.load(open(root/x['cache']));matches=[]
 for e in regs[x['id']]['evidence']:
  street=re.split(r',|\b(?:suite|ste\.?|floor|fl\.?|unit|room|bldg\.?|building)\b|#',e['address'],flags=re.I)[0];street=norm(street);city=norm(e['city'])
  if len(street)<7 or len(city)<3 or not re.match(r'^(\d+\b|PO BOX\b)',street):continue
  for page in d['pages']:
   if page.get('status')!=200:continue
   t=norm(page.get('text',''));a=contains(t,street)
   if a and contains(t,city):matches.append({'page_url':page['url'],'street_without_unit':street,'registration':e,'context':t[max(0,a.start()-120):a.end()+350],'method':'Candidate only: normalized street without suite and city found. Requires identity/context review; no automatic confirmation.'})
 if matches:out.append({'id':x['id'],'name':p[x['id']]['name'],'cache':x['cache'],'matches':matches})
(base/'relaxed-address-candidates42.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print(len(out),'new address candidates; no profiles changed')
