import json,gzip
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));ids=['b8c49c385b1be7c5','4500491bc49df646']
b=r/'featured322-before.json';assert not b.exists();b.write_text(json.dumps({i:p[i] for i in ids},indent=2,ensure_ascii=False)+'\n')
u='https://commercialspace.org/news_events/commercial-space-federation-csf-launches-rebrand-reorg-and-integrate-compete-and-unleash-plan/'
n='The association’s official December 2024 announcement explicitly identifies Commercial Space Federation as the renamed Commercial Spaceflight Federation. It describes the same Washington, DC trade association advocating for the commercial space industry before Congress and the Administration. Both filing-name records are consolidated as one operating organization, with original source IDs and filings preserved. The separately mentioned political action committee is not merged. Tax classification remains unknown. Official announcement body retrieved September 14, 2026.'
s={'url':u,'label':'Official December 2024 rebrand announcement','claim':n}
for i in ids:
 p[i].update(review_outcome='confirmed',website='https://commercialspace.org/',website_status='verified',checked_at='2026-09-14',notes=n,identity_evidence=n,description='Trade association advocating federal policy for commercial space companies, including launch providers, satellite services, space stations and spaceports. Renamed from Commercial Spaceflight Federation in December 2024.',logo_url='https://commercialspace.org/wp-content/uploads/2024/10/CSF-logo-horizontal-2024-white.svg',logo_kind='logo',logo_status='official_site_asset',logo_source_url=u,logo_background='dark')
 p[i]['sources'].append(s)
mp=Path('lobbying-map/research/verified-entity-merges.json');m=json.load(open(mp));assert not any(set(ids)&set(x['source_ids']) for x in m)
(r/'featured322-merge-before.json').write_text(json.dumps(m,indent=2)+'\n')
d=json.load(gzip.open('lobbying-map/public/data/directory-v3.json.gz','rt'));cards={c['id']:c for c in d['companies'] if c['id'] in ids};assert len(cards)==2
(r/'featured322-cards-before.json').write_text(json.dumps(cards,indent=2)+'\n')
m.append({'canonical_id':ids[0],'source_ids':ids,'rationale':n,'sources':[s],'reviewed_at':'2026-09-14'})
mp.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
(r/'reviewed.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');(r/'featured322-decisions.json').write_text(json.dumps({i:p[i] for i in ids},indent=2,ensure_ascii=False)+'\n')
print('Two confirmed identities, one verified duplicate, current full logo.')
