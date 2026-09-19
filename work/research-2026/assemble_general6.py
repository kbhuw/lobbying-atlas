import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round6-90-draft.json'))
for letter in 'abc':
 d=json.load(open(r/f'general-round6-{letter}-corrected.json'))
 if isinstance(d,list):d={v['id']:v for v in d}
 assert len(d)==30 and all(k in p for k in d)
 p.update(d)
def update(k,url,description,claim,source=None):
 v=p[k];old=v.get('website');v.update(website=url,description=description,status='sourced',review_outcome='partial',identity_evidence=claim)
 v['sources']=[s for s in v['sources'] if s.get('url') and s['url']!=old]
 v['sources'].append(dict(url=source or url,label='Primary organization evidence',claim=claim))
update('0babaad36e5337c2','https://albers.aero/','Provides aerospace and defense manufacturing, engineering, aircraft support and technology services.','Albers Aerospace official site identifies its industrial manufacturing, integrated defense solutions and special-projects businesses.')
update('e4285731dffa3cd7','https://albertvein.com/','Colorado medical practice diagnosing and treating vein and vascular conditions at clinics in Lone Tree and Colorado Springs.','Albert Vein Institute official site identifies the practice, its vein-care services and two Colorado locations.')
update('6e46985cc99587b3','https://www.strengthenfda.org/about-us','Coalition of patient, consumer, research and industry organizations advocating adequate funding and resources for the Food and Drug Administration.','Official about page identifies Alliance for a Stronger FDA and its advocacy for FDA appropriations.')
update('bea31b0bfa6104e1','https://www.acgbrands.com/en_US/acg-company-leadership','Consumer-products group managing a portfolio of outdoor, lighting and related product brands.','Official ACG Brands leadership page explicitly identifies Alliance Consumer Group and its brands.')
update('1483bc4b533bce08','https://www.alawitesassociation.org/','Advocacy organization representing the Alawite diaspora and advocating protection and inclusion of ethno-religious communities in Syria.','AAUS testimony submitted to USCIRF identifies the association, its president, mission and official website.','https://www.uscirf.gov/sites/default/files/11.18.25%20AAUS%20USCIRF%20Testimony.pdf')
update('c25141ffd31fa994','','Biopharmaceutical industry advocacy group participating in federal tax-policy debates. Its exact name appears in congressional lobbying records and a member company’s disclosed trade-association payments.','House registrant lookup identifies the exact alliance as a client of the Washington Tax & Public Policy Group.','https://lobbyingdisclosure.house.gov/lookup.asp?reg_id=37434')
p['c25141ffd31fa994']['sources'].append(dict(url='https://www.majoritywhip.gov/reconciliation/overall-support.htm',label='Alliance statement published by House Majority Whip',claim='The alliance expresses support for federal tax policies to encourage investment and innovation.'))
p['c25141ffd31fa994']['notes']='Current official website and legal ownership remain unverified; similarly named biopharma alliances were not substituted.'
v=p['e4b647b42ca664c5'];v['description']='Aerospace and defense contractor providing engineering, logistics, IT, cybersecurity and simulation services. The proposed website identifies All Points Logistics LLC; the filing uses the shortened name All Points LLC.';v['notes']='Exact shortened-name relationship remains partially verified; the website is All Points Logistics LLC in Merritt Island, Florida.'
v['sources']=[s for s in v['sources'] if 'allpointsllc.com' not in s.get('url','')];v['sources'].append(dict(url='https://allpointsllc.com/',label='All Points Logistics official site',claim='Official site identifies engineering, logistics, IT, cybersecurity and simulation services and the legal name All Points Logistics LLC.'))
for k,client,via,desc,url in [('24b37fd7f5150500','Power4PR','Alianza for Progress','Puerto Rico policy and community advocacy','https://www.power4puertorico.com/'),('7b161f1693160788','American Unity Fund','Allegiance Strategies','advocacy for LGBT Americans and religious freedom','https://www.americanunityfund.com/')]:
 v=p[k];v.update(name=f'{client} (via {via})',description=f'Represented in this disclosure by {via}: {client} works on {desc}.',website=url,review_outcome='partial',kind='Advocacy representation',ownership='Unknown');v['notes']='The website describes the represented client. The filing’s intermediary relationship is retained; these entities are not automatically merged.'
for k in ['08c3072cf3dfb46d','9cb95d35c6ba67fe','58c1d5f6244dbcbf','f3eded707fbb81ad','bb201fed0b9c2015']:
 v=p[k];v['description']='Individual named as a lobbying client in the disclosure archive. A separate organization profile and official business website have not been established.';v['notes']='Retained as an individual disclosure entry; no same-name company or personal website was assigned.';v['ownership']='Not applicable'
p['fd21b47329541ba5']['ownership']='Government body'
for v in p.values():
 old=v['ownership']
 if old.startswith('Public company ('):v['ownership']='Publicly traded'
 if old.startswith('Private company /'):v['ownership']='Private company'
 if old=='Subsidiary of Allegiant Travel Company':v['ownership']='Subsidiary of public company'
 if old=='Nonprofit / fiscally sponsored':v['ownership']='Nonprofit / tax-exempt'
 if old!=v['ownership']:v['notes']=v.get('notes','')+' '+old+'.'
 v['sources']=[s for s in v['sources'] if s.get('url','').startswith('https://')]
(r/'general-round6-90-draft.json').write_text(json.dumps(p,indent=2)+'\n')
