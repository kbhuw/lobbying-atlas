import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'))
rows={
'ef8cc1da96f69148':('https://cifanet.org/','The official site identifies the Council of Infrastructure Financing Authorities as a national not-for-profit organization representing Clean Water and Drinking Water State Revolving Funds. It advocates water-infrastructure funding and provides professional development and information. The association is distinct from the state-federal funds themselves. Broken animated counters are not used as data.'),
'3eed4e3a8dbfe47a':('https://www.ciab.com/about','The official About page identifies the Council of Insurance Agents & Brokers, also called CIAB or The Council, as an association of commercial property/casualty and employee-benefits brokerages. Its activities include government affairs, professional development and market intelligence. The separately described Council Foundation’s 501(c)(3) classification is not assigned to this association.'),
'fc2839b090584d1d':('https://www.copaa.org/page/about','The official About page names Council of Parent Attorneys and Advocates, Inc. as an independent nonprofit 501(c)(3) organization supporting education rights for students with disabilities. It provides training, systemic advocacy and a member referral directory; it explicitly does not directly represent individual families.'),
'60f7d39dded240c8':('https://www.kerncounty.com/government/board-of-supervisors/general-board-information/board-of-supervisors-meeting-information-and-schedule','Kern County’s official Board of Supervisors page identifies it as a California general-law county governed by five elected supervisors. It gives the county administrative center in Bakersfield. Exact county-government identity is confirmed; individual officeholder names are not required for this classification.'),
'50c96565179d9310':('https://www.lakecountyil.gov/5023/About-Us','The official About page identifies Lake County government in northeastern Illinois, created by the Illinois legislature in 1839. It describes county services, county-board budget and legislative responsibilities. This confirms the specific Illinois county, rather than another jurisdiction named Lake County.'),
'95951185a308dcbc':('https://www.mauicounty.gov/DocumentCenter/View/153586/2025-Charter','The county-hosted 2025 Charter, Article I section 1-1, explicitly establishes the County of Maui as a body politic and corporate in the State of Hawaii. This independently confirms the county-government identity; the phrase body corporate does not classify it as a private company.'),
'94cc516a87358a63':('https://tularecounty.ca.gov/county/about','The official About Tulare County page identifies the California county, its 1852 incorporation and general-law government. Exact county-government identity confirmed. Undated population and historical agricultural-production figures are not repeated as current statistics.')
}
b=r/'featured324-before.json';assert not b.exists();b.write_text(json.dumps({i:p[i] for i in rows},indent=2,ensure_ascii=False)+'\n')
for i,(u,n) in rows.items():
 n+=' Indexed official source body reviewed September 14, 2026; direct retrieval was blocked or unavailable.'
 p[i].update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-14',identity_evidence=n,notes=n)
 p[i]['sources'].append({'url':u,'label':'Indexed official source body reviewed September 14, 2026','claim':n})
p['fc2839b090584d1d']['legal_form']='Nonprofit corporation'
p['fc2839b090584d1d']['description']='Nonprofit association of parents, attorneys, advocates and allied professionals supporting education rights for students with disabilities through training, policy advocacy and referrals.'
(r/'featured324-decisions.json').write_text(json.dumps({i:p[i] for i in rows},indent=2,ensure_ascii=False)+'\n')
(r/'reviewed.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
print('Seven exact operating identities confirmed; no logo or ownership guesses added.')
