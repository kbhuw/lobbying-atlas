import json, pathlib, copy
r=pathlib.Path('work/research-2026'); p=json.load(open(r/'reviewed.json'))
xs=json.load(open(r/'verified-sites135-next100-review.json')); before={}; decisions=[]
assert not (r/'featured134-before.json').exists()
fix={
1:'Makes access equipment such as powered ascenders, ladders, poles and hooks for military, public-safety and industrial users.',
3:'Develops Neutron, an AI workbench for searching nuclear-industry documents and supporting document review and regulatory workflows.',
20:'Helps consumers refinance vehicle loans and arrange auto lease buyouts.',
22:'An automotive safety coalition working to improve traffic safety, including driver alcohol-detection technology.',
25:'Provides community electricity service and electrification programs in Alameda and San Joaquin counties, California.',
37:'A correctional-technology group whose affiliates provide communications, security and payment services for incarcerated people and facilities.',
42:'Provides military and commercial aviation training and training support.',
43:'An alternative asset manager investing in commercial aircraft and engines; its affiliated Aircraft Managers company handles aircraft leasing.',
63:'Organizes astronaut missions to the International Space Station and develops commercial space-station infrastructure and spacesuits.',
67:'Operates a Wisconsin ethanol and grain-processing facility being developed into an advanced biorefinery, as part of ClonBio Group.',
83:'An individual physician listed by Redeemer Health as practicing internal medicine in Bensalem, Pennsylvania.',
92:'Provides location-based threat intelligence and risk assessments for corporate security, defense and law-enforcement users.'}
special={
3:'Corrected a false website and logo match: atomiccanyon.com belongs to an unrelated accounting business. The nuclear-AI company uses atomic-canyon.com; its About page names Atomic Canyon, Inc. and describes Neutron. The replacement logo is the wordmark in that official page header.',
8:'Atticus terms explicitly identify Atticus Labs, Inc. and Atticus Law, P.C. together as service providers; the legal entities remain distinct.',
43:'The official page explicitly distinguishes Aviator Capital Management, LLC, the asset manager, from Aviator Capital Aircraft Managers, LLC, the leasing company.',
63:'The company distinguishes current ISS missions from development of Axiom Station and spacesuits. Development is not treated as proof of an operating independent station.',
67:'Corrected the unsupported equipment-manufacturer description. The official site describes the Wisconsin ethanol facility and its biorefinery development, explicitly links ClonBio Group as its parent, and names Aztalan Bio LLC in the footer. Planned expansion is not presented as completed.',
80:'The exact Bankers Life Insurance Company website states court-ordered liquidation effective November 30, 2024, under the North Carolina Insurance Commissioner. This is not a generic match to other Bankers Life brands.',
82:'The official About page describes combustion-engine development and manufacturing and states that Baker Engineering is a 100% tribally owned business of Waseyabek.',
83:'The provider directory identifies the exact named physician and internal-medicine practice. This is an individual, not a company; the source does not substantiate the proposed nephrology specialty.'}
extra=json.load(open(r/'featured134-corrections-evidence.json'))
for n,v in enumerate(xs):
 if v['decision']!='confirmed':continue
 i=v['id']; assert p[i]['name']==v['original_name'] and p[i]['review_outcome']!='confirmed'
 before[i]=copy.deepcopy(p[i]); note=special.get(n,'Official organization body text identifies this organization and supports the activity described here. Existing ownership evidence is retained; no ownership is inferred from its name.')
 p[i].update(description=fix.get(n,v['description']),notes=note,identity_evidence=note,review_outcome='confirmed',checked_at='2026-09-13',as_of='2026-09-13')
 ev=v['fetched_evidence']; e=ev[0]; assert e['http_status']==200
 if n in (3,67):
  e=extra[0 if n==3 else 1];ev=[dict(url=e['url'],http_status=e['http_status'],exact_excerpt=e['text'],cache_path=e['cache_path'])]
 if n==3:
  p[i].update(website='https://www.atomic-canyon.com/',website_status='verified',logo_url='https://www.atomic-canyon.com/images/logo-white.webp',logo_source_url='https://www.atomic-canyon.com/about/',logo_kind='logo',logo_status='official_site_asset',logo_background='dark')
  p[i]['sources']=[s for s in p[i]['sources'] if 'atomiccanyon.com' not in s['url']]
 if n==67:p[i].update(ownership='Subsidiary',kind='Ethanol and biorefinery company')
 if n==82:p[i]['ownership']='Subsidiary'
 if n==92:p[i]['kind']='Risk intelligence software company'
 ss={s['url']:s for s in p[i]['sources']};ss[e['url']]={'url':e['url'],'label':'Official organization evidence','claim':note};p[i]['sources']=list(ss.values())
 decisions.append(dict(id=i,name=p[i]['name'],decision='confirmed',notes=note,fetched_evidence=ev))
(r/'featured134-before.json').write_text(json.dumps(before,indent=2)+'\n')
(r/'featured134-decisions.json').write_text(json.dumps(decisions,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
print(len(decisions),'identity confirmations saved; wrong Atomic Canyon website/logo replaced')
