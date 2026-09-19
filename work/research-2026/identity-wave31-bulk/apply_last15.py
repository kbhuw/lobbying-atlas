import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'last15-before.json');q=json.load(open(R/'matches.json'))[100:];audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i in ['9c8732fc9f458ea8','9a4932d85ea436ab','a4520da5406a2e76','c99a636b9b8301ec','31c3c9c3b9705fcd']:
  audit.append({'id':i,'decision':'partial','reason':'Exact legal-entity relationship or conflicting filing state requires corroboration.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization name and address match the registration: {e['address']}, {e['city']}, {e['state']}. Original source: {e['archive']} / {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof,notes='Identity and official website confirmed; ownership or tax classification remains unverified.')
 x['description']=x['description'].split(' Self-reported')[0]
 if i=='fb562de31d11f1be':x['notes']='Official website states BCAN is a 501(c)(3) nonprofit. This statement has not been independently checked against IRS records in this pass.'
 if i=='786712ee350bfbd4':
  x['legal_form']='Mutual insurance company'
  x['notes']='Official company facts identify a mutual insurance company and a not-for-profit health plan. No particular federal tax-exemption subsection is inferred.'
 if i=='f0bf8ebfe9f52517':x['notes']='The filed Nashua address matches BluGlass Inc., explicitly listed on the group website. Preserve the US entity distinction from Australian BluGlass Limited; current ownership remains unverified.'
 if i=='ab73d1b64fd7fe33':x['notes']='The official UnityPoint location page identifies this hospital at the filed address. This does not establish the hospital operating legal entity or its tax classification.'
 if i=='b1c76d600f96d3ab':x['sources'].append({'url':'https://atzmanufacturing.com/','label':'Official company history and ownership','claim':'Identifies ATZ Manufacturing as formerly Action Manufacturing and a second-generation family-owned business based in Marshall, Minnesota.'})
 if i=='a0ade6d09cb6460c':x['notes']='The filing address matches the Madison research facility; the current corporate office is in Traverse City, Michigan. Ownership remains unverified.'
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'last15-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('10 additional identities confirmed;5 retained partial.')
