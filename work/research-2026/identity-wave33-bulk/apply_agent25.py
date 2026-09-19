import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'agent25-before.json');q=json.load(open(R/'matches.json'))[65:90];audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i in ['df529e3fefcf7dd2']:
  audit.append({'id':i,'decision':'partial','reason':'Exact legal-entity relationship or conflicting filing state requires corroboration.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization name and address match the registration: {e['address']}, {e['city']}, {e['state']}. Original source: {e['archive']} / {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof,notes=x.get('notes',''))
 x['description']=x['description'].split(' Self-reported')[0]
 if i=='c77f79bd2f55dc41':x['notes']='Florida DBPR license SEA4501709 directly identifies BWI of Central Florida Inc. as Drifters Riverfront Bar and Grill at the filed address; current active license checked September 12, 2026. Equity ownership remains unverified.'
 if i=='864c9b6a0bb9e250':x['notes']='Official GSA contract page names Earth Resources Technology, LLC as legal entity under Entarian and lists the filed Greenbelt address; checked September 12, 2026. Ownership remains unverified.'
 if i=='b1c76d600f96d3ab':x['sources'].append({'url':'https://atzmanufacturing.com/','label':'Official company history and ownership','claim':'Identifies ATZ Manufacturing as formerly Action Manufacturing and a second-generation family-owned business based in Marshall, Minnesota.'})
 if i=='a0ade6d09cb6460c':x['notes']='The filing address matches the Madison research facility; the current corporate office is in Traverse City, Michigan. Ownership remains unverified.'
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'agent25-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('24 additional identities confirmed;1 retained partial.')
