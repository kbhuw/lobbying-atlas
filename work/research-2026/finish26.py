import json,pathlib,copy,gzip
r=pathlib.Path('work/research-2026');p={};inputs={}
for s in 'abc':
 x=json.load(open(r/f'general-round26-{s}-researched.json'));p.update({v['id']:v for v in x} if isinstance(x,list) else x);inputs.update({v['id']:v for v in json.load(open(r/f'general-round26-{s}-input.json'))})
for s in 'ab':p.update(json.load(open(r/f'general-round26-{s}-corrections.json')))
def fix(k,desc=None,website=None,own='Unknown',source=None,claim=None,kind=None,out='partial'):
 v=p[k]
 if desc:v['description']=desc
 if website is not None:v['website']=website
 if kind:v['kind']=kind
 v.update(ownership=own,review_outcome=out)
 if claim:
  v.update(identity_evidence=claim,notes=claim);v['sources']=copy.deepcopy((inputs[k].get('profile') or {}).get('sources',[]))+[dict(url=source or website,label='Primary evidence',claim=claim)]
fix('a158c9b510892ff8','Reports manufacturing and selling ballistic armor, night-vision goggles, and protective equipment. Its exact legal identity and official website remain unconfirmed.','',source='https://lda.gov/api/v1/clients/55847/?format=json',claim='LDA self-reported business is protective equipment. A similarly named German toolmaker is excluded because its identity is not established as this client.',kind='Business')
fix('292633d75cdb0900','An education-focused holding company according to its lobbying registration. Its portfolio, owners, and official website have not been independently established.','',source='https://lda.gov/api/v1/clients/69172/?format=json',claim='LDA identifies the exact name and self-reported education holding-company activity; unrelated accounting-firm evidence was excluded.',kind='Business')
fix('f803e961dc001fa7','Financial-services client disclosed as Brian Dror CPA, Inc. A standalone official website and ownership have not been established.','',source='https://lda.gov/api/v1/clients/67804/?format=json',claim='Exact LDA client record reports financial-services activity.',kind='Business')
fix('b1a379a74dceec89','Indigo Global Development manages infrastructure, energy, agriculture, and water projects for emerging-market clients. This filing names Bridgeway Advocacy as its representative.','https://indigoglobalusa.com/',source='https://indigoglobalusa.com/',claim='Official website names Indigo Global Development Inc., a U.S. company with a New Orleans address and project-management operations. Ownership remains unverified.',kind='Business')
p['b1a379a74dceec89']['name']='Indigo Global Development (via Bridgeway Advocacy)'
fix('0ee7b2373db821ee','Provides early-childhood education, child welfare, family support, and youth services in Illinois. Formerly Children’s Home & Aid.','https://www.brightpoint.org/',own='Nonprofit / tax-exempt',source='https://www.brightpoint.org/about-us/who-we-are/about-brightpoint/',claim='Official Brightpoint Illinois site matches the LDA Illinois location and child/family services. Excludes the Indiana community-action organization and wireless distributor.',kind='Nonprofit',out='confirmed')
fix('e75e65ff5dad01cd','Supplies lottery systems, technology, and services. Formerly named IGT Global Solutions Corporation.','https://www.brightstarlottery.com/',source='https://careers.brightstarlottery.com/content/PrivacyPolicy/?locale=en_US',claim='Official Brightstar applicant notice names Brightstar Global Solutions Corporation and its lottery website; current exact ownership remains held pending subsidiary-list validation.',kind='Business')
p['e75e65ff5dad01cd']['sources'].append(dict(url='https://lei.bloomberg.com/leis/view/549300Q4QZEOJMM3MV46',label='LEI issuer registry',claim='Registry identifies exact Brightstar Global Solutions Corporation and its previous legal name IGT Global Solutions Corporation, changed July 1, 2025.'))
fix('5aca58282d7f4885','Develops and operates utility-scale power systems combining clean generation, energy storage, and power-management technology.','https://brightnightpower.com/',source='https://brightnightpower.com/',claim='BrightNight official site describes utility-scale clean-power systems; exact US LLC ownership is not established.',kind='Business')
fix('6e09fa4c8b6a6ea3','Service entity associated with the Brighthouse life-insurance and annuity group.','https://www.brighthousefinancial.com/',own='Subsidiary / affiliated entity',source='https://www.sec.gov/Archives/edgar/data/1685040/000119312525101812/d921731dars.pdf',claim='Brighthouse annual report identifies Brighthouse Services LLC as an indirect wholly owned subsidiary and employee benefit-plan sponsor.',kind='Business')
fix('98de56f6854031f4','Healthcare management and insurance-services entity within the former Bright Health group.','',own='Subsidiary / affiliated entity',source='https://www.sec.gov/Archives/edgar/data/1671284/000167128425000004/ex211_listingofsubsidiarie.htm',claim='SEC subsidiary exhibit identifies Bright Health Management Inc. as a Delaware entity in the group; current standalone site not established.',kind='Business')
for k in ['3e471757420dfb4b','982d808535d894ff']:fix(k,'Develops and manufactures pharmaceutical ingredients and medicines using advanced production technology in the United States.','https://brightpathlabs.com/',source='https://brightpathlabs.com/',claim='Official Bright Path site describes pharmaceutical manufacturing and drug-supply-chain work, not diagnostic testing.',kind='Business')
fix('14529cd17f8774f1','Home-health and hospice-care client in California. The home-health entity is listed by California HCAI in Redlands; the combined hospice label remains partly unresolved.','',source='https://hcai.ca.gov/facility/bright-sky-home-health-care-inc/',claim='California HCAI identifies the exact home-health agency in Redlands. The proposed brightskycare.com site returned no usable identity content and is withheld.',kind='Healthcare provider')
fix('86125c60130a5999','Advocacy client disclosed as Building Resilient Infrastructure & Developing Greater Equity. Its independent website and organizational structure remain unconfirmed.','',source='https://lda.gov/filings/public/filing/cf652d24-3409-427a-98cc-4784ce33dacf/print/',claim='Original LDA filing identifies the exact BRIDGE name and Ballard Partners as its representative. Guessed bridge4equity.org is excluded.',kind='Advocacy organization')
k='0593081923ccbbcc';p[k].update(ownership='Nonprofit / tax-exempt',review_outcome='confirmed',identity_evidence='Broward College catalog explicitly identifies its Foundation as the designated 501(c)(3) charitable fundraising organization.');p[k]['sources'].append(dict(url='https://catalog.broward.edu/college-information/broward-college-foundation/',label='Official college catalog',claim=p[k]['identity_evidence']))
# Normalize taxonomy; unproven private ownership is not inferred from an LLC or business website.
for k,v in p.items():
 o=v['ownership'].lower()
 if 'not independently' in o or 'unknown' in o or 'not separately' in o or 'not established' in o:v.update(ownership='Unknown',review_outcome='partial')
 elif o.startswith('publicly traded'):v['ownership']='Publicly traded'
 elif 'subsidiary' in o:v['notes']=v.get('notes','')+' '+v['ownership'];v['ownership']='Subsidiary / affiliated entity'
 elif o.startswith('501') or o=='nonprofit':v['ownership']='Nonprofit / tax-exempt'
 elif o.startswith('public entity') or o.startswith('public local'):v['ownership']='Government body'
 elif o.startswith('alaska native'):v['ownership']='Alaska Native corporation'
 elif o.startswith('privately held') or (v['ownership']=='Private company' and k not in ['a61044188643b2f8','ffcade7a3182db70']):v.update(ownership='Unknown',review_outcome='partial')
 if k in ['a2dbab96b24da501','0c14593bd068b8d2','d4d1e0f51a14b7fe']:
  v.update(ownership='Nonprofit / tax-exempt',website='https://www.breakthrought1d.org/about/');v['sources'].append(dict(url='https://www.breakthrought1d.org/for-the-media/press-releases/breakthrough-t1d-is-now-breakthrough-t1d/',label='Official JDRF rebrand announcement',claim='The official release is titled JDRF is now Breakthrough T1D and describes its type-1 diabetes mission.'))
 if v['ownership']=='Unknown' and v['review_outcome']=='confirmed':v['review_outcome']='partial'
 v['sources']+= [s for s in (inputs[k].get('profile') or {}).get('sources',[]) if s not in v['sources']]
 if not v['sources']:
  z=json.load(gzip.open(f'lobbying-map/public/data/reports/{k[:2]}.json.gz','rt'))[k][0];v['sources']=[dict(url=f"https://lda.gov/filings/public/filing/{z['id']}/print/",label='Original disclosure',claim='Identifies disclosed client name.')]
# Readable represented-client names, original filing aliases remain in directory.
for k,n in {'7dea0f814a1897f4':'Grounded Solutions Network (via Breakaway)','c4e7a34a547b2a92':'Codan Communications (via Brian Glackin & Associates)','001fe16c43cefcfe':'Empirical Systems Aerospace (via Brian Glackin & Associates)','2e997dbd7c963af2':'Save Our Standards (via Bridge Street Group)','bedc292b5cbf346a':'U.S. Chamber Institute for Legal Reform (via Bridge Street Group)'}.items():p[k]['name']=n
(r/'general-round26-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
