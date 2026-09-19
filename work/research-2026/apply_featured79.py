import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return {'url':u,'label':'Official organization evidence','claim':c}
for d in json.load(open(r/'featured79-first10.json'))+json.load(open(r/'featured79-middle10.json')):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','ownership','website']};f.update(review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced');s=[src(d['official_url'],d['exact_official_excerpt'])]
 if f['ownership'] in ['Government','Government entity']:f['ownership']='Government body'
 if i=='f04e8ee7aaadbb5b':
  f.update(ownership='Private company',notes='Premier’s take-private acquisition by Patient Square Capital completed November 25, 2025; former Nasdaq listing is not current ownership.')
  s.append(src('https://www.ropesgray.com/en/news-and-events/news/2025/11/patient-square-capital-completes-take-private-acquisition-of-premier-inc','Transaction counsel reports completed acquisition and cessation of Nasdaq trading November 25, 2025.'))
 if i=='e6c998fae0d6fa97':
  f.update(logo_url='https://prep4all.org/wp-content/themes/bushwick-digital/assets/images/prep4all-logo.svg',logo_kind='logo',logo_status='official_site_asset',logo_source_url='https://prep4all.org/',logo_background='dark');s.append(src('https://prep4all.org/','Homepage-labelled PrEP4All logo fetched and visually verified, white/cyan wordmark for dark background.'))
 if i=='9eb92943450fd0a0':f['notes']='Current PrePass Safety Alliance identity supported. Formerly reported as HELP Inc. is preserved as the filing’s reporting history, not asserted as a legal rename.'
 if i=='f1346cb9f34b7b29':
  f.update(review_outcome='confirmed',notes='Official terms name Pretium Partners, LLC and define website operator scope to include affiliates.',identity_evidence='Official website terms identify exact Pretium Partners, LLC entity.');s.append(src('https://pretium.com/terms-of-use/','Terms name Pretium Partners, LLC; Pretium collectively may include affiliates.'))
 if i=='fb398293a4663a0e':
  f.update(review_outcome='confirmed',notes='Official homepage explicitly names Pride Mobility Products Corporation and describes mobility equipment.',identity_evidence='Official homepage title and text give the exact Corporation name.');s=[src('https://www.pridemobility.com/','Homepage identifies Pride Mobility Products Corporation and mobility-product manufacturing.')]
 if i=='941730629a234d6e':
  f.update(ownership='Unknown',description='Logistics real-estate business conducted through Prologis, L.P., the operating partnership whose general partner is Prologis, Inc.',notes='Company annual report distinguishes the Inc. REIT parent from Prologis, L.P., the operating partnership named in these aliases. Parent public listing is not assigned to the LP.')
  s.append(src('https://ir.prologis.com/financials/annual-reports/content/0001193125-24-081532/0001193125-24-081532.pdf','2023 annual report identifies Prologis, Inc. as general partner of Prologis, L.P., the operating partnership.'))
 if i=='a44847bcac7c03cd':f.update(review_outcome='partial',notes='Current Protect Democracy United activity is supported; the former United to Protect Democracy relationship needs primary historical evidence beyond the filing label.')
 if i=='7586a458051244cc':f['description']='Spirits producer, marketer, importer, and distributor. Exact Inc. identity and parent relationship remain unresolved.'
 if i=='9265b4e819c1f1f6':
  s=[src('https://www.sec.gov/Archives/edgar/data/78239/000007823926000021/pvh-20260201.htm','PVH Corp. annual report for fiscal year ended February 1, 2026 identifies the exact registrant and listed company.')];f['notes']='Verified correct PVH fiscal-year-ended February 1, 2026 SEC annual report; unverified December 31 URL from preliminary research discarded.'
 if f['review_outcome']=='confirmed':f['website_status']='verified'
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append({'id':i,'decision':f['review_outcome'],'notes':f['notes']})
(r/'featured79-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured79-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed identities:',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()))
