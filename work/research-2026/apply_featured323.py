import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'))
rows={
'c87d60d845b9109f':('https://ccwater.com/27/About-Us','The official About page identifies Contra Costa Water District as a public water agency serving central and eastern Contra Costa County, governed by five elected directors, with headquarters at 1331 Concord Avenue. Indexed official body reviewed September 14, 2026; exact public-agency identity and government classification confirmed.'),
'7a8ded6b87d05717':('https://www.ccrta.org/','The official transit authority homepage identifies Corpus Christi Regional Transportation Authority, its establishment in 1986, fixed-route and B-Line paratransit services, and Corpus Christi offices. Indexed official body reviewed September 14, 2026; exact operating public-transit identity confirmed. Undated ridership and route counts are not repeated as current statistics.'),
'954439c7d5de693b':('https://converus.com/history-of-converus/','The official company history explicitly states the December 12, 2013 renaming to Converus, Inc. and identifies its EyeDetect eye-behavior credibility-assessment technology. The current official newsroom footer also identifies Converus, Inc. Indexed official bodies reviewed September 14, 2026. Product accuracy and scientific-validation marketing claims are not independently verified here. Current equity ownership remains unknown.'),
'7f1dd0969a9cdc2d':('https://c4ip.org/about/','The official About page explicitly identifies the Council for Innovation Promotion as a coalition advocating intellectual-property rights through policy campaigns and stakeholder engagement. Direct official body retrieved September 14, 2026. Identity confirmed; its policy arguments are not independent factual conclusions and current tax classification remains unknown.'),
'a7cbef718d7dfb95':('https://www.caorc.org/about-us','The official CAORC About page and homepage identify the Council of American Overseas Research Centers and its research-center network, scholar support, fellowship and cultural-heritage activities. Official bodies reviewed September 14, 2026; homepage directly retrieved. Public and private funders are not treated as owners, and member-center legal forms are not assigned to the council.')
}
b=r/'featured323-before.json';assert not b.exists();b.write_text(json.dumps({i:p[i] for i in rows},indent=2,ensure_ascii=False)+'\n')
for i,(u,n) in rows.items():
 p[i].update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-14',identity_evidence=n,notes=n)
 p[i]['sources'].append({'url':u,'label':'Official organization evidence reviewed September 14, 2026','claim':n})
p['954439c7d5de693b']['legal_form']='Corporation'
p['c87d60d845b9109f']['website']='https://ccwater.com/'
p['a7cbef718d7dfb95'].update(logo_url=(r/'evidence323/caorc-logo-url.txt').read_text(),logo_kind='logo',logo_source_url='https://www.caorc.org/',logo_status='official_site_asset')
(r/'featured323-decisions.json').write_text(json.dumps({i:p[i] for i in rows},indent=2,ensure_ascii=False)+'\n')
(r/'reviewed.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
print('Five identities confirmed; full CAORC logo saved. ConServe Inc/LLC remains unresolved; Converus asset403 not assigned.')
