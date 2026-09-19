import json,gzip,pathlib,datetime,random,sqlite3,unicodedata,collections
root=pathlib.Path('work/research-2026');data=json.load(gzip.open('lobbying-map/public/data/directory-v3.json.gz'));cs=[c for c in data['companies'] if c['years'].get('2026')]
# Reproducible mix of the actual 2026 population, not a familiar-brand-only sample.
rng=random.Random(20260905);chosen=[]
for status,n in [('sourced',10),('registry_matched',25),('self_reported',45),('pending',20)]:
 pool=[c for c in cs if c.get('profile',{}).get('status','pending')==status];chosen+=rng.sample(pool,min(n,len(pool)))
assert len(chosen)==100
norm=lambda s:' '.join(unicodedata.normalize('NFKC',s).upper().split())
names={norm(a) for c in chosen for a in c['aliases']};obs=collections.defaultdict(list)
c=sqlite3.connect('file:work/organization-research/bulk-profiles.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
for r in c.execute('select name,description,city,state,principal_city,principal_state,signed_date,source_url,source_member from descriptions'):
 if norm(r['name']) in names and len(obs[norm(r['name'])])<3:obs[norm(r['name'])].append(dict(r))
for c in chosen:c['filing_evidence']=[r for a in c['aliases'] for r in obs[norm(a)]]
root.joinpath('sample.json').write_text(json.dumps(chosen,indent=2))
for i,b in enumerate('abc'):root.joinpath('input-'+b+'.json').write_text(json.dumps(chosen[i::3],indent=2))
root.joinpath('queue.jsonl').write_text(''.join(json.dumps({'id':c['id'],'name':c['name'],'year':2026,'prior_status':c.get('profile',{}).get('status','pending'),'review_status':'queued','website_status':'unchecked','logo_status':'unchecked'})+'\n' for c in cs))
root.joinpath('run.json').write_text(json.dumps({'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':2026,'total':len(cs),'pilot_size':100,'sample_seed':20260905,'sample_strata':{'sourced':10,'registry_matched':25,'self_reported':45,'pending':20},'status':'running','cost_usd':None,'cost_note':'Subagent dollar billing not exposed; do not estimate as measured cost.'},indent=2))
print({b:len(chosen[i::3]) for i,b in enumerate('abc')})
