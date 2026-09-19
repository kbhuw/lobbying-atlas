import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'third20-before.json');q=json.load(open(R/'matches.json'))[40:60];audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i in ['7d44c2293047b7ed','2f736509baa1bb75']:
  audit.append({'id':i,'decision':'partial','reason':'Group website address matches, but exact filed legal-entity relationship remains unverified.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization name and address match the registration: {e['address']}, {e['city']}, {e['state']}. Original source: {e['archive']} / {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof,notes='Identity and official website confirmed; ownership or tax classification remains unverified.')
 if i=='50340466fd12f0ce':x['notes']='Atmo is the represented organization; Mabus Group is the intermediary in the original filing. These roles remain separate. Ownership remains unverified.'
 if i=='21030acc3791c5f3':x['notes']='Exact company name and full office address match. The filing places part of the street address in its city field; the official website identifies Austin, Texas. Ownership remains unverified.'
 if i=='b1c76d600f96d3ab':
  x.update(website='https://atzmanufacturing.com/',ownership='Private',description='Makes Trackchair all-terrain wheelchairs and other tracked mobility equipment, and provides custom manufacturing services.',notes='Official website identifies ATZ as formerly Action Manufacturing and a second-generation family-owned business. The Alota Action LLC legal-name relationship is reported by a third-party contract source and remains separately unverified.')
  x['sources'].append({'url':'https://atzmanufacturing.com/','label':'Official company history and ownership','claim':'Identifies ATZ Manufacturing as formerly Action Manufacturing and a second-generation family-owned business based in Marshall, Minnesota.'})
 if i=='a0ade6d09cb6460c':x['notes']='The filing address matches the Madison research facility; the current corporate office is in Traverse City, Michigan. Ownership remains unverified.'
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'third20-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('18 additional identities confirmed;2 retained partial.')
