import json,pathlib,re
r=pathlib.Path('work/research-2026');p=json.load(open(r/'irs-round1-correcting.json'));inputs={x['id']:x for l in 'abc' for x in json.load(open(r/f'irs-round1-{l}-input.json'))};a=json.load(open(r/'irs-round1-a-final-audit.json'))['findings'];b=json.load(open(r/'irs-round1-b-final-audit.json'));out={}
for k,v in p.items():
 o={f:v.get(f,'') for f in ['name','description','kind','website','identity_evidence']};o.update(ownership='Nonprofit / tax-exempt',status='sourced',review_outcome=v.get('review_outcome','partial'),website_status='filed',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved',notes='Individual organization review using its tax return, disclosure identity evidence and official website where available. Affiliated foundations and parent organizations remain distinct; tax exemption alone does not establish donation deductibility.',sources=[{'url':s['url'],'label':s.get('label','Source'),'claim':s.get('claim',s.get('claims',''))} for s in v['sources'] if s.get('url')])
 t=inputs[k]['tax_return'];o['sources'].append({'url':t['source_url'],'label':'Organization Form 990','claim':'Filed organization '+t.get('organization_name','')+'; EIN '+t['ein']+'. Mission and filed website reviewed. The return describes the organization as of its reporting period.'})
 if k in a and a[k].get('correction'):
  fix=a[k];o['sources'] += [{'url':s['url'],'label':s.get('label','Official source'),'claim':s.get('claim',s.get('claims',''))} for s in fix.get('sources',[])];o['review_outcome']=fix.get('review_outcome','partial');o['name']=fix.get('name',o['name'])
 if k in b:
  fix=b[k].get('corrections',{})
  for f in ['name','description','identity_evidence']:
   if fix.get(f):o[f]=fix[f]
  ss=b[k].get('supporting_source',{})
  if ss.get('url'):o['sources'].append({'url':ss['url'],'label':'Identity review source','claim':ss.get('excerpt','')})
 if k=='c65628d395cd08ee':o['description']='Trade organization advocating for the U.S. coal fleet and coal supply chain.'
 if k=='6921b1f27f582b47':o['notes']+=' Renamed American Alliance of Museums in 2012; original American Association of Museums filing names are preserved.'
 if k=='920784f13f3df837':o['name']='ACCSES';o['review_outcome']='partial'
 if k=='acbc2053e4ba0a7f':
  o.update(website='https://www.cpac.org/',identity_evidence='Official CPAC privacy notice explicitly identifies American Conservative Union doing business as CPAC and separately identifies American Conservative Union Foundation doing business as CPAC Foundation.',review_outcome='confirmed');o['sources'].append({'url':'https://www.cpac.org/privacy','label':'CPAC legal identity notice','claim':'Identifies the American Conservative Union d/b/a CPAC separately from the American Conservative Union Foundation d/b/a CPAC Foundation.'});o['notes']+=' CPAC is the operating name; the foundation remains a separate entity.'
 c=json.load(open(r/'website-cache'/f'{k}.json'))
 if o['website'] and c.get('requested_url','').rstrip('/')==o['website'].rstrip('/') and c.get('http_status')==200 and len(c.get('text',''))>100:
  o['website']=c.get('final_url',o['website']);o['website_status']='verified'
  if c.get('logo_http_status')==200 and k not in ['b19a8084b7f175f0','9a88cab8817466d4','8fcb76d9c1be097c']:
   for f in ['logo_url','logo_kind','logo_source_url']:o[f]=c.get(f,'')
   o['logo_status']='official_site_asset';o['sources'].append({'url':o['logo_source_url'],'label':'Official website branding','claim':'Official page supplies this '+o['logo_kind'].replace('_',' ')+'. Image response checked.'})
 else:o['review_outcome']='partial';o['website_status']='filed' if o['website'] else 'unresolved'
 # Sentence case in names, retaining known acronyms.
 o['name']=re.sub(r'\b(Of|For|The|And|ON|AT|LOS|GAS)\b',lambda m:{'Of':'of','For':'for','The':'the','And':'and','ON':'on','AT':'at','LOS':'Los','GAS':'Gas'}[m[0]],o['name'])
 if not o['identity_evidence']:o['identity_evidence']='IRS EIN and organization name, House disclosure identity evidence, and organization tax-return mission reviewed; historical alias relationships are not inferred.'
 assert len(o['description'])>20;out[k]=o
for k,n in {'6ea6b3f0f8228b6d':'AIDS Healthcare Foundation','912bf610e9f5d972':'AIDS United','8c3d1efb6b88104c':'AlohaCare','dbd9c7039aed7405':'AltaSea at the Port of Los Angeles','81ae1420aefc4515':'AMERIPEN','8915af431a60fd67':'AnMed Health System','56ee554586e57d3d':'ARcare','d48fa15c5e72d2ef':'APTS Action Inc.'}.items():out[k]['name']=n
for k in ['92fdc2897b80a25b','9310fb0079cade50','60cc8271ec9e6de9','e06e8e7dc2ce0f6a','cd2629a0bf1cb720','acbc2053e4ba0a7f','aa9443b57c75e40c','57a2c409789fd861']:out[k]['featured']=True
assert len(out)==150;(r/'irs-round1-rootchecked.json').write_text(json.dumps(out,indent=2)+'\n');print('150 staged; source/logo repairs applied')
