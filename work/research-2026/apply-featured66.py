import json,copy
from pathlib import Path
p=Path('work/research-2026');d=json.load(open(p/'reviewed.json'));inp=json.load(open(p/'featured66-input.json'));before={x['id']:copy.deepcopy(d[x['id']]) for x in inp};dec=[]
def put(i,u,e,**kw):
 x=d[i];assert x['review_outcome']!='confirmed';x.update(review_outcome='confirmed',identity_evidence=e,notes=e,checked_at='2026-09-13',as_of='2026-09-13',website_status='verified',ownership='Unknown',**kw);x['sources']=[s for s in x.get('sources',[]) if s.get('label')=='Original lobbying disclosure']+[{'url':u,'label':'Primary identity evidence','claim':e}];dec.append({'id':i,'url':u,'evidence':e,**kw})
a=json.load(open(p/'featured66-first10.json'));assert {x['originalID'] for x in a}=={x['id'] for x in inp[:10]}
for x in a:
 if x['originalID'] not in ['10e796c80f11fbf6','7732b751da32c2d3','6324a90dfeb62bc2','a5aaa4ac13311aff']:continue
 put(x['originalID'],x['exact_quotes'][0]['url'],x['evidence'],kind=x['proposed']['kind'],website=x['proposed']['website'])
rows=[
('bfd0070c1d8a2bfe','https://synmax.com/privacy-policy/','Official July 2026 privacy policy explicitly identifies SynMax Inc. and its geospatial intelligence services. Original filing names Holly Strategies Inc. on behalf of SynMax Inc.; preserve the intermediary and represented-company scope.'),
('347bb1a48758bac3','https://ezaccess.com/policies/privacy-policy','Official privacy policy explicitly identifies EZ-ACCESS as a DBA of Homecare Products Inc., matching the filed legal company and accessibility equipment business.'),
('1cfb0f9297609690','https://www.prospera.co/privacy-policy-2025-07-04.pdf','Official 2025 privacy policy explicitly names Honduras Prospera Inc. as a Delaware corporation formerly Honduras Prospera LLC. This confirms the filed corporation without equating it to the zone administration, foundation or other affiliates.'),
('0f1f8b02e7754074','https://hts.hopper.com/legal/privacy-policy','Official HTS privacy policy explicitly identifies Hopper (USA) Inc., matching the original US corporation. The wider Hopper group and non-US affiliates are not substituted.'),
('d6b805c0f4972bae','https://www.hopskipdrive.com/privacy/','Official privacy policy updated November 12, 2025 explicitly names HopSkipDrive Inc. and its transportation platform, matching the original legal name.'),
('b84e981f04419df0','https://www.hopeforhemophilia.org/applications.html','Official Hope for Hemophilia applications page identifies Hope Charities in its site metadata and describes bleeding-disorder assistance, matching the original unsuffixed organization and activity. Tax-exempt status and legal form remain unverified.'),
('2ba07a57ad80c674','https://www.horizondefenseus.com/','Official Horizon Defense Solutions site matches the original unsuffixed organization name and defense engineering/government support activity. No legal suffix or ownership is inferred.'),
('2adc17b385b185a5','https://horizonleague.org/','Official Horizon League website identifies the athletic conference, matching the original unsuffixed organization. Tax-exempt status is not independently established in this review.')]
for i,u,e in rows:put(i,u,e)
d['a5aaa4ac13311aff']['ownership']='Nonprofit / tax-exempt';d['a5aaa4ac13311aff']['sources'].append({'url':'https://www.thehome.org/','label':'Official nonprofit statement','claim':'Official site states registered 501(c)(3) nonprofit organization.'})
x=d['6324a90dfeb62bc2'];x['ownership']='Public company (NYSE: HD)';x['sources'].append({'url':'https://ir.homedepot.com/investor-resources/faqs','label':'Official investor FAQ','claim':'Official FAQ confirms NYSE ticker HD and public-company status.'});x.update(logo_url='https://corporate.homedepot.com/themes/custom/bootstrap_thd/images/logo-site-header-homedepot.svg',logo_source_url='https://corporate.homedepot.com/',logo_status='official_site_asset',logo_kind='logo',logo_background='dark')
(p/'featured66-before.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n');(p/'featured66-root-decisions.json').write_text(json.dumps(dec,indent=2,ensure_ascii=False)+'\n')
for f,indent,nl in [(p/'reviewed.json',2,True),(Path('lobbying-map/research/reviewed-2026.json'),None,False),(Path('outputs/2026-research-trial/profiles.json'),2,True)]:f.write_text(json.dumps(d,ensure_ascii=False,indent=indent)+ ('\n' if nl else ''))
print('Confirmed',len(dec),'new logo 1')
