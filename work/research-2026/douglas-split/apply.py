import json,gzip,pathlib,hashlib,datetime,copy
root=pathlib.Path('lobbying-map'); sid='db32ea46ccd83520'
def read(p):return json.loads(pathlib.Path(p).read_text())
def save(p,d):pathlib.Path(p).write_text(json.dumps(d,indent=2)+'\n')
master=read('work/research-2026/reviewed.json');extra=read(root/'research/profiles.json');splits=read(root/'research/verified-entity-splits.json')
assert not any(d['source_id']==sid for d in splits)
base=json.load(gzip.open(root/'research/directory-base.json.gz'));original=next(c for c in base['companies'] if c['id']==sid)
reports=json.load(gzip.open(root/'public/data/reports/db.json.gz'))[sid];groups={s:[] for s in ['CO','WA','NE','unassigned']};sources={s:[] for s in groups}
for r in reports:
 p=pathlib.Path('work/research-2026/government-api-pass')/(r['id']+'.json');d=read(p) if p.exists() else {};client=d.get('client',{});state=client.get('state')
 if state in groups and d.get('filing_uuid')==r['id']:
  groups[state].append(r['id']);sources[state].append({'url':f"https://lda.gov/api/v1/filings/{r['id']}/?format=json",'label':'Filing jurisdiction evidence','claim':f"Client {client['id']} reports Douglas County in {state}."})
 else:groups['unassigned'].append(r['id'])
assert all(r['id'] not in groups['unassigned'] for r in reports if r['year']==2026)
save('work/research-2026/douglas-split/profile-before.json',master[sid]);children=[]
names={'CO':'Colorado','WA':'Washington','NE':'Nebraska','unassigned':'unassigned historical filings'}
websites={'CO':'https://www.douglasco.gov/','WA':'https://www.douglascountywa.gov/'}
known={c['id'] for c in base['companies']}|set(extra)|set(master)
for state,ids in groups.items():
 if not ids:continue
 cid=sid if state=='CO' else hashlib.sha256((sid+':'+state).encode()).hexdigest()[:16]
 assert cid==sid or cid not in known
 name=f'Douglas County ({names[state]})';children.append(dict(id=cid,name=name,aliases=original['aliases'],members=original['members'],filing_ids=ids,issues=[]))
 p=copy.deepcopy(master[sid]);p.update(name=name,sources=sources[state],website=websites.get(state,''),ownership='Government' if state!='unassigned' else 'Unknown',legal_form='County government' if state!='unassigned' else '',status='sourced' if state!='unassigned' else 'unresolved',review_outcome='confirmed' if state in websites else 'partial' if state=='NE' else 'unresolved',website_status='verified' if state in websites else 'unresolved')
 p['description']=f'County government of Douglas County, {names[state]}.' if state!='unassigned' else 'Historical Douglas County filings whose jurisdiction has not yet been verified. These reports are not attributed to a single county.'
 if state=='CO':p['description']+=' Provides county services including public safety, transportation, public health and human services.'
 if state=='WA':p['description']+=' Administers county services including roads, land-use planning, public records and emergency services.'
 p['identity_evidence']='Each assigned filing was checked against its embedded LDA client state.' if state!='unassigned' else 'Exact source-name collision; these historical filings await individual jurisdiction verification.'
 p['notes']='Separated from a source-name group containing Colorado, Washington and Nebraska. Unchecked historical filings remain in a separate unassigned entry. Logo has not been verified.'
 if state in websites:p['sources'].append(dict(url=websites[state],label='Official county website',claim=f'Identifies Douglas County, {names[state]}, and lists county services.'))
 if state=='unassigned':p['sources']=sum(sources.values(),[])
 if cid==sid:master[cid]=p
 else:extra[cid]=p
splits.append(dict(source_id=sid,mode='filings',rationale='Same-name county governments separated by individually checked LDA client state. Every original filing is retained once; unchecked historical reports remain unassigned.',sources=sum(sources.values(),[]),children=children))
save(root/'research/verified-entity-splits.json',splits);save(root/'research/profiles.json',extra)
save('work/research-2026/reviewed.json',master);save('outputs/2026-research-trial/profiles.json',master)
(root/'research/reviewed-2026.json').write_text(json.dumps(master,separators=(',',':'))+'\n')
m=read(root/'research/publication-metadata.json');m['total']+=len(children)-1;m['counts']['sourced']+=3;m['updated']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(root/'research/publication-metadata.json',m)
save('work/research-2026/douglas-split/assignment-summary.json',{s:len(ids) for s,ids in groups.items()});print({s:len(ids) for s,ids in groups.items()})
