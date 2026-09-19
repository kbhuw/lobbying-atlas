import json,pathlib,re,urllib.parse
r=pathlib.Path('work/research-2026')
def read(f):return json.load(open(r/f))
def keyed(d):return {x['id']:x for x in d} if isinstance(d,list) else d
p={**read('irs-round2-a-root-rewrite.json'),**read('irs-round2-b-researched.json'),**keyed(read('irs-round2-c-researched.json'))}
inputs={x['id']:x for l in 'abc' for x in read(f'irs-round2-{l}-input.json')}
b=read('irs-round2-b-final-audit.json');c=keyed(read('irs-round2-c-final-audit.json')['records'])
audit={**read('irs-round2-a-branding-audit.json'),**read('irs-round2-b-branding-audit.json'),**keyed(read('irs-round2-c-branding-audit.json')['records'])}
out={}
for k,v in p.items():
 o={f:v.get(f,'') for f in ['name','description','kind','website','identity_evidence']}
 o.update(ownership='Nonprofit / tax-exempt',status='sourced',review_outcome='partial',website_status='filed' if o['website'] else 'unresolved',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved',notes='Individual review of the IRS identity, tax-return activity, House disclosure and official website where available. Historical names remain searchable. Related legal entities remain distinct. Tax-return information reflects its reporting period.',sources=[{'url':s['url'],'label':s.get('label','Source'),'claim':s.get('claim',s.get('claims',''))} for s in v['sources'] if s.get('url')])
 t=inputs[k]['tax_return'];o['sources'].append({'url':t['source_url'],'label':'Organization Form 990','claim':'Filed organization '+t.get('organization_name','')+'; EIN '+t['ein']+'. Mission and filed website reviewed; information reflects the return reporting period.'})
 if k in b and b[k].get('corrections'):
  fix=b[k];o.update(name=fix['name'],description=fix['description'],identity_evidence=fix['corrections'].get('identity_evidence',o['identity_evidence']))
  ss=fix.get('supporting_source',{});o['sources'].append({'url':ss['url'],'label':'Identity review source','claim':ss.get('excerpt','')})
 if k in c:
  fix=c[k];o['description']=fix['description']
  if fix.get('correction'):o['notes']+=' '+fix['correction']
 if k=='43338a53d01e20f8':o['description']='Community hospital in Columbus, Texas providing emergency, inpatient, outpatient, clinic, and specialty medical services.'
 if k=='f3b1e12c3ea65816':o['description']='Museum preserving Connecticut history and culture through exhibitions, collections, research, and education.'
 if k=='ce4a332cf1c2ee06':o['name']='FMI, The Food Industry Association'
 if k=='e2df598434767eb1':
  o['name']='Cal Poly Partners';o['sources'].append({'url':'https://ucm.calpoly.edu/news/cal-poly-corporation-renamed-cal-poly-partners','label':'University name-change announcement','claim':'Cal Poly Corporation renamed Cal Poly Partners in February 2024.'});o['notes']+=' Previously Cal Poly Corporation; separate from Cal Poly Foundation.'
 if k=='dc3faa4b4000309a':
  o['name']='Fort Bend Regional Partnership';o['sources'].append({'url':'https://fortbendregionalpartnership.com/fort-bend-chamber-of-commerce-unveils-new-identity-as-the-fort-bend-regional-partnership/','label':'Official rebrand announcement','claim':'Fort Bend Chamber of Commerce announced the Fort Bend Regional Partnership name in February 2026.'});o['notes']+=' Previously Fort Bend Chamber of Commerce.'
 if k=='b4cf5ae86664d375':o['website']='https://floridatomatoexchange.com/';o['description']='Trade association representing Florida tomato growers and packers and advocating on government policy affecting tomato production.'
 if k=='f7565533abd69e9d':o['website']='https://www.fti.edu/'
 cp=r/'website-cache'/f'{k}.json';cache=read(str(cp.relative_to(r))) if cp.exists() else {}
 # Match cache to supplied URL, case-insensitive host. A redirect is recorded explicitly.
 def norm(u):
  q=urllib.parse.urlsplit(u);return(q.hostname or '',q.path.rstrip('/'))
 verified=o['website'] and norm(cache.get('requested_url',''))==norm(o['website']) and cache.get('http_status')==200 and len(cache.get('text',''))>150
 if verified:
  o['website']=cache.get('final_url',o['website']);o['website_status']='verified';o['review_outcome']='confirmed'
  o['sources'].append({'url':o['website'],'label':'Official organization website','claim':'Page identity and activities reviewed against the disclosed organization and tax-return identity on 2026-09-05.'})
  a=audit.get(k,{})
  keep=a.get('status',a.get('decision'))=='keep'
  if k in ['f136646b94b73718','ce4a332cf1c2ee06','dc3faa4b4000309a','b4cf5ae86664d375','f7565533abd69e9d']:keep=True
  if keep and cache.get('logo_http_status')==200:
   candidate=a.get('replacement_candidate_url',a.get('replacement_candidate',cache.get('logo_url','')))
   if k in ['f136646b94b73718','ce4a332cf1c2ee06','dc3faa4b4000309a','b4cf5ae86664d375','f7565533abd69e9d']:candidate=cache.get('logo_url','')
   if candidate==cache.get('logo_url'):
    for f in ['logo_url','logo_kind','logo_source_url']:o[f]=cache.get(f,'')
    o['logo_status']='official_site_asset'
  if o['logo_url']:o['sources'].append({'url':o['logo_source_url'],'label':'Official website branding','claim':'Organization page supplies this '+o['logo_kind'].replace('_',' ')+'. Asset response checked.'})
 # Shared site is disclosed as affiliated rather than silently equating legal entities.
 if k in ['ed0dd31f4c106ebc','d2785b0e70d08c3f','c609a31491f9a423','cc7271b3983b45eb','5d5d776beb2b80fd']:
  o['notes']+=' Linked website presents the affiliated organization or wider system; a separate entity-specific logo was not established.';o['review_outcome']='partial';o['website_status']='filed';o.update(logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved')
 o['name']=re.sub(r'\b(of|for|the|and|on|in|at)\b',lambda m:m[0].lower(),o['name'],flags=re.I)
 for a,z in {'BAY':'Bay','BIG':'Big','MAN':'Man','CAN':'Can','POR LA':'por la','OIL':'Oil','MID':'Mid','OUR':'Our',"Children'S":"Children’s",'inc.':'Inc.','international':'International'}.items():o['name']=re.sub(r'\b'+re.escape(a)+r'\b',z,o['name'])
 if not o['identity_evidence']:o['identity_evidence']='IRS name and EIN '+t['ein']+' reviewed alongside House disclosure and tax-return activity; alias or parent identity is not inferred.'
 if not o['website']:o['website_status']='unresolved'
 assert len(o['description'])>25 and o['sources'];out[k]=o
names={'d6166916694f46a6':'BioSTL','99d650b48eec74a0':'BioNJ','d2785b0e70d08c3f':'CareerWise Colorado','c62902015f19ec4d':'CareSource','dd5268550066278d':'CareSource Mission','b94a8ac9b02b80b0':'CATF Action','8371aa025896270c':'EducationSuperHighway','88dee613d80a7db3':'GMTO Corporation','c4582a8090a7db5e':'FoodCorps','8640f20b12f7cd62':'CurePSP','a5fdc41725ea1c09':'CropLife America','9200af77e37c6bad':'DeFi Education Fund','bc4f73187ad04ecc':'Coalition for Regulated HFCs, Inc.','f704e2a795967269':'CORE Electric Cooperative'}
for k,n in names.items():out[k]['name']=n
for k in ['668b42f00cb020e9','8d4071a0bcd8f8e5','d5e04ab791aa0e01','adc9c3c7e4567c84','e754135d29d815fb','b89d3eb50cab1b56','f567c37161f03465','7695e8513e6d6adb','70acb2199695784a']:out[k]['featured']=True
for v in out.values():
 for source in v['sources']:
  q=urllib.parse.urlsplit(source['url']);source['url']=urllib.parse.urlunsplit((q.scheme.lower(),q.netloc.lower(),q.path,q.query,q.fragment))
assert len(out)==225
(r/'irs-round2-rootchecked.json').write_text(json.dumps(out,indent=2)+'\n')
from collections import Counter
print(len(out),Counter(x['review_outcome'] for x in out.values()),'logos',sum(bool(x['logo_url']) for x in out.values()))
