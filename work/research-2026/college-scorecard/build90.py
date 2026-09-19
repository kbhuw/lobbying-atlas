import json,pathlib,re
r=pathlib.Path('work/research-2026');cr=r/'college-scorecard';out={};src=json.load(open(cr/'source.json'))['source_url'];control={'1':'Public institution','2':'Private nonprofit','3':'Private for-profit'}
exclude={'11fc7ca672fa2895','5b171cfef26bd631','6aec73c885da3d2d','6fb00379d66d8087'}
for label in ['a','b','c']:
 p=json.load(open(cr/f'review-{label}-researched.json'));inputs={x['id']:x for x in json.load(open(cr/f'review-{label}-input.json'))};assert set(p)==set(inputs)
 if label=='a':p.update(json.load(open(cr/'review-a-corrections.json')))
 for k,v in p.items():
  x=inputs[k];school=x['location_matches'][0]['school'];disc=x['location_matches'][0]['disclosure'];cache=json.load(open(r/'website-cache'/f'{k}.json'));sources=[s for s in v['sources'] if 'Education Department' not in s.get('label','') and 'Scorecard' not in s.get('label','')]
  sources.append({'label':'Education Department institution record — May 2025','url':src,'claim':f"UNITID {school['UNITID']}: {school['INSTNM']}, {school['CITY']}, {school['STABBR']}; reported website {school['INSTURL']}; institutional control: {control[school['CONTROL']]}. Snapshot released May 19, 2025."})
  o={f:v.get(f,'') for f in ['name','description','website','identity_evidence','notes']};o.update(sources=sources,kind='College / university',ownership=control[school['CONTROL']],institution_control_as_of='2025-05-19',status='sourced',review_outcome='confirmed',website_status='verified',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved')
  o['notes']+=' Institutional control is from the May 2025 Education Department snapshot unless a newer source is cited.'
  for old,new in [(' Of ',' of '),(' And ',' and '),(' VIA ',' Via '),('Gardner-webb','Gardner-Webb')]:o['name']=o['name'].replace(old,new)
  for term in [' in service of humanity',' in service to the public good',' focused on leadership and service',' emphasizing learning, service, and leadership',' preparing graduates for leadership and service',' designed around student success','affordable ','accessible ','quality ']:o['description']=o['description'].replace(term,'')
  o['description']=o['description'].rstrip('.')+'.'
  if cache.get('logo_http_status')==200 and len(cache.get('text',''))>60 and k not in exclude and '/core/misc/favicon.ico' not in cache.get('logo_url',''):
   for f in ['logo_url','logo_kind','logo_source_url']:o[f]=cache[f]
   o['logo_status']='official_site_asset';o['sources'].append({'label':'Official website branding','url':o['logo_source_url'],'claim':'Official site supplies this '+o['logo_kind'].replace('_',' ')+'. Image response checked.'})
  out[k]=o
v=out['c7d1bac8c13328f9'];corr=json.load(open(cr/'review-c-corrections.json'))['corrections']['c7d1bac8c13328f9'];v.update(website=corr['recommended_website'],description='Community college in Freeport, Illinois, offering degrees, certificates, transfer programs and workforce education.',identity_evidence=corr['identity_note']);v['sources']=[s for s in v['sources'] if 'highlandcc.edu' not in s['url']]+[dict(label='Correct Illinois institution identity',**s) for s in corr['evidence']];v['notes']+=' The separate Kansas college is not assigned to this record.'
v=out['686378667d09e6ec'];v.update(description='College in Muskogee, Oklahoma, whose accreditation was withdrawn in July 2024. Current operating status remains unconfirmed.',website_status='filed',review_outcome='partial');v['sources'].append({'label':'Accreditor action','url':'https://www.hlcommission.org/for-students/accreditation-actions/june-2024/','claim':'HLC withdrew Bacone College accreditation effective July 17, 2024. This does not by itself establish legal closure.'})
v=out['80991d3365361180'];v.update(ownership='Private nonprofit',institution_control_as_of='2025-12-15');v['notes']='The May 2025 Scorecard classified GCU as for-profit. A December 15, 2025 university announcement reports subsequent Education Department recognition of nonprofit status; the newer status is displayed. Grand Canyon Education is a separate company.';v['sources'].append({'label':'Updated nonprofit recognition','url':'https://news.gcu.edu/gcu-news/department-of-education-officially-recognizes-nonprofit-status-of-grand-canyon-university/','claim':'December 15, 2025 university announcement reports formal Education Department recognition of GCU as a nonprofit institution.'})
for k in ['f4c636b784758363','de341329c9e6e95c','841d8d7347242995','8fcbe5cce7ab2f2b','bb2a1bfed1f2e73f','2b6331e3e8f7ebe2','b259a22796aa0d1b','7977f5c18bea0570']:out[k]['featured']=True
out['bf75752c3d46cec4']['description']='Christian university offering online and campus-based degree programs.'
out['fe8dcf0f64870f8e']['description']='Public research university offering undergraduate and graduate programs in business, education, health, humanities, sciences and other fields.'
assert len(out)==90
(cr/'review90-staged.json').write_text(json.dumps(out,indent=2)+'\n');print('90 staged with correctcampuses, GCU update, Bacone uncertainty and logo exclusions')
