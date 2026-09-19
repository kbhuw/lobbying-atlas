import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));reviews=json.load(open(r/'government120-next50-review.json'));before={};dec=[]
notes={
4:'Idaho’s Department of Water Resources names exact Cat Creek Energy LLC in proceedings for water-permit applications. This confirms the project developer’s legal identity, not approval of every permit or operation of a power plant.',
11:'Central Pines Regional Council’s official website identifies the regional council, its board, member support and local-government programs. Public here means a governmental organization, not a stock-market listing.',
14:'EPA’s facility registry explicitly names CF&I Steel LP doing business as Rocky Mountain Steel Mills at its Pueblo facility. This verifies the legal name and trade name; historical EVRAZ references do not establish the current ownership chain.',
18:'New York’s April 13, 2007 tax opinion names exact Church Communities Inc. and describes its then-recognized section 501(d) religious or apostolic organization status. Current status and any relationship to Church Communities International or the Bruderhof website remain unverified.',
24:'Albuquerque’s official cabq.gov website independently confirms the New Mexico municipal government and its city services.',
27:'Boulder’s official bouldercolorado.gov website independently confirms the Colorado municipal government and its city services.',
28:'Brea’s official cityofbrea.gov website identifies its California city council and municipal services.',
36:'Emeryville’s official emeryvilleca.gov website identifies the California municipal government.',
39:'Flagstaff’s official flagstaff.az.gov website identifies the Arizona municipal government.',
40:'Fontana’s official fontanaca.gov website identifies the California municipal government and its city projects.',
41:'Gainesville’s official Florida government website matches the Gainesville, FL location in the original registration evidence. This record remains distinct from other cities named Gainesville.',
43:'Gresham’s official greshamoregon.gov website confirms the Oregon municipal government.',
47:'Jackson’s official jacksonms.gov website identifies the Mississippi municipal government, matching the state explicitly included in this record’s name.'}
assert not (r/'featured121-before.json').exists()
for n,note in notes.items():
 x=reviews[n];i=x['id'];assert p[i]['name']==x['original_name'];assert p[i]['review_outcome']!='confirmed'
 before[i]=json.loads(json.dumps(p[i]));own='Government body' if n in [11,24,27,28,36,39,40,41,43,47] else ('Unknown' if n==14 else x['ownership'])
 p[i].update(description=x['description'],ownership=own,notes=note,identity_evidence=note,review_outcome='confirmed',checked_at='2026-09-13',as_of='2026-09-13')
 # Preserve existing website/logo verification; this is an identity review only.
 sources={s['url']:s for s in p[i]['sources']}
 good={e['url'] for e in x['fetched_evidence'] if e['http_status']==200}
 for s in x['sources']:
  if s['url'] in good:sources[s['url']]=dict(s,label='Government primary evidence')
 p[i]['sources']=list(sources.values());dec.append(dict(id=i,name=p[i]['name'],decision='confirmed',ownership=own,notes=note,fetched_evidence=x['fetched_evidence']))
(r/'featured121-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured121-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('13 government-source identities saved; websites/logos preserved')
