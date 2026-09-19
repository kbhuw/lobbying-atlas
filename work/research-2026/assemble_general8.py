import json,pathlib
r=pathlib.Path('work/research-2026');p={}
for l in 'abc':
 d=json.load(open(r/f'general-round8-{l}-corrected.json'));d={v['id']:v for v in d} if isinstance(d,list) else d;assert len(d)==30;p.update(d)
def fix(k,url,desc,claim,source=None):
 v=p[k];old=v.get('website');v.update(website=url,description=desc,review_outcome='partial',status='sourced',identity_evidence=claim)
 v['sources']=[s for s in v.get('sources',[]) if s.get('url') and s['url']!=old]
 v['sources'].append(dict(url=source or url,label='Primary organization evidence',claim=claim))
fix('489fb33c09ba566e','https://ambltc.com/','Industry advocacy group representing nursing-home operators and engaging policymakers on skilled-nursing and long-term-care services.','Ambassadors Group official site identifies its nursing-home operator advocacy and New Jersey office. This is distinct from the former student-travel company of the same name.')
p['489fb33c09ba566e']['notes']='The filing describes long-term-care advocacy, matching this operating group. The website footer names an LLC while tax records name an Inc.; exact legal structure remains uncertain.'
fix('dea8b08c5c53336c','https://www.amc-civil.com/what-we-do/','Infrastructure contractor specializing in heavy civil and marine construction, industrial demolition, construction inspection and project controls.','AMC Civil official services page identifies the contractor and its heavy civil, marine and demolition capabilities.')
fix('1f465a247cc706bd','https://www.americafa.org/','Advocacy organization whose lobbying disclosure describes work on a unified U.S. legal framework for cannabis, including hemp and marijuana.','Official website footer identifies America First Agriculture Inc.; the site currently has limited public information. Its policy activity is retained as self-reported filing context.')
fix('fc8b1ea8801ed819','https://amcot.org/','Organization of grower-owned cotton-marketing cooperatives promoting and marketing U.S. cotton internationally.','AMCOT official site identifies member cooperatives owned by American cotton growers and their U.S. cotton marketing activity.')
fix('259bfa07306bba6c','https://americafirstrefining.com/','Company developing a refinery in Brownsville, Texas, designed to process American shale oil using hydrogen-powered operations.','America First Refining official site describes its planned Brownsville refinery. Project plans are not treated as evidence of completed construction or operations.')
fix('4cb9972aced95fa4','https://www.amentum.com/','Public holding company providing engineering, technology and mission-support services for government and commercial customers.','Amentum Holdings Inc. identifies itself as the public issuer NYSE: AMTM in its third-quarter 2026 results.','https://ir.amentum.com/news/news-details/2026/Amentum-Reports-Third-Quarter-Fiscal-Year-2026-Results/default.aspx');p['4cb9972aced95fa4']['ownership']='Publicly traded'
v=p['5cc401d6425a344e'];v['ownership']='Subsidiary of public company';v['notes']='Amedisys became a UnitedHealth Group subsidiary when the acquisition closed on August 14, 2025. Required divestitures changed the combined service footprint.';v['sources'].append(dict(url='https://www.sec.gov/Archives/edgar/data/896262/000110465925078145/tm2523306d1_8k.htm',label='Amedisys acquisition closing filing',claim='Amedisys reports closing its merger with UnitedHealth Group on August 14, 2025, becoming a wholly owned subsidiary.'))
p['7b0dfd4d0bcf9cf2']['sources'].append(dict(url='https://www.agloan.com/terms-and-conditions/',label='American AgCredit legal terms',claim='Terms identify American AgCredit ACA, PCA and FLCA as operators of agloan.com.'))
for k in ['ee28081dc141859d','1052a91d28bbfa88','181a92be1b95cc6a','f9aee15766a7cc9f']:p[k]['featured']=True
for k,v in p.items():
 v.pop('id',None);v.setdefault('notes','');v.setdefault('legal_form','');v.setdefault('featured',False);v.setdefault('identity_evidence',v['notes'])
 v['sources']=[s for s in v['sources'] if s.get('url','').startswith('https://')]
 old=v['ownership']
 if old.startswith('Nonprofit /'):v['ownership']='Nonprofit / tax-exempt'
 elif old.startswith('Public company /'):v['ownership']='Unknown';v['review_outcome']='partial'
 elif old.startswith('Subsidiary of American Airlines'):v['ownership']='Subsidiary of public company'
 if old!=v['ownership']:v['notes']+=' '+old+'.'
assert len(p)==90
(r/'general-round8-90-draft.json').write_text(json.dumps(p,indent=2)+'\n')
s=(r/'check_general7.py').read_text().replace('general-round7','general-round8');(r/'check_general8.py').write_text(s)
