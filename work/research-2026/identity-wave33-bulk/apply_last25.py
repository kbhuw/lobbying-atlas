import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'last25-before.json');q=json.load(open(R/'matches.json'))[90:];audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i in ['e97ef9b82b9deb5e','d3ff3d3de7f7bab1','f27d9e78af643e26','e83056ad1c709683','775bfaf68a474c62','0d1635ad7190e2f1','624f388be854b50c']:
  audit.append({'id':i,'decision':'partial','reason':'Exact legal-entity relationship or conflicting filing state requires corroboration.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization name and address match the registration: {e['address']}, {e['city']}, {e['state']}. Original source: {e['archive']} / {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof,notes=x.get('notes',''))
 x['description']=x['description'].split(' Self-reported')[0]
 if i=='cc7681cf1d9eac90':x['name']='Engineered Tax Services, Inc.'
 if i in ['de3116449e13fcf6','476dfd67e91cbd34']:x['notes']='The EnergySource Minerals name and Carlsbad address match; ESM Inside LLC is separately identified as its employer. Duplicate-name review is pending. Ownership remains unverified.'
 if i=='b1c76d600f96d3ab':x['sources'].append({'url':'https://atzmanufacturing.com/','label':'Official company history and ownership','claim':'Identifies ATZ Manufacturing as formerly Action Manufacturing and a second-generation family-owned business based in Marshall, Minnesota.'})
 if i=='a0ade6d09cb6460c':x['notes']='The filing address matches the Madison research facility; the current corporate office is in Traverse City, Michigan. Ownership remains unverified.'
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'last25-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('18 additional identities confirmed;7 retained partial.')
