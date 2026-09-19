import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return {'url':u,'label':'Official organization evidence','claim':c}
extra={
'86d2666ab62cd1db':('https://www.sec.gov/Archives/edgar/data/1830487/000183048726000013/phvs-20251231.htm','2025 group accounts list Pharvaris, Inc. (Delaware, USA) with 100% equity interest and describe it as service provider to the principal group company.'),
'bfaa14050737333d':('https://pittstrailers.com/wp-content/uploads/2023/03/application-for-employment_pittstrailers_form.pdf','Official employment document identifies Pitts Trailers as a division of Pitts Enterprises, Inc.'),
'645855c270b943f4':('https://www.sec.gov/Archives/edgar/data/1637207/000163720726000011/plnt-20251231.htm','2025 annual report states Planet Intermediate, LLC owns 100% of Planet Fitness Holdings, LLC, a franchisor and operator of fitness centers.'),
'8493aa5593a96cf2':('https://newsroom.porsche.com/en_US/2026/company/porsche-reports-us-retail-sales-for-half-year-2026.html','July 2026 official company release explicitly names Porsche Cars North America, Inc.'),
'ba9d0762487a1e6d':('https://www.acecashexpress.com/about/press-releases/news/ace-cash-express-announces-new-corporate-site-identity-populus-financial-group/','June 20, 2019 company announcement states ACE Cash Express is changing its corporate name to Populus Financial Group.')}
for d in json.load(open(r/'featured78-first10.json'))+json.load(open(r/'featured78-middle10.json')):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','ownership','website']};f.update(review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced');s=[src(d['official_url'],d['exact_official_excerpt'])]
 if i in extra:
  u,c=extra[i];s.append(src(u,c));f.update(review_outcome='confirmed',identity_evidence=c,notes=c)
 if i=='86d2666ab62cd1db':f.update(ownership='Subsidiary',description='U.S. service subsidiary in the Pharvaris biopharmaceutical group, which develops therapies for angioedema. The group’s 2025 accounts report 100% ownership of this entity.')
 if i=='645855c270b943f4':f['ownership']='Subsidiary'
 if i=='ba9d0762487a1e6d':s.append(src('https://www.populusfinancial.com/privacy/ca/','Current policy identifies Populus Financial Group, Inc. and its stores doing business as ACE Cash Express.'))
 if i=='cf5ef7a402928c49':f['notes']='February 2026 official legal-entity list identifies Philips North America LLC at 222 Jacobs Street, Cambridge. The former reporting label is retained as a filing label; no legal rename from Healthcare/Holding is asserted.'
 if i=='425b385807319e2f':f['notes']='Confirmed unsuffixed Phathom Pharmaceuticals organization. Website terms name an LLC while current investor materials name Inc.; no claim of legal continuity between those suffixes or parent ownership is made.'
 if i=='d6e8033438d8a201':f.update(ownership='Unknown',legal_form='Public benefit corporation',notes='Planet Labs PBC identity is supported. The filing’s former-name claim involving Planet Labs Federal Inc. remains unverified. Public benefit corporation is a legal form, not an ownership category.')
 if i=='151734a23ff46e94':f['notes']='Current Pivotal Health brand activity supported. Original AFHC and Radix Health references preserved; exact historical and represented-organization relationships remain unresolved.'
 if f['review_outcome']=='confirmed':f['website_status']='verified'
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append({'id':i,'decision':f['review_outcome'],'notes':f['notes']})
(r/'featured78-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured78-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed identities:',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()))
