import json,pathlib,copy
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));a={x['id']:x for x in json.load(open(r/'sbir-domain-candidates215.json'))};assert not (r/'featured219-before.json').exists();before={};dec=[]
items={
'b3d5e614df0c7a5f':('Electra.aero','https://electra.aero/','The SBIR award identifies ELECTRA.AERO INC., its electra.aero domain, Manassas location and hybrid-electric aircraft propulsion work. The current official site confirms the matching aviation business and Manassas headquarters.'),
'f2903267fff66b31':('Seatrec Incorporated','https://seatrec.com/','The federal award identifies SEATREC, INC. and explicitly links seatrec.com. The official site describes ocean-temperature-powered subsea drones and monitoring systems, matching the represented ocean-technology business.'),
'8d7065f035026c2e':('Prelude Corporation (PreludeDx)','https://www.preludedx.com/','The official PreludeDx site identifies Prelude Corporation in its copyright notice and describes its cancer-test business. The federal award names PRELUDE CORP and links the same domain; the historical award is used for identity, not current performance claims.'),
'e679b4271e6beb3d':('Weather Stream (formerly Orbital Micro Systems)','https://weatherstream.com/technology/orbital-micro-systems/','The official company history explicitly states Orbital Micro Systems is now known as Weather Stream. The 2026 SBIR record identifies ORBITAL MICRO SYSTEMS, INC. DBA Weather Stream and gives the same Boulder address and domain. The former-name relationship is corroborated; no legal conversion or ownership claim is inferred.'),
'6a579579858c2df3':('BeaverFit USA','https://beaverfitusa.com/','The official BeaverFit USA site names BeaverFit North America LLC in its footer and lists 120 Woodland Avenue, Reno. The SBIR record gives the same legal name, address and domain, confirming the U.S. business identity.')}
for i,(name,url,note) in items.items():
 v=p[i];before[i]=copy.deepcopy(v);x=a[i]['records'][0];v.update(name=name,review_outcome='confirmed',website_status='verified',checked_at='2026-09-13',notes=note,identity_evidence=note)
 v['sources'].extend([dict(url=url,label='Official identity and activity evidence',claim=note),dict(url='https://data.www.sbir.gov/mod_awarddatapublic_no_abstract/award_data_no_abstract.csv',label='Federal award identity: '+x['UEI'],claim=f"Awardee {x['Company']}, UEI {x['UEI']}, explicitly links {x['Company Website']}. Used as identity evidence; no ownership inference.")])
 if i=='8d7065f035026c2e':v['kind']='Cancer diagnostic testing company'
 if i=='6a579579858c2df3':v['kind']='Fitness and training equipment manufacturer'
 dec.append(dict(id=i,record=x,notes=note))
for k,v in [('before',before),('decisions',dec)]: (r/f'featured219-{k}.json').write_text(json.dumps(v,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('5 identities and 1 website confirmed')
