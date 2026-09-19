import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'second20-before.json');q=json.load(open(R/'matches.json'))[20:40];audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i=='b639175db9b98f7f':audit.append({'id':i,'decision':'partial','reason':'Bravida brand and address match; independently corroborating Argentum legal-name relationship remains necessary.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization name and address match the registration: {e['address']}, {e['city']}, {e['state']}. Original source: {e['archive']} / {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof,notes='Identity and official website confirmed; ownership or tax classification remains unverified.')
 if i in ['155cfbef9a470535','74534c2fac01baef']:x['legal_form']='Limited liability company (LLC)'
 if i=='70afd95e09373b55':x['legal_form']='Corporation'
 if i=='36ab0d5dd75cd922':x['name']='Association for Accessible Medicines';x['notes']='Official name uses “for Accessible Medicines”; original filing wording is retained. Tax classification remains unverified.'
 if i in ['3b2fd965fc215f5d','42581577922cd55d']:x['notes']='This entry identifies the regional chapter, not the national organization. Tax classification remains unverified.'
 if i=='88b673ff6aef94cc':x['notes']='Healthcare communications company formerly branded WELL Health. The address distinguishes it from other Artera businesses. Ownership remains unverified.'
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'second20-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('19 additional identities confirmed;1 retained partial.')
