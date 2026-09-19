import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'fourth20-before.json');q=json.load(open(R/'matches.json'))[60:80];audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i in ['ec0acfb24a65a6a8','cc96c2e46d94e4e8','aab173f9ac277c3b','6c814815d3b40283','da748fd88a5c44d9','2ba7fc965bebe04c']:
  audit.append({'id':i,'decision':'partial','reason':'Exact legal-entity relationship or conflicting filing state requires corroboration.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization name and address match the registration: {e['address']}, {e['city']}, {e['state']}. Original source: {e['archive']} / {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof,notes='Identity and official website confirmed; ownership or tax classification remains unverified.')
 x['description']=x['description'].split(' Self-reported')[0]
 if i=='bcec7a8269e6d7d3':x['notes']='The official contact page explicitly lists Awbury Technical Solutions LLC at the filed address, separately from other Awbury entities. Ownership remains unverified.'
 if i in ['53f8e487f0119112','27c70d1d49d29993']:x['notes']='Name and headquarters match Bausch Health Companies Inc. A potential duplicate of the other Bausch Health entry is recorded for deduplication review; no merge applied here. Ownership remains unverified.'
 if i=='b1c76d600f96d3ab':x['sources'].append({'url':'https://atzmanufacturing.com/','label':'Official company history and ownership','claim':'Identifies ATZ Manufacturing as formerly Action Manufacturing and a second-generation family-owned business based in Marshall, Minnesota.'})
 if i=='a0ade6d09cb6460c':x['notes']='The filing address matches the Madison research facility; the current corporate office is in Traverse City, Michigan. Ownership remains unverified.'
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'fourth20-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('14 additional identities confirmed;6 retained partial.')
