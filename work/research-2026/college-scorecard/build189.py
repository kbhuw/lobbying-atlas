import json,pathlib,re
r=pathlib.Path('work/research-2026');cr=r/'college-scorecard';out={};src=json.load(open(cr/'source.json'))['source_url'];control={'1':'Public institution','2':'Private nonprofit','3':'Private for-profit'}
for label in 'abc':
 p=json.load(open(cr/f'round2-{label}-researched.json'));p={v['id']:v for v in p} if isinstance(p,list) else p
 inputs={x['id']:x for x in json.load(open(cr/f'round2-{label}-input.json'))};assert set(p)==set(inputs)
 for k,v in p.items():
  x=inputs[k];school=x['location_matches'][0]['school'];disc=x['location_matches'][0]['disclosure'];cache=json.load(open(r/'website-cache'/f'{k}.json'))
  sources=[{'label':s.get('label','Official institution source'),'url':s['url'],'claim':s.get('claim',s.get('claims',''))} for s in v['sources'] if 'disclosurespreview.house.gov' not in s['url']]
  sources += [{'label':'Education Department institution record — May 2025','url':src,'claim':f"UNITID {school['UNITID']}: {school['INSTNM']}, {school['CITY']}, {school['STABBR']}; reported website {school['INSTURL']}; institutional control: {control[school['CONTROL']]}. Snapshot released May 19, 2025."},{'label':'House lobbying disclosure — '+disc['source_member'],'url':disc['source_url'],'claim':f"Reported client {disc['name']}; location {disc['city']}, {disc['state']}; principal location {disc['principal_city']}, {disc['principal_state']}; signed {disc['signed_date']}."}]
  o={f:v.get(f,'') for f in ['name','description','website']};o.update(sources=sources,identity_evidence=v.get('identity_notes',v.get('identity_evidence','')),notes='Institutional control is from the May 2025 Education Department snapshot; public institution describes that classification and does not imply stock-market listing.',kind='College / university',ownership=control[school['CONTROL']],institution_control_as_of='2025-05-19',status='sourced',review_outcome=v['review_outcome'],website_status='verified' if v['review_outcome']=='confirmed' else 'filed',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved')
  for term in ['accessible ',' in a close academic community',' with a focus on honor and service',' in a liberal arts and service-oriented community',' in a faith-based learning community',' in Tucson and beyond']:
   o['description']=o['description'].replace(term,'')
  if cache.get('logo_http_status')==200 and len(cache.get('text',''))>60 and '/core/misc/favicon.ico' not in cache.get('logo_url',''):
   for f in ['logo_url','logo_kind','logo_source_url']:o[f]=cache[f]
   o['logo_status']='official_site_asset';o['sources'].append({'label':'Official website branding','url':o['logo_source_url'],'claim':'Official site supplies this '+o['logo_kind'].replace('_',' ')+'. Image response checked.'})
  out[k]=o
# Do not attribute the separately operated medical center's care to Vanderbilt University.
v=out['f9cfb60e565bd49e'];v['description']='Private research university in Nashville, Tennessee, offering undergraduate, graduate and professional education.';v['sources']=[s for s in v['sources'] if s['label']!='Official institution website'];v['sources'].append({'label':'University purpose and academic profile','url':'https://www.vanderbilt.edu/about/','claim':'University describes teaching, research and the arts; its campus is in Nashville.'})
out['4c0c1481de484228']['name']='Batten University';out['4c0c1481de484228']['notes']+=' Formerly Virginia Wesleyan University; official name changed July 1, 2026. Historical disclosure names remain searchable.'
# Plain display names; preserve source names in citations and original directory aliases.
for k,n in {'9d8ad463d1105a95':'University of Maryland, Baltimore County','f10859bf0e582e7b':'University of Massachusetts Amherst','6d522ca0dcf9a5a5':'University of Nevada, Las Vegas','e749449f4838c0be':'University of Nevada, Reno','6fcd5d40b56898a6':'WSU Tech','9e258b5ea17c23f3':'Mt. Hood Community College','ec125b676d848925':'Mt. San Antonio College'}.items():out[k]['name']=n
for k in ['abcf358c6d1b8a15','558189f677c575be','50c3e786d29448c1','60b288ac2867db56','ccfa09731928abd4','7f7007685369bd77','f9cfb60e565bd49e','58b06a31295dee6c','91d1a43bdf39c646']:out[k]['featured']=True
assert len(out)==189
(cr/'round2-staged.json').write_text(json.dumps(out,indent=2)+'\n');print('189 staged')
