import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));reviews=json.load(open(r/'government121-next50-review.json'));before={};dec=[]
notes={
2:'Lake Wales’ official lakewalesfl.gov website identifies the Florida city and its commission. This matches the state-specific filing identity.',
18:'Miramar’s official miramarfl.gov website explicitly identifies the City of Miramar, Florida and its municipal boards. Its official website relationship is now verified.',
19:'Mission Viejo’s official missionviejo.gov website identifies the California municipal government and city services.',
20:'Monroe’s official monroewa.gov website explicitly identifies the City of Monroe, Washington. This record remains separate from other cities named Monroe.',
24:'Oakland’s official oaklandca.gov website explicitly identifies the California city and its services. The official website relationship is verified.',
36:'Salinas’ official salinas.gov website identifies the California municipal government and city services. The official website relationship is verified.',
44:'Tucson’s official tucsonaz.gov website identifies the Arizona municipal government and city services. The official website relationship is verified.',
48:'Waco’s official wacotx.gov website identifies the Texas municipal government and its city services. This verified current domain replaces the previously filed older domain.'}
assert not (r/'featured122-before.json').exists()
for n,note in notes.items():
 x=reviews[n];i=x['id'];assert p[i]['name']==x['original_name'];assert p[i]['review_outcome']!='confirmed'
 before[i]=json.loads(json.dumps(p[i]));own='Government body'
 p[i].update(description=x['description'],ownership=own,notes=note,identity_evidence=note,review_outcome='confirmed',checked_at='2026-09-13',as_of='2026-09-13')
 p[i]['website_status']='verified'
 if n==48:p[i]['website']='https://www.wacotx.gov/'
 sources={s['url']:s for s in p[i]['sources']}
 good={e['url'] for e in x['fetched_evidence'] if e['http_status']==200}
 for s in x['sources']:
  if s['url'] in good:sources[s['url']]=dict(s,label='Government primary evidence')
 p[i]['sources']=list(sources.values());dec.append(dict(id=i,name=p[i]['name'],decision='confirmed',ownership=own,notes=note,fetched_evidence=x['fetched_evidence']))
(r/'featured122-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured122-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('8 city identities saved; 5 website statuses upgraded')
