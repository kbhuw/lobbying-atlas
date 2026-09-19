import json,pathlib,datetime,csv,collections,re,urllib.parse
r=pathlib.Path('work/research-2026');site=pathlib.Path('lobbying-map');p=json.load(open(r/'reviewed.json'));raw=json.load(open(r/'tax-large-reviewed-1.json'));holds=json.load(open(site/'research/registry-match-holds.json'));batch={k:v for k,v in raw.items() if k not in holds and k!='40ebdbda41565c95'}
assert len(batch)==97
for k,v in batch.items():
 # Root reviewed all descriptions for name/activity correspondence; keep identity limitations explicit.
 for a,b in [(' CAR ',' Car '),(' ART',' Art'),(' BAR ',' Bar '),(' ON ',' on '),(' LAW ',' Law '),(' PET ',' Pet '),('PET ','Pet '),('HOT TUB','Hot Tub'),(' TAX ',' Tax '),(' TO ',' to '),('NEW Jersey','New Jersey'),(' ANN ',' Ann '),('Icivics','iCivics'),('Wateraid','WaterAid'),('Camba','CAMBA'),('Womens','Women’s')]:v['name']=v['name'].replace(a,b)
 if 'Represents' in v['description'] or 'Trade association' in v['description']:v['kind']='Trade / business association'
 if k in ['49a4f7e20bff27ef','4e468de3d5724730']:v['kind']='Labor union'
 if v['kind'] in ['Nonprofit organization','University','Museum','Healthcare provider']:v['kind']='Nonprofit / initiative'
 a=json.load(open(r/'website-cache'/f'{k}.json'));v['logo_status']='unresolved'
 if v.get('website_status')=='verified' and a.get('http_status')==200 and a.get('requested_url','').lower().rstrip('/')==v.get('website','').lower().rstrip('/'):
  v['website']=a['requested_url']
  if a.get('logo_http_status')==200:
   for field in ['logo_url','logo_kind','logo_source_url']:v[field]=a[field]
   v['logo_status']='official_site_asset';v['sources'].append({'label':'Official website branding','url':a['logo_source_url'],'claim':'Website supplies the displayed '+a['logo_kind'].replace('_',' ')+'. Asset fetched successfully.'})
 else:
  v['website_status']='filed';v['review_outcome']='partial'
 u=urllib.parse.urlsplit(v['website']);v['website']=urllib.parse.urlunsplit((u.scheme.lower(),u.netloc.lower(),u.path,u.query,u.fragment))
 p[k]=v
assert len(p)==275
for f in [r/'reviewed.json',site/'research/reviewed-2026.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,indent=2)+'\n')
m=json.load(open(site/'research/reviewed-2026-manifest.json'));m['reviewed_ids']=sorted(p)
if not any(b['name']=='tax-large-b-97' for b in m['batches']):m['batches'].append({'name':'tax-large-b-97','ids':sorted(batch)})
(site/'research/reviewed-2026-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
f=site/'scripts/test-reviewed-2026.mjs';f.write_text(f.read_text().replace('length,178','length,275').replace('178 exact IDs','275 exact IDs'))
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
summary={'scope':2026,'total':len(q),'reviewed':len(p),'remaining':len(q)-len(p),'websites':sum(bool(v.get('website')) for v in p.values()),'branding':dict(collections.Counter(v.get('logo_kind') or 'missing' for v in p.values())),'publication_status':'178-profile deployment in progress; 97 additional profiles checked locally','full_scope_complete':False};(out/'current-progress.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
