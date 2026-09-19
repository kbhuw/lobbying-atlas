import json,pathlib,copy,collections
root=pathlib.Path(__file__).resolve().parents[2];base=root/'work/research-2026/identity-wave39-bulk';path=root/'work/research-2026/reviewed.json';p=json.loads(path.read_text());matches=json.loads((base/'matches.json').read_text()); byid={x['id']:x for x in matches}; decisions=json.loads((base/'agent-next25.json').read_text())
overrides={'4155afb4facfc7cb':('confirm','Full matched page explicitly lists SNF Holding Company / SNF Polydyne, 1 Chemical Plant Road, Riceboro, GA.'),'1eb9a87f1cf435f3':('confirm','Contact page explicitly identifies Space Nuclear Power Corp, including copyright, at the filed Los Alamos address.'),'19dd4b85f078672a':('hold','South Bow group contact does not establish the exact Infrastructure Operations subsidiary.'),'6da188d6b7189ce2':('hold','Exact LLC identity remains to be corroborated beyond operating brand.'),'600573e528382b01':('hold','Exact incorporated entity remains to be corroborated beyond operating brand.'),'18d7cfcb0665ba88':('hold','Exact LLC identity remains to be corroborated beyond operating brand.'),'003942092fa7a2b5':('hold','Exact LLC identity remains to be corroborated beyond operating brand.')}
for d in decisions:
 if d['id'] in overrides:d['decision'],d['evidence']=overrides[d['id']]
localholds={97:'Next FX page does not establish StageFX identity.',98:'Filed Ltd differs from official Inc; no legal continuity established.',105:'STL group page does not establish exact US incorporated subsidiary.'}
for i in range(95,111):
 x=matches[i];decisions.append({'id':x['id'],'decision':'hold' if i in localholds else 'confirm','evidence':localholds.get(i,'Official name, activity and address corroborate the filed organization.'),'url':x['matches'][0]['page_url']})
last=json.loads((base/'agent-last6.json').read_text())
for d in last:
 if d['id']=='e193e77a5bf3b2d6':d.update(decision='confirm',evidence='Official site uses both Stueve Siegel Hanson and Stueve Siegel Hanson LLP at the filed address; omitted suffix is not a conflicting legal form.')
decisions+=last
assert len(decisions)==47 and len({d['id'] for d in decisions})==47
backup={d['id']:copy.deepcopy(p[d['id']]) for d in decisions};(base/'final47-before.json').write_text(json.dumps(backup,indent=2,ensure_ascii=False))
for d in decisions:
 if d['decision']!='confirm':continue
 x=p[d['id']];assert x['review_outcome']=='partial',(d['id'],x['review_outcome']);m=byid[d['id']]['matches'][0];r=m['registration'];proof=f"{d['evidence']} Registration: {r['client_name']}, {r['address']}, {r['city']}, {r['state']}. Evidence: {r['archive']} / {r['member']}."
 x.update(status='sourced',review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12')
 old=x.get('identity_evidence','');x['identity_evidence']=(old+' ' if isinstance(old,str) else json.dumps(old)+' ')+proof
 for s in [{'url':d['url'],'label':'Official organization identity and address','claim':proof},{'url':r['source_url'],'label':f"House registration archive: {r['member']}",'claim':f"Filed client {r['client_name']} at {r['address']}, {r['city']}, {r['state']}; {r['description']}"}]:
  if s not in x.setdefault('sources',[]):x['sources'].append(s)
renames={'f4d93ca3aed0c91f':'St. Croix Regional Medical Center','fb7910f03ead8211':'StationMD','510b1da6ada6c9db':'SteerBridge','75639623d83526c1':'STIDD Systems, Inc.','f66c5a13fb8760b6':'StormQuant Inc.','363f1785ff00d7a4':'SOLVD Health','724123aded934476':'SpaceRake, Inc.','93030b9413ae5f74':'Sparacino PLLC','e65e4384328acf61':'Southeast Coastal Ocean Observing Regional Association (SECOORA)'}
for id,name in renames.items():p[id]['name']=name
x=p['b00feb2b3e1a457b'];x['notes']=x.get('notes','')+' The official website now uses Mighty Therapeutics and explicitly states that it was formerly named Stealth BioTherapeutics. The lobbying-era name is retained.';x['website']='https://mightytx.com/';x['sources'].append({'url':'https://mightytx.com/','label':'Official rename disclosure','claim':'Mighty Therapeutics explicitly identifies its former name as Stealth BioTherapeutics and lists 123 Highland Ave, Needham.'})
for f,pretty in [(path,True),(root/'lobbying-map/research/reviewed-2026.json',False),(root/'outputs/2026-research-trial/profiles.json',True)]:f.write_text(json.dumps(p,indent=2 if pretty else None,ensure_ascii=False))
(base/'final47-decisions.json').write_text(json.dumps(decisions,indent=2,ensure_ascii=False))
mp=root/'lobbying-map/research/verified-entity-merges.json';merges=json.loads(mp.read_text());ids=['7c7784645ddfd8a3','9277a17d593b76f1'];assert not any(set(ids)&set(m['source_ids']) for m in merges)
(base/'rtx-merges-before.json').write_text(json.dumps(merges,indent=2));rationale='RTX Corp and affiliates and RTX Corporation and Affiliates are spelling variants of the same organization at 1000 Wilson Blvd, Arlington, VA. Both registration records describe aerospace and defense. Original identities and filing histories are retained.'
merges.append({'canonical_id':ids[0],'source_ids':ids,'rationale':rationale,'sources':[{'url':'https://www.rtx.com/contacts','claim':rationale}]+[{'url':byid[id]['matches'][0]['registration']['source_url'],'claim':byid[id]['matches'][0]['registration']['member']} for id in ids],'reviewed_at':'2026-09-12'});mp.write_text(json.dumps(merges,indent=2,ensure_ascii=False))
covered=[]
for f in ['agent35-decisions.json','local35-decisions.json','final47-decisions.json']:
 a=json.loads((base/f).read_text());covered += [d['id'] for d in a]
assert len(covered)==117 and set(covered)==set(byid)
print('Final47',collections.Counter(d['decision'] for d in decisions));print('All profiles',collections.Counter(x['review_outcome'] for x in p.values()))
