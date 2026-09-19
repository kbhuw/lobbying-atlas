import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'local15-before.json');q=json.load(open(R/'matches.json'))[35:50];audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i in ['0a9de684dd130284','d98ee2a4cc511f0d','0ee06d909f0bd925','2e9c719be316f40b']:
  audit.append({'id':i,'decision':'partial','reason':'Exact legal-entity relationship or conflicting filing state requires corroboration.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization name and address match the registration: {e['address']}, {e['city']}, {e['state']}. Original source: {e['archive']} / {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof,notes=x.get('notes',''))
 x['description']=x['description'].split(' Self-reported')[0]
 if i=='7d24e6c81cdb6988':x['name']='International Code Council (ICC)'
 if i=='0a1adad01630ed90':x['name']='International Association of Scientific, Technical & Medical Publishers (STM)'
 if i=='96f2b48615d27fd7':x['name']='International Association of Sheet Metal, Air, Rail and Transportation Workers'
 if i=='bc33f336075276cc':x['legal_form']='Company limited by guarantee';x['notes']='Official footer gives England and Wales company number 6467372 and identifies a company limited by guarantee. Tax exemption is not inferred.'
 if i=='b1c76d600f96d3ab':x['sources'].append({'url':'https://atzmanufacturing.com/','label':'Official company history and ownership','claim':'Identifies ATZ Manufacturing as formerly Action Manufacturing and a second-generation family-owned business based in Marshall, Minnesota.'})
 if i=='a0ade6d09cb6460c':x['notes']='The filing address matches the Madison research facility; the current corporate office is in Traverse City, Michigan. Ownership remains unverified.'
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'local15-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('11 additional identities confirmed;4 retained partial.')
