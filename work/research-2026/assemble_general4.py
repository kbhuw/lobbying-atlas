import json,pathlib
r=pathlib.Path('work/research-2026')
def read(f):return json.load(open(r/f))
p=read('general-round4-90-draft.json')
for k,a in read('general-round4-a-audit.json').items():
 if a.get('correction'):
  p[k].update(a['correction'])
  if a.get('source_url'):p[k]['sources'].append(dict(url=a['source_url'],claim=a['source_excerpt'],label='Primary identity correction'))
for k,v in read('general-round4-a-repairs.json').items():
 old=p[k]['sources'];p[k].update(v);p[k]['sources']=[s for s in old if 'advion.org' not in s['url']]+v['sources']
for k,c in read('general-round4-b-corrections.json')['corrections'].items():
 for f in ['name','website','description','ownership']:p[k][f]=c[f]
 p[k]['sources']=[s for s in p[k]['sources'] if 'lockheedmartin' not in s['url']]
 for f in ['supporting_source','additional_source']:
  if c.get(f):p[k]['sources'].append(dict(c[f],label='Corporate identity evidence'))
for a in read('general-round4-c-audit.json')['records']:
 k=a['id']
 for f in ['website','ownership','description']:
  if a.get(f+'_correction'):p[k][f]=a[f+'_correction']
 p[k]['sources']+=a['sources']
 if k=='4feb2399fd1c7a79':p[k].update(description='Molecular diagnostics company providing MammaPrint breast-cancer recurrence testing and BluePrint tumor subtyping to help guide treatment decisions.',review_outcome='partial',status='sourced',identity_evidence='Official homepage identifies Agendia Inc. in Irvine, California and describes molecular breast-cancer testing, matching the clinical laboratory and molecular diagnostics filing descriptions.')
 if k=='4c95b6a16e501c0c':p[k]['notes']='The disclosed Agility Public Warehousing legal entity now uses the Makhazen brand; separate Agility entities are not merged.'
k='545b5c44939a50b1';p[k].update(website='https://aerofliteinc.com/about',description='Aerial firefighting company operating airtankers and water-scooping aircraft to support wildfire suppression and land-management agencies.',ownership='Private company',status='sourced',review_outcome='confirmed',identity_evidence='Official Aero-Flite website describes the same firefighting business as the filing; its 2025 corporate introduction identifies it as privately owned.')
p[k]['sources'] += [dict(url='https://aerofliteinc.com/about',claim='Aero-Flite describes airtanker and water-scooping aircraft used for wildfire suppression.',label='Official company overview'),dict(url='https://aerofliteinc.com/wp-content/uploads/2025-AFI-Introduction.pdf',claim='2025 corporate introduction identifies Aero-Flite as a privately owned aerial firefighting provider.',label='Official company introduction')]
for k in ['ef6b025d2e9b8a9d','9d36129f3b82ada1','6b54662afba94dc0']:p[k]['featured']=True
(r/'general-round4-90-draft.json').write_text(json.dumps(p,indent=2)+'\n')
