import json,datetime
from pathlib import Path
r=Path('work/research-2026');p=json.loads((r/'reviewed.json').read_text()); rows=[]
def add(i,desc,url,evidence,ownership='Unknown',legal=''):
 rows.append(dict(id=i,description=desc,url=url,evidence=evidence,ownership=ownership,legal_form=legal))
add('09ba466746941267','DuPont entity associated with specialty materials and products.','https://www.iana.org/whois?q=.dupont','IANA identifies the exact DuPont Specialty Products USA, LLC and 974 Centre Road, Wilmington, matching the filed entity and address. The registry links dupont.com. This confirms identity, not ultimate ownership.',legal='LLC')
add('06db573ef06e7701','Provides enterprise IT, consulting and engineering services.','https://investors.dxc.com/investor-news/news-details/2026/DXC-Launches-One-of-Its-Most-Powerful-Growth-Engines-DXC-Engineering/default.aspx','Official June 2026 release identifies DXC Technology Company and its NYSE: DXC listing, and describes enterprise technology and engineering services.','Publicly traded','Corporation')
add('df529e3fefcf7dd2','Modifies and operates aircraft for specialized government and commercial missions.','https://www.navair.navy.mil/osbp/node/1281','NAVAIR supplier profile names Dynamic Aviation Group, Inc., links its website, and gives 1402 Airport Road, Bridgewater, matching the original registration.',legal='Corporation')
add('3cedecf72f09ee7c','Supplies explosives and blasting services for mining and construction.','https://www.dynonobel.com/disclaimer/','Official website terms identify Dyno Nobel Inc. explicitly. This supports the exact filed Inc. entity; no parent ownership is inferred.',legal='Corporation')
for i in ['217951c4b81d06f9','56c42fcf045a5703']:
 add(i,'Manufactures and distributes essential oils and wellness products through independent sellers.','https://media.doterra.com/us/en/forms/wellness-advocate-terms-and-conditions.pdf','Official US agreement expressly defines doTERRA International, LLC as dōTERRA and gives 389 S 1300 W, Pleasant Grove. Original filings use both the brand and exact LLC. This confirms US brand/entity linkage without including foreign affiliates.',legal='LLC')
add('265ab1f81ed763a4','Offers an app that lets workers access earned wages before payday.','https://www.earnin.com/','Current official site confirms the EarnIn brand and earned-wage-access activity. Footer separately names Activehours, Inc. and EarnIn US1 LLC; retain brand scope rather than claiming those entities are identical.')
add('43bf9bc63b7d035c','National nonprofit supporting people with disabilities, older adults, veterans and families.','https://www.easterseals.com/about-us/financials','Official financials page identifies Easter Seals, Inc. doing business as Easterseals, 501(c)(3) status, and 141 W Jackson Blvd Suite 1400A, Chicago, matching a filed address. Independent affiliates remain separate.','Nonprofit / tax-exempt (501(c)(3))','Nonprofit corporation')
(r/'featured56-root-before.json').write_text(json.dumps({x['id']:p[x['id']] for x in rows},indent=2,ensure_ascii=False)+'\n')
for x in rows:
 a=p[x['id']];a.update(description=x['description'],ownership=x['ownership'],legal_form=x['legal_form'],review_outcome='confirmed',website_status='verified',identity_evidence=x['evidence'],notes=x['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced')
 a['sources'].append(dict(url=x['url'],label='Primary identity evidence',claim=x['evidence']))
(r/'featured56-root-decisions.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
for f,compact in [(r/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:f.write_text(json.dumps(p,ensure_ascii=False,indent=None if compact else 2)+('' if compact else '\n'))
print('Saved',len(rows),'confirmed identities')
