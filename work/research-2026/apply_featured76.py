import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return {'url':u,'label':'Official organization evidence','claim':c}
for d in json.load(open(r/'featured76-first10.json'))+json.load(open(r/'featured76-middle10.json')):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','ownership','website']};f.update(review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced');s=[src(d['official_url'],d['exact_official_excerpt'])]
 if i=='0e38c4e035ae52f6':f.update(description='Museum and memorial in Columbus, Ohio, sharing the stories of U.S. veterans across military branches and eras.',kind='Veterans museum and memorial')
 if i=='c42a2ffe14add548':f['description']='Represents real estate investment trusts and the publicly traded real estate industry; operates under the Nareit name.'
 if i=='15796533ca3f49ef':f['description']='Professional association supporting court reporters, captioners, and related legal-record services.'
 if i=='5d580a6928e5bfe3':f['description']='Labor union representing federal employees and advocating for their workplace interests.'
 if i=='dba8945e7861c45f':f['notes']='Confirmed as the National Spine & Pain Centers brand. The unsuffixed filing does not identify one operating affiliate.'
 if i=='7327cb71daad95c7':
  f.update(review_outcome='confirmed',notes='Nestlé USA’s official coupon policy explicitly names Nestlé USA, Inc.; Inc and unsuffixed original variants identify the same U.S. organization.',identity_evidence='Exact Inc entity named in official company coupon redemption policy.')
  s.append(src('https://www.nestleusa.com/coupon-policy','Policy explicitly includes Nestlé USA, Inc. among the named Nestlé affiliated companies.'))
 if i=='e9b4c74cc163827c':
  f.update(review_outcome='confirmed',notes='Investment-manager presentation published by Nebraska Investment Council explicitly names New Mountain Capital, L.L.C.; punctuation variants preserved.',identity_evidence='Manager-authored government-hosted presentation identifies New Mountain Capital, L.L.C. and its investment-manager role.')
  s.append(src('https://nic.nebraska.gov/sites/default/files/doc/6.d.%20PUBLIC%20New%20Mtn%20VII%20-%20Manager.pdf','Presentation identifies New Mountain Capital, L.L.C. and/or its affiliates as investment managers.'))
 if i=='b0044e55337d1759':
  f['notes']='Official September 2017 newsletter explains the change from NYU Langone Medical Center to NYU Langone Health as of July 20, 2017. Confirmed institution/health-system name, not a claim that all hospital affiliates are one legal entity.'
  s.append(src('https://nyulangone.org/files/publication_issues/news-views-september-2017.pdf','September 2017 newsletter describes former NYU Langone Medical Center and new NYU Langone Health name as of July 20.'))
 if i=='e11f11e9b71ff361':
  f['ownership']='Nonprofit';s.append(src('https://balletcenter.nyu.edu/faqs/donations/','NYU center states gifts fall under New York University 501(c)(3) tax-exempt organization.'))
 if i=='0c12b7eb3abf0297':f['ownership']='Unknown'
 if f['review_outcome']=='confirmed':f['website_status']='verified'
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append({'id':i,'decision':f['review_outcome'],'notes':f['notes']})
(r/'featured76-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured76-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed identities:',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()))
