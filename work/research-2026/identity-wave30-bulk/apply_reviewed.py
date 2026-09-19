import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'before.json')
accepted=['09c9662ab0458fb1','0f4ceb294a8b89a4','211d0c174a53b0e9','40960fb4b191eec5','42340b4cf8776938','9706911406ac89cc','a2e1ead593a8ef2d','c1837d8942f748bb','8002d7e31b84a6f5','fe7833bbeff2124d']
audit=[]
for i in accepted:
 d=json.load(open(R/(i+'.json')));m=d['matches'][0];e=m['registration'];x=p[i]
 proof=f"Official page matches the filing name/business and street address at {e['address']}, {e['city']}, {e['state']}. House registration: {e['archive']}, {e['member']}."
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof)
 x['notes']='Identity and website are corroborated by the official business/contact page and the original registration address. Ownership remains separately qualified; an address match does not establish shareholders or a parent company.'
 if i=='0f4ceb294a8b89a4':x['ownership']='Private';x['notes']='Official Aero Air homepage describes generations of family ownership. Individual ownership percentages are not established.'
 if i=='fe7833bbeff2124d':x['name']='American Family Mutual Insurance Company, S.I.';x['notes']='Official company-information page names the exact S.I. insurer and Madison address. S.I. denotes the converted stock insurer; it is kept distinct from the ultimate mutual holding company. Ownership chain remains unverified here.'
 if i=='a2e1ead593a8ef2d':x['notes']='The Akron address resolves the previously ambiguous Alterra brand match to alterra360.com. Official footer names Alterra Energy LLC; no merger with other Alterra-named businesses is assumed.'
 if i=='8002d7e31b84a6f5':x['notes']='Official contact page identifies AllianceBernstein L.P. at the historical filing address. The listed holding partnership is not automatically substituted for this operating partnership.'
 if i=='42340b4cf8776938':x['legal_form']='Limited liability company (LLC)';x['notes']='Official website footer names American Vascular Associates, LLC and matches the Palm Harbor address. No shareholder or parent-company claim is made.'
 if i=='40960fb4b191eec5':x['name']='American Feed Industry Association (AFIA)'
 x['sources'] += [{'url':m['page_url'],'label':'Official address and identity checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 audit.append({'id':i,'decision':'identity_confirmed','evidence':m,'ownership_inferred_from_address':False})
for i,u in [('42340b4cf8776938','https://www.americanvascular.com/hs-fs/hubfs/Red3.png?width=641&height=217&name=Red3.png'),('9706911406ac89cc','https://www.americanroads.com/images/logo.png')]:
 x=p[i];x.update(logo_url=u,logo_source_url=json.load(open(R/(i+'.json')))['matches'][0]['page_url'],logo_kind='logo',logo_status='official_site_asset');shutil.copyfile(R/(i+'-logo.png'),ROOT/'lobbying-map/public/logos'/f'{i}-official.png')
for d in json.load(open(R/'matches.json')):
 if d['id'] not in accepted:audit.append({'id':d['id'],'decision':'still_partial','reason':'Address match alone does not resolve the exact legal entity, represented-principal relationship, or other existing qualification. No automatic confirmation.'})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'review-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('Confirmed',len(accepted),'identities; added two official logos. Other matches remain partial.')
