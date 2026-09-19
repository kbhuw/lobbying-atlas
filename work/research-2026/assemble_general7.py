import json,pathlib
r=pathlib.Path('work/research-2026');p={}
for l in 'abc':
 d=json.load(open(r/f'general-round7-{l}-corrected.json'));d={v['id']:v for v in d} if isinstance(d,list) else d;assert len(d)==30;p.update(d)
def fix(k,url,desc,claim,source=None,ownership='Unknown'):
 v=p[k];old=v.get('website');v.update(website=url,description=desc,ownership=ownership,review_outcome='partial',status='sourced',identity_evidence=claim,notes='Identity and activity corroborated by the cited source. Any remaining legal-entity or ownership uncertainty is retained.')
 v['sources']=[s for s in v.get('sources',[]) if s.get('url') and s['url']!=old]
 v['sources'].append(dict(url=source or url,label='Primary organization source',claim=claim))
fix('d595b8cfb60baaec','https://saveoursound.org/about/','Advocacy organization working to preserve Nantucket Sound’s ecology and traditional uses, improve water quality and prevent development it considers inappropriate.','Official Alliance to Protect Nantucket Sound about page identifies the organization and its conservation and preservation mission.')
fix('5d681d7807ac18f6','https://alppouch.com/pages/contact','Company selling tobacco-free nicotine pouches under the ALP brand.','Official ALP nicotine-pouch site identifies ALP Supply Co. in its contact information.')
fix('7711126e69ef191e','https://www.aointl.com/about-us/company-overview/','Leaf-tobacco merchant purchasing, processing, storing and shipping tobacco for manufacturers. Current operations use Alliance One International LLC, a Pyxus subsidiary; the archive retains the older Inc. name.','Official company overview identifies Alliance One International LLC as a leaf-tobacco merchant and Pyxus International subsidiary.')
p['7711126e69ef191e']['notes']='Current official site describes the LLC; the historic Inc. name also preceded Pyxus. The exact historical legal-entity continuity should not be inferred from the shared name.'
fix('f096614977369371','https://safetynetalliance.org/','Coalition of safety-net hospitals advocating Medicare and Medicaid policies and funding that support care for medically vulnerable communities.','The Alliance of Safety-Net Hospitals official site identifies the exact coalition, its members and its federal healthcare policy mission.')
fix('3b25e96fce25a46c','https://usij.org/about/','Coalition of inventors, startups, investors and research institutions advocating a stronger U.S. patent system.','USIJ official about page expands the acronym as Alliance of U.S. Startups & Inventors for Jobs and describes its patent-policy mission.')
fix('54371ca33c2fb045','https://modernizeprescribinginfo.com/about-us/','Coalition advocating electronic prescribing information for healthcare professionals in place of paper pharmaceutical labels.','Alliance to Modernize Prescribing Information official site describes its proposal for electronic approved labeling information.')
fix('dc1cbc548e3f63f3','','Membership organization supporting access to licensed Medicare insurance agents and education and improvement of its member agencies.','GoHealth’s 2026 proxy statement describes ALMIA as a nonprofit and states its purpose of supporting Medicare beneficiaries’ access to licensed insurance agents.','https://investors.gohealth.com/static-files/908c78eb-e2c5-4963-937f-fcd50ecba6c0',ownership='Nonprofit / tax-exempt')
fix('74308de5f0e904cb','https://buysaferx.pharmacy/about-asop-global/','Advocacy nonprofit working to combat illegal online drug sellers and improve access to safe medicines through research, education and policy.','ASOP Global official about page identifies Alliance for Safe Online Pharmacies as a Washington, D.C. 501(c)(4) organization.',ownership='Nonprofit / tax-exempt')
fix('f5cb13ced71c58f0','https://www.affuture.org/','Advocacy organization promoting artificial-intelligence development and adoption and opposing restrictions it considers obstacles to technological progress.','Alliance for the Future’s manifesto describes its coalition of entrepreneurs, technologists and policy experts and its advocacy for AI development.','https://www.affuture.org/manifesto/')
for k in ['2fb646fc42f0e72a','1ddb097f6f7148e7']:
 fix(k,'https://theabp.org/','Advocacy organization educating policymakers and the media about business partnerships and policies affecting those businesses.','Alliance for Business Partnerships official site describes its business-partnership advocacy. The filing’s spelling or singular-name variation is retained as an alias.')
 p[k]['sources'].append(dict(url='https://downloads.regulations.gov/IRS-2024-0028-0019/attachment_1.pdf',label='Alliance comment submitted to IRS',claim='Alliance for Business Partnerships submits comments about partnership tax rules under its own name and Washington, D.C. address.'))
 p[k]['notes']='The disclosed spelling or singular-name variant is associated with this group provisionally; no automatic legal-entity merge was made.'
fix('405b80eaef25fecd','https://allianceforinfrastructure.com/','Business coalition advocating a federal infrastructure bank and increased federal financing for U.S. infrastructure.','Official site identifies The Alliance for Financing U.S. Infrastructure Inc., its purpose and 501(c)(6) status.',ownership='Nonprofit / tax-exempt')
fix('e9905a95e1b8e317','https://www.ibm.com/','IBM is represented in this disclosure through Alliance of Professionals & Consultants. IBM provides business software, infrastructure and consulting services.','The filing identifies the represented client as IBM; APC’s official about page identifies the professional-services and staffing intermediary.','https://www.apcinc.com/about-apc/')
p['e9905a95e1b8e317']['name']='IBM (via Alliance of Professionals & Consultants)';p['e9905a95e1b8e317']['notes']='Website is the represented client IBM. The intermediary and principal are retained separately in the disclosure.'
for k,v in p.items():
 v.pop('id',None);v.setdefault('identity_evidence',v.get('notes',''));v.setdefault('notes','');v.setdefault('legal_form','');v.setdefault('featured',False)
 v['sources']=[s for s in v['sources'] if s.get('url','').startswith('https://')]
 old=v['ownership']
 if old.startswith('Nonprofit /'):v['ownership']='Nonprofit / tax-exempt'
 elif old.startswith('Subsidiary of Altria'):v['ownership']='Subsidiary of public company'
 elif old.startswith('Intermediary;'):v['ownership']='Unknown'
 elif old.startswith('Private company /'):v['ownership']='Private company'
 elif old in ['Public special district','Government / public district']:v['ownership']='Government body'
 if old!=v['ownership']:v['notes']+=' '+old+'.'
assert len(p)==90
(r/'general-round7-90-draft.json').write_text(json.dumps(p,indent=2)+'\n')
