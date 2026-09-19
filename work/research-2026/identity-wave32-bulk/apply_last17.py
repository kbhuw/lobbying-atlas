import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'last17-before.json');q=json.load(open(R/'matches.json'))[75:];audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i in ['45af18082e8f37ed']:
  audit.append({'id':i,'decision':'partial','reason':'Exact legal-entity relationship or conflicting filing state requires corroboration.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization name and address match the registration: {e['address']}, {e['city']}, {e['state']}. Original source: {e['archive']} / {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof,notes=x.get('notes',''))
 x['description']=x['description'].split(' Self-reported')[0]
 if i=='8751d1a65aed2b50':x['notes']='The original registration explicitly names Cohesity, Inc., and the current official footer names the same entity at the filed address. Preserve the distinction from Cohesity Global Inc.; current ultimate ownership remains unverified.'
 if i=='412a981b65243596':x['notes']='Coalition identity and contact address confirmed. The Nareit website copyright does not establish separate incorporation or tax status for the coalition.'
 if i=='b1c76d600f96d3ab':x['sources'].append({'url':'https://atzmanufacturing.com/','label':'Official company history and ownership','claim':'Identifies ATZ Manufacturing as formerly Action Manufacturing and a second-generation family-owned business based in Marshall, Minnesota.'})
 if i=='a0ade6d09cb6460c':x['notes']='The filing address matches the Madison research facility; the current corporate office is in Traverse City, Michigan. Ownership remains unverified.'
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'last17-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('16 additional identities confirmed;1 retained partial.')
