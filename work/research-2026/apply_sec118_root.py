import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));reviews=json.load(open(r/'sec-remaining117-next50-review.json'));before={};dec=[]
notes={
16:'Metropolitan Life Insurance Company’s 2025 annual report identifies the exact New York corporation as wholly owned by MetLife Inc. The insurer and its listed parent remain separate.',
17:'MGM’s SEC subsidiary exhibit names exact MGM Public Policy, LLC, incorporated in Nevada. The parent website is a group website; a separate operating function has not been independently established.',
22:'Rocket Lab’s June 2026 financial reporting states that the acquisition of all Motiv Space Systems Inc. equity closed May 26, 2026. The completed transaction supports subsidiary classification.',
23:'MBIA’s 2025 annual report explicitly identifies National Public Finance Guarantee Corporation as an indirect wholly owned subsidiary. It stopped pursuing new policies in 2017 and now services and remediates its existing portfolio.',
26:'NOVONIX’s SEC report names exact NOVONIX Anode Materials LLC, formerly PUREgraphite LLC. Although originally a joint venture, its consolidated entity table lists 100% ownership; the historical joint-venture label is not used as current ownership.',
39:'Primerica’s SEC annual report explicitly includes exact PFS Investments Inc. among three principal direct or indirect wholly owned US subsidiaries. It is the group’s broker-dealer and registered investment adviser.',
41:'Premier’s August 19, 2025 subsidiary exhibit lists exact Delaware Premier Healthcare Solutions Inc.; footnote 1 explicitly states it is wholly owned by Premier Inc. The ownership evidence is dated to that exhibit.',
48:'Regal Rexnord’s December 31, 2024 significant-subsidiary exhibit lists exact Regal Beloit America Inc., incorporated in Wisconsin. Ownership evidence is dated to the exhibit.',
49:'Regions’ SEC annual report explicitly identifies Regions Bank as an Alabama state-chartered Federal Reserve member bank, supervised by the Federal Reserve and Alabama State Banking Department. The exact bank identity is confirmed; this review does not establish its current ownership percentage.'}
assert not (r/'featured118-before.json').exists()
for n,note in notes.items():
 x=reviews[n];i=x['id'];assert p[i]['name']==x['original_name'];assert p[i]['review_outcome']!='confirmed'
 before[i]=json.loads(json.dumps(p[i]));own='Unknown' if n in [49] else ('Subsidiary' if n in [26,39] else x['ownership'])
 p[i].update(description=x['description'],ownership=own,notes=note,identity_evidence=note,review_outcome='confirmed',checked_at='2026-09-13',as_of='2026-09-13')
 # Preserve existing website/logo verification; this is an identity review only.
 sources={s['url']:s for s in p[i]['sources']}
 good={e['url'] for e in x['fetched_evidence'] if e['http_status']==200}
 for s in x['sources']:
  if s['url'] in good:sources[s['url']]=dict(s,label='SEC primary evidence')
 p[i]['sources']=list(sources.values());dec.append(dict(id=i,name=p[i]['name'],decision='confirmed',ownership=own,notes=note,fetched_evidence=x['fetched_evidence']))
(r/'featured118-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured118-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('9 independently checked SEC identities saved; website/logo statuses preserved')
