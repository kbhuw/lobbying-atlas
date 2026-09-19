import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));reviews=json.load(open(r/'government119-first40-review.json'));before={};dec=[]
notes={
1:'The coalition’s November 9, 2018 comments hosted by NTIA name the exact 21st Century Privacy Coalition and describe its privacy-policy advocacy. This confirms historical organizational identity; current legal status and governance remain unverified.',
3:'Oregon’s July 30, 2026 tissue-bank register names Acesso Biologics at 8905 W Post Road, Suite 220, Las Vegas, matching the disclosed address. Registration confirms identity, not clinical effectiveness or ownership.',
7:'A federal government publication quotes the exact Alliance for Biopharmaceutical Competitiveness and Innovation in connection with tax-policy advocacy. Current standalone website, legal form and ownership remain unverified.',
9:'The CFPB’s organization-specific rulemaking-petition page and Michigan legislative testimony identify exact American Association of Consumer Credit Professionals. Current standalone website and tax status remain unverified.',
15:'The National Park Service identifies exact Antelope Point Holdings LLC doing business as Antelope Point Marina & Resort, providing Lake Powell marina services. This establishes the concessioner identity and trade name; current ownership remains unverified.',
17:'The federal SBIR company portfolio identifies exact Argo Space Corp, its El Segundo address and UEI XCDRBUPW2EK3, with in-space transport awards. It is distinct from the unrelated argodesign design agency.',
24:'The NPPES record identifies exact Azorna Healthcare LLC, NPI 1144933342, the DBA Azorna Hospice and Palliative Care and community-based hospice taxonomy. It confirms provider identity rather than quality of care or ownership.',
26:'Bay County’s official Florida government website explicitly identifies the Bay County Board of County Commissioners and its county-government responsibilities. This is a government body.',
27:'An Oregon regulatory filing identifies exact Better Life Health Inc. and describes wholly owned Remedy Meds and Prime Health Platform subsidiaries. This establishes the holding-company identity; its own ownership and standalone website remain unverified.',
29:'The CFTC’s January 3, 2022 order identifies exact Delaware Blockratize Inc., headquartered in New York and doing business as Polymarket.com at that time. This historical identity does not establish the current platform’s legal operator or ownership.',
31:'Hanover Borough’s official government website identifies Borough of Hanover at 33 Frederick Street, York County, Pennsylvania. This confirms the Pennsylvania municipal government, distinct from other Hanovers.',
32:'A California legislative hearing agenda names counsel for exact Botanicals for Better Health and Wellness in its botanical-products policy session. This supports organizational identity and advocacy activity, not tax status or the safety of botanical products.',
37:'La Paz County’s official sanitary-sewer information names Buckskin Sanitary District and its service area between the CRIT reservation and Parker Dam. Identity and local service function are established; the specific legal governance classification was not rechecked.'}
assert not (r/'featured120-before.json').exists()
for n,note in notes.items():
 x=reviews[n];i=x['id'];assert p[i]['name']==x['original_name'];assert p[i]['review_outcome']!='confirmed'
 before[i]=json.loads(json.dumps(p[i]));own='Government body' if n in [26,31] else x['ownership']
 p[i].update(description=x['description'],ownership=own,notes=note,identity_evidence=note,review_outcome='confirmed',checked_at='2026-09-13',as_of='2026-09-13')
 # Preserve existing website/logo verification; this is an identity review only.
 sources={s['url']:s for s in p[i]['sources']}
 good={e['url'] for e in x['fetched_evidence'] if e['http_status']==200}
 for s in x['sources']:
  if s['url'] in good:sources[s['url']]=dict(s,label='Government primary evidence')
 p[i]['sources']=list(sources.values());dec.append(dict(id=i,name=p[i]['name'],decision='confirmed',ownership=own,notes=note,fetched_evidence=x['fetched_evidence']))
(r/'featured120-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured120-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('13 government-source identities saved; websites/logos preserved')
