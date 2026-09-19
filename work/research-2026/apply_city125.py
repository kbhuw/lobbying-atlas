import json,pathlib,gzip,hashlib,copy,collections
r=pathlib.Path('work/research-2026');site=pathlib.Path('lobbying-map');p=json.load(open(r/'reviewed.json'));extras=json.load(open(site/'research/profiles.json'));splits=json.load(open(site/'research/verified-entity-splits.json'));meta=json.load(open(site/'research/publication-metadata.json'));base={x['id']:x for x in json.load(gzip.open(site/'research/directory-base.json.gz'))['companies']};v=json.load(open(r/'government124-city-split-validation.json'))
assert not (r/'featured125-before.json').exists();before={'profiles':{},'extra_ids':[],'splits':copy.deepcopy(splits),'metadata':copy.deepcopy(meta)};audit=[]
state_names={'CA':'California','OH':'Ohio','WA':'Washington','FL':'Florida'}
for g in v['groups']:
 sid=g['source_id'];original=base[sid];before['profiles'][sid]=copy.deepcopy(p[sid]);assert not any(s['source_id']==sid for s in splits)
 reports=[]
 for member in original['members']:reports+=json.load(gzip.open(site/f'public/data/reports/{member[:2]}.json.gz'))[member]
 allids={x['id'] for x in reports};current={x['id'] for x in reports if x['year']==2026};assert current=={x['filing_id'] for x in g['rows']}
 groups=collections.defaultdict(list);sources=[]
 for row in g['rows']:
  a=json.load(open(row['cache_path']));assert a['filing_uuid']==row['filing_id'];c=a['client'];state=c['state'];assert state==row['client_state'] and c['ppb_state']==state;assert c['name'].strip() in original['aliases'];groups[state].append(a['filing_uuid']);sources.append({'url':row['source_url'],'label':'Original filing client jurisdiction','claim':f"Client {c['id']} names {c['name']} in {state_names[state]}; both client state fields agree."})
 used={x for xs in groups.values() for x in xs};groups['unassigned']=sorted(allids-used);children=[]
 for j,(state,ids) in enumerate(sorted(groups.items())):
  cid=sid if j==0 else hashlib.sha256(f'{sid}:filing-jurisdiction:{state}'.encode()).hexdigest()[:16]
  assert cid==sid or cid not in p and cid not in extras and cid not in base
  name=original['name']+' ('+(state_names[state] if state!='unassigned' else 'unassigned historical filings')+')'
  child={'id':cid,'name':name,'aliases':original['aliases'],'members':original['members'],'filing_ids':ids,'issues':[]};children.append(child)
  profile=copy.deepcopy(p[sid]);profile.update(name=name,kind='Government',ownership='Government body',status='sourced',website='',website_status='unresolved',logo_url='',logo_source_url='',logo_kind='',logo_status='unresolved',checked_at='2026-09-13',as_of='2026-09-13',sources=sources)
  if state=='unassigned':
   profile.update(description=f'Historical filings under {original["name"]} whose municipal jurisdiction has not been assigned. These totals must not be attributed to one city.',review_outcome='partial',notes='All filings not individually checked for client jurisdiction remain here. No assignment is inferred from registrant address or the shared city name.')
  else:
   note=f'Only individually checked 2026 filings with matching client state and principal-place-of-business state {state} are included. Historical filings not checked remain in a separate unassigned group.'
   profile.update(description=f'Municipal government of {original["name"].replace("City of ","")}, {state_names[state]}.',review_outcome='confirmed',notes=note)
   if state=='OH':profile.update(website='https://lakewoodoh.gov/',website_status='verified')
   if state=='FL':profile.update(website='https://www.miami.gov/',website_status='verified')
  profile['identity_evidence']=profile['notes']
  if cid==sid:
   old_status=p[cid]['status']
   if old_status!=profile['status']:meta['counts'][old_status]-=1;meta['counts'][profile['status']]+=1
   p[cid]=profile
  else:extras[cid]=profile;before['extra_ids'].append(cid);meta['counts']['sourced']+=1;meta['total']+=1
 assert sorted(x for c in children for x in c['filing_ids'])==sorted(x['id'] for x in reports)
 splits.append({'source_id':sid,'mode':'filings','rationale':'Distinct municipalities shared a normalized name. Every 2026 filing is assigned by its own verified client jurisdiction; all unchecked historical filings remain unassigned. Every original filing is preserved exactly once.','sources':sources,'children':children});audit.append({'source_id':sid,'total_filings':len(reports),'checked_2026':len(used),'children':[{'id':c['id'],'name':c['name'],'filings':len(c['filing_ids'])} for c in children]})
(r/'featured125-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured125-decisions.json').write_text(json.dumps(audit,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(site/'research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
for f,x in [('profiles.json',extras),('verified-entity-splits.json',splits),('publication-metadata.json',meta)]: (site/'research'/f).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(audit,indent=2))
