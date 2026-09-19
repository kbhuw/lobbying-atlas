import json,pathlib,copy
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured228-before.json').exists();before={};dec=[]
items={
'303181404bbc8e9a':('https://www.ampact.us/privacy-policy','Ampact’s official privacy policy identifies Ampact Inc. as the organization. Its official board biography describes Ampact as a 501(c)(3) nonprofit managing AmeriCorps programs. Identity and nonprofit classification are supported; no ownership or control beyond that status is inferred.'),
'17657bc809a21991':('https://www.anbex.com/','Anbex’s official homepage identifies Anbex, Inc. and its IOSAT potassium iodide tablet business, matching the disclosed pharmaceutical manufacturer. Identity is confirmed; ownership remains unknown.'),
'a822944c59b1ba47':('https://www.anchorhocking.com/contact-us/','The official contact page explicitly identifies Anchor Hocking Company on anchorhocking.com, matching the disclosed glassware manufacturer. Related Corelle entities are not merged into this record; current ownership remains unknown.'),
'8cefa8a466f9bcb0':('https://www.ardentmills.com/documentation/','Ardent Mills’ official documentation page explicitly names Ardent Mills, LLC in its invoice and import/export terms. The exact filed LLC and operating website are confirmed; separately named affiliates are not treated as the same legal entity and current ownership remains unknown.'),
'0a6e589b78897ecf':('https://www.agg.com/about-us/','The official AGG About page describes the Atlanta and Washington law firm and names Arnall Golden Gregory LLP in its copyright notice. This confirms the exact disclosed firm and official domain; ownership remains unknown.')}
for i,(url,n) in items.items():
 v=p[i];before[i]=copy.deepcopy(v);v.update(review_outcome='confirmed',checked_at='2026-09-13',notes=n,identity_evidence=n);v['sources'].append(dict(url=url,label='Official identity evidence',claim=n))
 if i=='303181404bbc8e9a':
  v['ownership']='Nonprofit / tax-exempt';v['sources'].append(dict(url='https://www.ampact.us/our-team2/kim-plahn',label='Official nonprofit classification',claim='The official biography explicitly describes Ampact as a 501(c)(3) nonprofit managing AmeriCorps programs.'))
 dec.append(dict(id=i,url=url,notes=n))
for k,v in [('before',before),('decisions',dec)]: (r/f'featured228-{k}.json').write_text(json.dumps(v,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('5 identities and Ampact nonprofit classification confirmed')
