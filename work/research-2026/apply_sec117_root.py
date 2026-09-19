import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));reviews=json.load(open(r/'sec-remaining116-next40-review.json'));before={};dec=[]
notes={
2:'FirstEnergy’s 2025 annual report names the exact FirstEnergy Service Company and its corporate-support function. A June 2003 SEC order explicitly identifies it as the service-company subsidiary; the parent issuer remains separate.',
10:'A February 26, 2020 letter submitted to the SEC names exact Global Trading Systems, LLC at 545 Madison Avenue, New York, identifies gtsx.com and describes its automated market-making business. Current ownership is unverified.',
15:'The SEC Form D names exact Delaware Intelligent Mapping, LLC and its Park City, Utah address. The legal identity is confirmed; neither LLC form nor a financing filing establishes current ownership.',
17:'An April 2, 2025 submission to the SEC explicitly names Kiln USA Inc and describes its cryptocurrency-staking infrastructure. This conflicts with the generic legal-services activity in the lobbying record; that discrepancy is retained. Current ownership and the official website relationship remain unverified.',
21:'Lithium Americas’ December 31, 2025 corporate structure lists Nevada LAC Management LLC at 100%. A December 20, 2024 management-services agreement independently names the same manager. The listed LAC issuer is its parent.',
27:'Lincoln Electric’s 2023 subsidiary and joint-venture exhibit explicitly names Lincoln Electric Automation, Inc. in the United States. This confirms the legal entity within the group; the combined list alone does not establish exact ownership percentage or control.',
28:'Liquidia’s 2025 annual report explicitly identifies Liquidia Technologies as its wholly owned subsidiary and predecessor for SEC reporting. Its historical LQDA listing ended November 18, 2020; the current ticker belongs to Liquidia Corporation.',
32:'The SEC Form D identifies exact Lynch Regenerative Medicine, LLC, Tennessee incorporation in 2023, and its Franklin business address. Identity is confirmed; current ownership remains Unknown.',
38:'Match Group’s December 31, 2024 subsidiary exhibit explicitly names Match Group Holdings I, LLC, incorporated in Delaware. The parent issuer remains separate.'}
assert not (r/'featured117-before.json').exists()
for n,note in notes.items():
 x=reviews[n];i=x['id'];assert p[i]['name']==x['original_name'];assert p[i]['review_outcome']!='confirmed'
 before[i]=json.loads(json.dumps(p[i]));own='Unknown' if n in [27] else x['ownership']
 p[i].update(description=x['description'],ownership=own,notes=note,identity_evidence=note,review_outcome='confirmed',checked_at='2026-09-13',as_of='2026-09-13')
 # Preserve existing website/logo verification; this is an identity review only.
 sources={s['url']:s for s in p[i]['sources']}
 good={e['url'] for e in x['fetched_evidence'] if e['http_status']==200}
 for s in x['sources']:
  if s['url'] in good:sources[s['url']]=dict(s,label='SEC primary evidence')
 p[i]['sources']=list(sources.values());dec.append(dict(id=i,name=p[i]['name'],decision='confirmed',ownership=own,notes=note,fetched_evidence=x['fetched_evidence']))
(r/'featured117-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured117-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('9 independently checked SEC identities saved; website/logo statuses preserved')
