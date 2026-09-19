import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));reviews=json.load(open(r/'government122-next100-review.json'));before={};dec=[]
notes={
0:'West Memphis’ official municipal website confirms the Arkansas city government. This does not establish any similarly named organization.',
7:'The coalition’s comments submitted to USPTO explicitly name Coalition for 21st Century Patent Reform and describe its member manufacturers and patent-policy advocacy. Coalition identity is confirmed; nonprofit tax status is not inferred.',
8:'An October 2022 government-hosted submission names Coalition for Chemical Innovations and describes its chemical-industry stakeholders and TSCA policy mission. Its policy claims are attributed to the coalition; tax status remains unverified.',
11:'A congressional hearing record contains COFIR’s October 23, 2017 letter under the exact Coalition Organized for the Future of Insurance Regulation name. This establishes the historical insurance-policy coalition, not a current tax classification.',
18:'A congressional steel-industry hearing identifies the chair of exact Committee on Pipe and Tube Imports. This verifies the industry organization’s identity; it is not equated with a similarly named political committee.',
23:'The January 6, 2021 FHFA submission identifies exact Community Home Lenders Association and its small and midsized independent mortgage-bank membership. This confirms the historical association; current successor identity requires separate evidence.',
24:'Texas DIR’s historical contract record names exact Comprehensive Communication Services LLC and describes emergency-preparedness hardware and related services. The contract is marked inactive; this is not a claim of current contract eligibility.',
27:'The federal SBIR portfolio identifies exact Continuous Composites Inc. at its Coeur d’Alene, Idaho address. Identity and technology activity are corroborated; current ownership remains unverified.',
28:'An April 2015 DOE rulemaking submission names exact Contractors International Group on Nuclear Liability and describes its nuclear-supplier policy activity. The ad hoc group is not assumed to be a nonprofit corporation.',
32:'A Pennsylvania public payment schedule repeatedly names exact Cornell Abraxas Group LLC for professional education services. The exact provider identity is supported; current ownership and parent relationships remain unverified.',
35:'Kauai County’s official website identifies County of Kauai at 4444 Rice Street, Lihue, Hawaii. This is a county government.',
56:'HHS TAGGS identifies exact Eastern Plains Healthcare Consortium, UEI HAMWCHKUSNB5, at 111 6th Street in Hugo, Colorado. The record confirms identity and location; it does not establish nonprofit tax status.',
64:'A November 1, 2019 California BSCC grant application identifies exact Epidaurus DBA Amity Foundation, tax ID 77-0418201 and corporate number C1953746. The exact legal-name/DBA relationship is confirmed; current tax status requires the separate IRS evidence retained in the profile.',
67:'Victorville’s state-filed housing plan names exact ERNA Enterprises LLC among housing developers. This confirms local development identity, not current ownership.',
70:'A manufacturer submission to NHTSA names exact Evolution Electric Vehicles Inc., Chino address and low-speed vehicle activity. A manufacturer’s compliance statement is not an independent safety approval.',
81:'DOE’s project summary explicitly identifies Forge Battery as Forge Nano Inc.’s commercial lithium-ion battery-production subsidiary. The described facility was proposed; project funding information does not prove completion or disbursement.',
83:'Franklin County’s official Ohio government website confirms the state-specific county identity.',
84:'The federal SBIR portfolio identifies exact Freedom Flight Works Inc., San Diego address and UEI ZESAR93MFHA7, with parafoil-system awards. This confirms identity and activity; ownership remains unverified.',
92:'Nebraska’s official water-rights record names exact Gering-Fort Laramie Irrigation District and its Fort Laramie Canal system. The previously supplied gflid.org domain remains unverified.',
97:'A congressional funding record identifies exact Green Brook Flood Control Commission and its Green Brook Basin project in New Jersey. This confirms the commission’s historical identity and function; it does not establish the present project’s completion.'}
assert not (r/'featured124-before.json').exists()
for n,note in notes.items():
 x=reviews[n];i=x['id'];assert p[i]['name']==x['original_name'];assert p[i]['review_outcome']!='confirmed'
 before[i]=json.loads(json.dumps(p[i]));own='Unknown' if n==84 else x['ownership']
 p[i].update(description=x['description'],ownership=own,notes=note,identity_evidence=note,review_outcome='confirmed',checked_at='2026-09-13',as_of='2026-09-13')
 # Preserve existing website/logo verification; this is an identity review only.
 sources={s['url']:s for s in p[i]['sources']}
 good={e['url'] for e in x['fetched_evidence'] if e['http_status']==200}
 for s in x['sources']:
  if s['url'] in good:sources[s['url']]=dict(s,label='Government primary evidence')
 p[i]['sources']=list(sources.values());dec.append(dict(id=i,name=p[i]['name'],decision='confirmed',ownership=own,notes=note,fetched_evidence=x['fetched_evidence']))
(r/'featured124-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured124-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('20 government-source identities saved; websites/logos preserved')
