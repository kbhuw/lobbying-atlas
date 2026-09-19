import json,pathlib,copy
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured223-before.json').exists();before={};dec=[]
items={
'2f0a598260e19c64':('https://soundpharma.com/','The official homepage explicitly names Sound Pharmaceuticals, Inc. and describes it as a privately held biopharmaceutical company in Seattle. Its hearing-loss drug-development activity matches the filing. The treatments remain investigational; no efficacy or approval claims are inferred.',True),
'906ba6f6120a10b0':('https://rebelliondefense.com/privacy-policy','The current official privacy policy explicitly names Rebellion Defense, Inc. and affiliates, resolving the link between this exact filed entity and the Rebellion-branded domain. The homepage’s Rebellion Industries branding is not treated as evidence of a legal rename. Ownership remains unknown.',True),
'9649113e640f128c':('https://www.neros.tech/legal/privacy-policy','The official Neros privacy policy identifies Neros, Inc., matching the federal awardee and neros.tech domain. This supports the operating business represented as Neros Technologies in the lobbying disclosure. Icebreaker Strategies remains the disclosed intermediary; no ownership relationship is inferred.',True),
'a275308ae7608cba':('https://www.qualis-corp.com/our-history/','The official company overview confirms the Qualis engineering business but currently uses Qualis LLC in its body and footer, while the original lobbying label says Qualis Corporation. Formal entity continuity and current ownership remain unresolved; the current wording is recorded without assuming a corporate conversion.',False)}
for i,(url,n,c) in items.items():
 v=p[i];before[i]=copy.deepcopy(v);v.update(checked_at='2026-09-13',notes=n,identity_evidence=n)
 if c:v.update(review_outcome='confirmed',website_status='verified')
 if i=='2f0a598260e19c64':v['ownership']='Private company'
 v['sources'].append(dict(url=url,label='Official identity clarification',claim=n));dec.append(dict(id=i,confirmed=c,url=url,notes=n))
for k,v in [('before',before),('decisions',dec)]: (r/f'featured223-{k}.json').write_text(json.dumps(v,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('3 identities, 1 website, 1 ownership classification; Qualis discrepancy saved')
