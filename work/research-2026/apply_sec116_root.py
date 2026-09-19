import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));reviews=json.load(open(r/'sec-remaining115-first40-review.json'));before={};dec=[]
notes={
3:'The 2017 Amazon SEC subsidiary list names exact Delaware Amazon Corporate LLC at 100% ownership at that date. This confirms the historical legal identity; current ownership percentage remains unverified. Retained separately from Amazon.com Inc.',
4:'American Electric Power’s December 31, 2025 subsidiary list explicitly names American Electric Power Service Corporation, incorporated in New York. The listed parent and service subsidiary remain separate.',
6:'American Water’s 2025 annual report explicitly identifies American Water Works Service Company, Inc. as a wholly owned subsidiary providing support and operational services to the group.',
8:'Compass’s January 9, 2026 SEC filing states that its acquisition closed that day and Anywhere Real Estate Inc. survived as a wholly owned subsidiary. The former public listing is historical.',
12:'Avis Budget Group’s 2025 annual report explicitly names Avis Budget Car Rental, LLC as its subsidiary and debt issuer. The parent’s CAR stock listing does not belong to this LLC.',
15:'Bio-Rad’s June 30, 2026 quarterly filing confirms the exact Hercules, California issuer and NYSE stock registration. Identity and public-company status are independently supported.',
16:'Biohaven Ltd.’s December 31, 2025 subsidiary exhibit explicitly lists Biohaven Pharmaceuticals, Inc., incorporated in Delaware. This entity is distinct from its listed parent.',
17:'Bitcoin Depot’s 2025 annual report explicitly records that Lux Vending LLC merged into Delaware Bitcoin Depot Operating LLC on June 30, 2023, with the latter surviving. The exact operating identity is confirmed; its current immediate ownership chain is not established by the excerpt reviewed.',
18:'Black Hills Corporation’s June 30, 2026 quarterly filing confirms its South Dakota identity, Rapid City address and NYSE BKH stock registration.',
20:'The SEC-filed 2024 subsidiary exhibit names Bright Health Management, Inc., incorporated in Delaware. This is dated subsidiary evidence; current immediate ownership and a standalone website remain unverified.',
21:'Brighthouse’s 2024 annual report identifies Brighthouse Services, LLC as the group’s internal services and payroll company. The exact entity is confirmed from dated group reporting; the listed parent is separate.',
22:'BrightSpring’s 2025 annual report names BrightSpring Health Services, Inc., its Louisville address and Nasdaq BTSG stock registration.',
25:'An August 2022 SEC-filed announcement identifies Captura Biopharma, Inc. and its development of oral chelators for radiation contamination and heavy-metal poisoning. A signed proposed business combination does not establish closing, current public status, or regulatory approval of its treatments.',
26:'The 2024 SEC Form D names Carbon GeoCapture Corp, Wyoming incorporation, and its Laramie business address. This confirms identity; Form D alone does not establish current ownership.',
28:'SM Energy’s SEC filing states that its sale of South Texas assets to exact Delaware Caturus Energy, LLC completed April 30, 2026. This proves the entity and transaction, not Caturus’s own ownership structure.',
32:'Comstock’s 2023 annual report explicitly identifies CHCI Asset Management, LC as one of its real-estate-focused operating subsidiaries. The ownership evidence is dated to that report.',
34:'Chubb’s SEC annual reporting documents the March 26, 2024 conversion of Chubb INA Holdings Inc. to Chubb INA Holdings LLC. This row preserves the historical Inc. filing name; neither the subsidiary nor its former name is treated as the listed parent.',
37:'A December 2020 SEC page explicitly names Citadel Enterprise Americas LLC, formerly Citadel LLC. Citadel Securities’ 2023 financial statements separately name this entity among providers of administrative and investment-related services. Current ownership is unverified.',
38:'Citadel Securities’ 2023 SEC-filed financial statements explicitly name Citadel Enterprise Americas Services LLC among providers of administrative and investment-related services. It remains separate from Citadel Enterprise Americas LLC; current ownership is unverified.',
39:'Citigroup’s December 31, 2005 principal-subsidiary exhibit explicitly lists Citigroup Washington, Inc., incorporated in the District of Columbia. This confirms historical identity; it does not establish the current ownership chain.'}
assert not (r/'featured116-before.json').exists()
for n,note in notes.items():
 x=reviews[n];i=x['id'];assert p[i]['name']==x['original_name'];assert p[i]['review_outcome']!='confirmed'
 before[i]=json.loads(json.dumps(p[i]));own='Unknown' if n in [17,20,21,39] else x['ownership']
 p[i].update(description=x['description'],ownership=own,notes=note,identity_evidence=note,review_outcome='confirmed',checked_at='2026-09-13',as_of='2026-09-13')
 # Preserve existing website/logo verification; this is an identity review only.
 sources={s['url']:s for s in p[i]['sources']}
 good={e['url'] for e in x['fetched_evidence'] if e['http_status']==200}
 for s in x['sources']:
  if s['url'] in good:sources[s['url']]=dict(s,label='SEC primary evidence')
 p[i]['sources']=list(sources.values());dec.append(dict(id=i,name=p[i]['name'],decision='confirmed',ownership=own,notes=note,fetched_evidence=x['fetched_evidence']))
(r/'featured116-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured116-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('20 independently checked SEC identities saved; website/logo statuses preserved')
