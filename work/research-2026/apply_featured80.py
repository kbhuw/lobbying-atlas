import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def source(u,c):return {'url':u,'label':'Primary organization evidence','claim':c}
extra={
'b87e5adc2acf1b5a':('https://www.qinetiq.com/-/media/23f13013973e438f9cc8ce678bc18161.ashx','2026 annual report lists QinetiQ Inc. among group subsidiaries.'),
'65f2d6ba7932dea7':('https://qorvo.gcs-web.com/press-releases','July 28, 2026 earnings release identifies Qorvo as Nasdaq QRVO.'),
'3fa37c9f9cb31776':('https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm','June 2026 quarterly report confirms IPO closed June 5, 2026; distinguish listed Inc. from separately filed LLC.'),
'444d4bbf71d0913f':('https://www.rei.com/newsroom/c/sustainability','Official newsroom identifies REI as a consumer cooperative.'),
'4c20f6a76ef680ea':('https://ir.redcatholdings.com/_assets/_b14aa56c05d802532772b54eae076ba2/redcatholdings/news/2026-02-19_Red_Cat_to_Ring_the_Nasdaq_Opening_Bell_of_Friday__212.pdf','Company February 2026 release identifies Red Cat Holdings Inc. as Nasdaq RCAT.'),
'fc4dc89f0f44f22c':('https://richs.com/mindy-rich-named-chairman-of-rich-holdings-inc/','Official announcement identifies Rich Products Corporation as family-owned private business and Rich Holdings Inc. as corporate parent.'),
'99c3a701764b929b':('https://www.rolex.com/en-us/legal-notices/privacy-notice','Official privacy controller is ROLEX SA, Swiss company CH-660.0.012.920-4, Geneva.'),
'064cff322f450231':('https://ro.co/privacy-policy/','September 3, 2026 privacy notice identifies Roman Health Ventures Inc. and affiliated operating companies under Ro.'),
'a9cec62312ea39e8':('https://rsmus.com/','Official site identifies RSM US LLP as the U.S. member firm; independent global member firms remain distinct. Filed unsuffixed brand retained.'),
'e5fb53aa93282742':('https://www.sec.gov/Archives/edgar/data/1830081/000121390026070201/ea0295237-8k_rumble.htm','SEC current report documents legal name change from Rumble Inc. to RUM Group Inc. effective June 18, 2026; Nasdaq RUM.')}
for d in json.load(open(r/'featured80-first10.json'))+json.load(open(r/'featured80-middle10.json')):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','ownership','website']};f.update(review_outcome='confirmed',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[source(d['official_url'],d['exact_official_excerpt'])]
 if i in extra:
  u,c=extra[i];s.append(source(u,c));f.update(notes=c,identity_evidence=c)
 if f['ownership']=='Government entity':f['ownership']='Government body'
 if i=='b87e5adc2acf1b5a':f['ownership']='Subsidiary'
 if i in ['3fa37c9f9cb31776','4c20f6a76ef680ea','e5fb53aa93282742']:f['ownership']='Public company'
 if i=='fc4dc89f0f44f22c':f['ownership']='Private company'
 if i=='99c3a701764b929b':f['legal_form']='SA'
 if i=='064cff322f450231':f['legal_form']='Corporation'
 if i=='a9cec62312ea39e8':f['description']='RSM is an assurance, tax, and consulting brand. Its U.S. member firm is RSM US LLP; global member firms are separate legal entities.'
 if i=='e5fb53aa93282742':f['description']='Video-platform and cloud-services company filed as Rumble Inc.; renamed RUM Group Inc. effective June 18, 2026.'
 if i=='d096e404eaa9ec7b':
  f.update(logo_url='https://www.qlarant.com/wp-content/uploads/2024/02/Qlarant_R_logo_Wht2C_with_BestTag_11_21_2018.png',logo_source_url='https://www.qlarant.com/',logo_kind='logo',logo_status='official_site_asset',logo_background='dark');s.append(source('https://www.qlarant.com/','Official header logo fetched and visually verified: white Qlarant wordmark, yellow mark, tagline.'))
 if i=='3fa37c9f9cb31776':
  u='https://ir.quantinuum.com/news-releases/news-release-details/quantinuum-announces-pricing-upsized-initial-public-offering-0';f.update(logo_url='https://mma.prnewswire.com/media/2655950/6002341/Quantinuum_Logo.jpg',logo_source_url=u,logo_kind='logo',logo_status='official_site_asset',logo_background='light');s.append(source(u,'Official issuer press release links Quantinuum logo on press-distribution CDN; fetched and visually verified.'))
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append({'id':i,'decision':f['review_outcome'],'notes':f['notes']})
(r/'featured80-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured80-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed:',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()))
