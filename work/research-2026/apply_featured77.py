import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return {'url':u,'label':'Official organization evidence','claim':c}
extra={
'b7541f89577f5280':('https://www.sec.gov/Archives/edgar/data/917225/000110465923089231/tm2323309d1_sc13ga.htm','SEC disclosure states Newmont Mining Corporation changed its name to Newmont Goldcorp Corporation on April 17, 2019 and to Newmont Corp. on January 6, 2020.'),
'ccab1bdfab3298bb':('https://www.sec.gov/Archives/edgar/data/1142417/000119312526078361/nxst-20251231.htm','2025 annual report defines Nexstar as Nexstar Media Group, Inc. and its consolidated subsidiaries; group scope retained.'),
'2444ec141479f692':('https://www.nokia.com/privacy/notices/affiliates/','Official affiliate list names Nokia of America Corporation.'),
'5f48077cce1720ee':('https://www.noom.com/terms-and-conditions-of-use/','Terms explicitly identify Noom, Inc. as provider of Noom website and app services.'),
'c7bc081b90272b62':('https://www.nm.org/-/media/northwestern/resources/about-us/northwestern-medicine-fy20-community-benefits-plan-report.pdf','FY2020 community report identifies Northwestern Memorial HealthCare as the nonprofit corporate parent of its named hospitals and subsidiaries.'),
'65fef439c510d52e':('https://www.onsemi.com/site/pdf/Annual-Report-Canada-Bill-S211.pdf','2025 official report identifies ON Semiconductor Corporation (dba onsemi).')}
for d in json.load(open(r/'featured77-first10.json'))+json.load(open(r/'featured77-middle10.json')):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','ownership','website']};f.update(review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced');s=[src(d['official_url'],d['exact_official_excerpt'])]
 if i in extra:
  u,c=extra[i];s.append(src(u,c));f.update(review_outcome='confirmed',identity_evidence=c,notes=c)
 if i=='b7541f89577f5280':f['description']='Mining company historically filed as Newmont Mining Corporation; renamed Newmont Goldcorp in 2019 and Newmont Corporation in 2020. Produces gold and other metals.'
 if i=='ccab1bdfab3298bb':f['notes']+=' This filing names the parent and affiliates together; individual affiliate ownership is not inferred.'
 if i=='f1359c9aa25c852b':f.update(ownership='Unknown',notes='Official filing describes Newsmax Inc. as a new holding company owning Newsmax Media, Inc. This does not establish a simple legal rename. The filed FKA claim remains unverified; do not merge the parent and operating company.')
 if i=='e69c9874a99be539':f['notes']='Confirmed as a combined parent/subsidiary filing: official policy explicitly identifies FPL as a NextEra subsidiary. The two legal entities remain distinguished.'
 if i=='840870a64279a727':s.append(src('https://www.nei.org/','Browser-rendered official homepage identifies Nuclear Energy Institute and describes industry advocacy and education.'))
 if i=='fba08b73f9c1d91b':f['notes']='Confirmed at OpenAI organization/brand scope. This unsuffixed filing alone does not select one legal entity or establish ownership.'
 if f['review_outcome']=='confirmed':f['website_status']='verified'
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append({'id':i,'decision':f['review_outcome'],'notes':f['notes']})
(r/'featured77-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured77-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed identities:',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()))
