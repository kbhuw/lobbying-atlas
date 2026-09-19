import json,pathlib,sys,re,datetime
r=pathlib.Path('work/research-2026');site=pathlib.Path('lobbying-map');batch_path=pathlib.Path(sys.argv[1]);name=sys.argv[2];batch=json.load(open(batch_path));p=json.load(open(r/'reviewed.json'));old=len(p)
assert isinstance(batch,dict) and batch
assert not(set(batch)&set(p)), 'Batch must contain only new IDs; apply corrections explicitly'
for k,v in batch.items():assert v.get('identity_evidence') and len(v.get('description',''))>20 and v.get('sources')
p.update(batch)
for f in [r/'reviewed.json',site/'research/reviewed-2026.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text((json.dumps(p,separators=(',',':')) if f==site/'research/reviewed-2026.json' else json.dumps(p,indent=2))+'\n')
m=json.load(open(site/'research/reviewed-2026-manifest.json'));assert not any(b['name']==name for b in m['batches']);m['batches'].append({'name':name,'ids':sorted(batch)});m['reviewed_ids']=sorted(p);(site/'research/reviewed-2026-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
f=site/'scripts/test-reviewed-2026.mjs';s=f.read_text().replace(f'length,{old}',f'length,{len(p)}').replace(f'{old} exact IDs',f'{len(p)} exact IDs');f.write_text(s)
q=[json.loads(l) for l in (r/'queue.jsonl').read_text().splitlines()]
for x in q:
 if x['id'] in batch:
  v=batch[x['id']];x.update(review_status=v['review_outcome'],website_status=v.get('website_status','unresolved'),logo_status=v.get('logo_status','unresolved'),missing_fields=[f for f in ['website','logo_url','ownership'] if not v.get(f) or v.get(f)=='Unknown'],reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
(r/'queue.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in q));print(old,'->',len(p),'reviewed')
