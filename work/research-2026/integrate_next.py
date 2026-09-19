import json,pathlib,datetime,csv,collections
r=pathlib.Path('work/research-2026');site=pathlib.Path('lobbying-map');p=json.load(open(r/'reviewed.json'));batch={}
for n in range(2):batch.update(json.load(open(r/f'tax-next-reviewed-{n}.json')))
held=['0a950197f4f06659','0c68f3a8dfe9756b']
for k in held:batch.pop(k)
prior=set(p)
for k,v in batch.items():
 a=json.load(open(r/'website-cache'/f'{k}.json'));v['logo_status']='unresolved'
 if a.get('requested_url')==v.get('website') and a.get('logo_http_status')==200 and v.get('website_status')=='verified':
  for field in ['logo_url','logo_kind','logo_source_url']:v[field]=a[field]
  v['logo_status']='official_site_asset';v['sources'].append({'label':'Official website branding','url':a['logo_source_url'],'claim':'Official site supplies the displayed '+a['logo_kind'].replace('_',' ')+'. Image returned successfully when checked.'})
 v['review_outcome']='confirmed' if v.get('website_status')=='verified' else 'partial'
 p[k]=v
assert len(p)==178 and prior<=p.keys()
for f in [r/'reviewed.json',site/'research/reviewed-2026.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,indent=2)+'\n')
m=json.load(open(site/'research/reviewed-2026-manifest.json'));m['reviewed_ids']=sorted(p)
if not any(b['name']=='tax-next-58' for b in m['batches']):m['batches'].append({'name':'tax-next-58','ids':sorted(batch)})
(site/'research/reviewed-2026-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
f=site/'scripts/test-reviewed-2026.mjs';f.write_text(f.read_text().replace('length,120','length,178').replace('120 exact IDs','178 exact IDs'))
q=[json.loads(l) for l in (r/'queue.jsonl').read_text().splitlines()]
for x in q:
 k=x['id']
 if k in p:
  v=p[k];x.update(review_status=v['review_outcome'],website_status=v.get('website_status','unresolved'),logo_status=v.get('logo_status','unresolved'),missing_fields=[field for field in ['website','logo_url','ownership'] if not v.get(field) or v.get(field)=='Unknown'],reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 elif k in held:x.update(review_status='identity_review_needed',review_note='Exact legal-entity/domain relationship requires further checking.')
(r/'queue.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in q))
out=pathlib.Path('outputs/2026-research-trial');fields=['id','name','description','kind','ownership','website','logo_url','logo_kind','review_outcome','checked_at','sources']
with (out/'profiles.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for k,v in p.items():w.writerow({**{field:v.get(field,'') for field in fields},'id':k,'sources':' | '.join(s['url'] for s in v['sources'])})
summary={'scope':2026,'total':len(q),'reviewed':len(p),'remaining':len(q)-len(p),'websites':sum(bool(v.get('website')) for v in p.values()),'branding':dict(collections.Counter(v.get('logo_kind') or 'missing' for v in p.values())),'publication_status':'120 live; 58 additional profiles checked locally','full_scope_complete':False};(out/'current-progress.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
