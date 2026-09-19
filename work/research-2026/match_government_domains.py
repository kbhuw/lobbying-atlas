"""Generate evidence candidates, never reviewed profiles, from CISA's .gov registry."""
import csv,json,re,pathlib,sqlite3,sys,urllib.parse
r=pathlib.Path(__file__).resolve().parent
rows=json.load(open(sys.argv[1]));registry=list(csv.DictReader(open(r/'dotgov-current.csv')))
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def locality(s):
 s=re.sub(r'^city of\s+','',s,flags=re.I);s=re.split(r'[,()]',s)[0];return s.strip()
db=sqlite3.connect(r.parent/'organization-research/research.sqlite')
state_names="Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming|District of Columbia".split('|')
state_codes="AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split()
state_map=dict(zip([x.lower() for x in state_names],state_codes))
out={}
for v in rows:
 states=set()
 for source in v.get('profile',{}).get('sources',[]):
  m=re.search(r'/clients/(\d+)',source['url'])
  if m:
   z=db.execute('select state from lda_clients where id=?',(int(m[1]),)).fetchone()
   if z and z[0]:states.add(state_map.get(z[0].lower(),z[0].upper()))
 for name,code in sorted(state_map.items(),key=lambda z:-len(z[0])):
  if re.search(r'(?:,|\s|\()'+re.escape(name)+r'\)?$',v['name'],re.I):states.add(code);break
 if not states:
  m=re.search(r'(?:,|\s)([A-Z]{2})$',v['name'])
  if m and m[1] in state_codes:states.add(m[1])
 label=locality(v['name']);candidates=[]
 for g in registry:
  if g['Domain type']!='City':continue
  if states and g['State'] not in states:continue
  city=g['City'];name=g['Organization name']
  if norm(label)==norm(city) or norm(v['name'])==norm(name) or norm(label).startswith(norm(city)) and len(norm(label))-len(norm(city))<=2:
   candidates.append({k:g[k] for k in ['Domain name','Domain type','Organization name','City','State']})
 out[v['id']]={'name':v['name'],'filing_states':sorted(states),'candidates':candidates,'status':'candidate_only'}
p=pathlib.Path(sys.argv[2]);p.write_text(json.dumps(out,indent=2)+'\n');print(sum(bool(v['candidates']) for v in out.values()),'of',len(out),'have CISA candidates; individual identity and website checks still required')
