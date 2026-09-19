import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'fifth20-before.json');q=json.load(open(R/'matches.json'))[80:100];audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i in ['bcb6c193382c8f48','337d4bfe32cfb526','3f8960d91ea35840']:
  audit.append({'id':i,'decision':'partial','reason':'Exact legal-entity relationship or conflicting filing state requires corroboration.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization name and address match the registration: {e['address']}, {e['city']}, {e['state']}. Original source: {e['archive']} / {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof,notes='Identity and official website confirmed; ownership or tax classification remains unverified.')
 x['description']=x['description'].split(' Self-reported')[0]
 if i=='5927976f900fdfbf':x['notes']='Identifies the county government in Pennsylvania. This is a government body, not a privately owned company.'
 if i=='cb10b85b3df243dc':x['notes']='BioTissue identity and address confirmed. Preserve the distinction from TissueTech; this check does not establish current ownership.'
 if i in ['d152cfcd899bb505','c26899eb7518506b']:x['notes']='The same legal name and office address occur in the other Biomass Energy Systems entry. Saved as a duplicate candidate for review; no merge applied here. Ownership remains unverified.'
 if i=='b1c76d600f96d3ab':x['sources'].append({'url':'https://atzmanufacturing.com/','label':'Official company history and ownership','claim':'Identifies ATZ Manufacturing as formerly Action Manufacturing and a second-generation family-owned business based in Marshall, Minnesota.'})
 if i=='a0ade6d09cb6460c':x['notes']='The filing address matches the Madison research facility; the current corporate office is in Traverse City, Michigan. Ownership remains unverified.'
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'fifth20-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('17 additional identities confirmed;3 retained partial.')
