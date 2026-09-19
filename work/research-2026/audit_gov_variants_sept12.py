import csv,json,re,pathlib,zipfile,collections,xml.etree.ElementTree as ET
ROOT=pathlib.Path('work/research-2026'); p=json.loads((ROOT/'reviewed.json').read_text())
def norm(s):return re.sub(r'[^A-Z0-9]','',s.upper().replace('&','AND'))
cs={k:v for k,v in p.items() if v.get('review_outcome')=='partial' and v.get('ownership')=='Government body'}
from urllib.parse import urlparse
gov=list(csv.DictReader((ROOT/'gov-registry-sept12/current-full.csv').open()))
bydomain=collections.defaultdict(list)
for r in gov:bydomain[r['Domain name'].lower()].append(r)
zs={};accepted=[];deferred=[]
for k,v in cs.items():
 reasons=[];matches=[]
 domain=urlparse(v.get('website','')).netloc.lower().removeprefix('www.')
 matches=bydomain.get(domain,[])
 if len(matches)!=1:reasons.append('No unique current domain registration')
 if not reasons:
  r=matches[0];key=(norm(r['Organization name']),norm(r['City']),r['State'])
  if r['Suborganization name'].strip() not in {'','(blank)'}:reasons.append('Department or program domain requires review')

  proof=None
  if not reasons:
   for s in v['sources']:
    if not s['url'].endswith('.zip'):continue
    members=re.findall(r'(\d+\.xml)',s.get('label','')+' '+s.get('claim',''))
    if not members:continue
    f=pathlib.Path('work/federal-directory/raw')/s['url'].split('/')[-1]
    if not f.exists():continue
    if str(f) not in zs:
     z=zipfile.ZipFile(f);zs[str(f)]=(z,{pathlib.PurePosixPath(n).name:n for n in z.namelist()})
    z,names=zs[str(f)]
    for m in set(members):
     if m not in names:continue
     try:doc=ET.fromstring(z.read(names[m]))
     except ET.ParseError:continue
     def val(tag):return (doc.findtext(tag) or '').strip()
     name,city,state=val('clientName'),val('clientCity'),val('clientState')
     if (norm(name),norm(city),state)==key:
      proof={'archive':str(f),'member':names[m],'client_name':name,'city':city,'state':state,'source_url':s['url']};break
    if proof:break
   if not proof:reasons.append('No exact name and location link in cited raw disclosure XML')
 if reasons:deferred.append({'id':k,'name':v['name'],'reasons':reasons})
 else:accepted.append({'id':k,'name':v['name'],'registry':r,'disclosure':proof,'prior_outcome':v['review_outcome']})
for z,_ in zs.values():z.close()
o=ROOT/'gov-name-variants-sept12';o.mkdir(exist_ok=True);(o/'audit.json').write_text(json.dumps({'accepted':accepted,'deferred':deferred},indent=2)+'\n')
print('Candidates:',len(cs),'exact links:',len(accepted),'deferred:',len(deferred));print(collections.Counter(reason for r in deferred for reason in r['reasons']));print('Examples:',[(x['name'],x['registry']['Domain type']) for x in accepted[:20]])
