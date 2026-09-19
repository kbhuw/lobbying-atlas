import csv,json,re,pathlib,zipfile,collections,xml.etree.ElementTree as ET
ROOT=pathlib.Path('work/research-2026'); p=json.loads((ROOT/'reviewed.json').read_text())
def norm(s):return re.sub(r'[^A-Z0-9]','',s.upper().replace('&','AND'))
cs={k:v for k,v in p.items() if v.get('ownership')=='Not applicable' and any(s.get('label','').startswith('IRS organization record') for s in v['sources'])}
eins={m.group(1) for v in cs.values() for s in v['sources'] if s.get('label','').startswith('IRS organization record') for m in [re.search(r'EIN (\d{9})',s['label'])] if m}
irs={};frequency=collections.Counter()
for f in pathlib.Path('work/organization-research/irs').glob('eo*.csv'):
 with f.open() as z:
  for r in csv.DictReader(z):
   frequency[(norm(r['NAME']),norm(r['CITY']),r['STATE'])]+=1
   if r['EIN'].zfill(9) in eins:irs[r['EIN'].zfill(9)]=r
zs={};accepted=[];deferred=[]
for k,v in cs.items():
 reasons=[];matches=[]
 for s in v['sources']:
  if s.get('label','').startswith('IRS organization record'):
   m=re.search(r'EIN (\d{9})',s['label'])
   if m and m.group(1) in irs:matches.append(irs[m.group(1)])
 if len(matches)!=1:reasons.append('IRS record not unique or absent')
 if re.search(r'government|municipal|public institution|tribal|state university',v.get('kind',''),re.I):reasons.append('Government classification requires individual assessment')
 if not reasons:
  r=matches[0];key=(norm(r['NAME']),norm(r['CITY']),r['STATE'])
  if r['STATUS']!='01' or int(r['SUBSECTION']) not in {3,4,5,6,7,8,9,10,12,13,14,15,19}:reasons.append('Status or subsection outside supported scope')
  if frequency[key]!=1:reasons.append('Multiple IRS organizations have the same name and location')
  if norm(v['name'])!=norm(r['NAME']):reasons.append('Profile and IRS legal name differ')
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
 else:accepted.append({'id':k,'name':v['name'],'irs':r,'disclosure':proof,'prior_outcome':v['review_outcome']})
for z,_ in zs.values():z.close()
o=ROOT/'irs-classification-links';o.mkdir(exist_ok=True);(o/'audit.json').write_text(json.dumps({'accepted':accepted,'deferred':deferred},indent=2)+'\n')
print('Candidates:',len(cs),'exact links:',len(accepted),'deferred:',len(deferred));print(collections.Counter(reason for r in deferred for reason in r['reasons']));print('Examples:',[(x['name'],x['irs']['SUBSECTION']) for x in accepted[:20]])
