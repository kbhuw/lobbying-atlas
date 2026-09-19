import json,pathlib,datetime,csv,collections,re,urllib.parse
r=pathlib.Path('work/research-2026');site=pathlib.Path('lobbying-map');p=json.load(open(r/'reviewed.json'));batch=json.load(open(r/'sec-round2-rootchecked.json'));holds=json.load(open(site/'research/registry-match-holds.json'));assert len(batch)==45
p.update(batch)
assert len(p)==834
for f in [r/'reviewed.json',site/'research/reviewed-2026.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,indent=2)+'\n')
m=json.load(open(site/'research/reviewed-2026-manifest.json'));m['reviewed_ids']=sorted(p)
if not any(b['name']=='sec-round2-45' for b in m['batches']):m['batches'].append({'name':'sec-round2-45','ids':sorted(batch)})
(site/'research/reviewed-2026-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
f=site/'scripts/test-reviewed-2026.mjs';f.write_text(f.read_text().replace('length,789','length,834').replace('789 exact IDs','834 exact IDs'))
q=[json.loads(l) for l in (r/'queue.jsonl').read_text().splitlines()]
for x in q:
 k=x['id']
 if k in p:
  v=p[k];x.update(review_status=v['review_outcome'],website_status=v.get('website_status','unresolved'),logo_status=v.get('logo_status','unresolved'),missing_fields=[field for field in ['website','logo_url','ownership'] if not v.get(field) or v.get(field)=='Unknown'],reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 elif k in holds:x.update(review_status='identity_review_needed',review_note=holds[k]['reason'])
(r/'queue.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in q))
out=pathlib.Path('outputs/2026-research-trial');fields=['id','name','description','kind','ownership','website','logo_url','logo_kind','review_outcome','checked_at','sources']
with (out/'profiles.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for k,v in p.items():w.writerow({**{field:v.get(field,'') for field in fields},'id':k,'sources':' | '.join(s['url'] for s in v['sources'])})
summary={'scope':2026,'total':len(q),'reviewed':len(p),'remaining':len(q)-len(p),'websites':sum(bool(v.get('website')) for v in p.values()),'branding':dict(collections.Counter(v.get('logo_kind') or 'missing' for v in p.values())),'publication_status':'742 profiles live; 27 existing reviews reconciled and 20 new profiles checked locally','full_scope_complete':False};(out/'current-progress.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
