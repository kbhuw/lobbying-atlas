import json,pathlib,urllib.parse
r=pathlib.Path('work/research-2026');g=r/'dotgov';p=json.load(open(g/'all403-drafts.json'));inputs={x['id']:x for x in json.load(open(g/'2026-candidates.json'))};existing=json.load(open(r/'reviewed.json'));ex=json.load(open(g/'branding-exclusions.json'));source=json.load(open(g/'source.json'))['url'];out={}
for fn in ['wrong-domain-repairs.json','three-program-domain-repairs.json','two-program-domain-repairs.json','last-two-repairs.json']:
 f=g/fn
 if f.exists():
  a=json.load(open(f));a={v['id']:v for v in a} if isinstance(a,list) else a;p.update(a)
kindmap={'city':'Municipal government','municipal':'Municipal government','county':'County government','county - election':'County government','state or territory':'State government','state':'State government','tribal':'Tribal government','publicagency':'Public agency','special district':'Special district','special district government':'Special district','interstate':'Interstate agency','interstate public agency':'Interstate agency'}
for k,v in p.items():
 if k in existing:continue
 x=inputs[k];matches=x['location_matches'];m=matches[0];d=m['domain_record'];disc=m['disclosure'];states=sorted({t['domain_record']['State'].upper() for t in matches});mixed=len(states)>1;cache=json.load(open(r/'website-cache'/f'{k}.json'))
 sources=[{'url':s['url'],'label':s.get('label','Official source'),'claim':s.get('claim',s.get('claims',''))} for s in v['sources'] if 'disclosurespreview.house.gov' not in s['url']]
 sources.append({'url':source,'label':'CISA registered .gov domain record','claim':f"Domain {d['Domain name']} registered to {d['Organization name']}, {d['City']}, {d['State']}. A registered domain may serve a department or program rather than the whole organization."})
 for match in matches:
  ds=match['disclosure'];entry={'url':ds['source_url'],'label':'House lobbying disclosure — '+ds['source_member'],'claim':f"Client {ds['name']}, reported location {ds['city']}, {ds['state']}; source member {ds['source_member']}."}
  if entry not in sources:sources.append(entry)
 kind=kindmap.get(v.get('kind','').lower(),v.get('kind','Public agency'))
 o={f:v.get(f,'') for f in ['name','description','website']};o.update(kind=kind,ownership='Government body' if 'university' not in kind.lower() else 'Public institution',sources=sources,identity_evidence=v.get('identity_notes',''),status='sourced',review_outcome=v.get('review_outcome','partial'),website_status='verified' if v.get('review_outcome')=='confirmed' else 'filed',checked_at='2026-09-05',as_of='2026-09-05',notes='Government organization; public does not mean publicly traded.',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved')
 if 'exact matched city and state' in o['description']:o['description']=f"{kind} for {d['Organization name']} in {d['State']}."
 if mixed:
  o.update(status='unresolved',review_outcome='unresolved',website_status='unresolved',website='',ownership='Unknown',description=f"This name group contains disclosure evidence for separate governments in {' and '.join(states)}. A single organization has not been established.",identity_evidence='House and CISA records match multiple states: '+', '.join(states)+'. The name group requires separation before assigning one website or logo.',notes='Ambiguous same-name organizations. Filing totals in this group must not be attributed to a single government.')
 elif cache.get('logo_http_status')==200 and len(cache.get('text',''))>60 and k not in ex and cache.get('requested_url','').rstrip('/')==o['website'].rstrip('/') and '/core/misc/favicon.ico' not in cache.get('logo_url',''):
  for f in ['logo_url','logo_kind','logo_source_url']:o[f]=cache[f]
  o['logo_status']='official_site_asset';o['sources'].append({'url':o['logo_source_url'],'label':'Official website branding','claim':'Official page supplies the linked '+o['logo_kind'].replace('_',' ')+'. Image response checked.'})
 out[k]=o
assert len(out)==402
(g/'402-staged.json').write_text(json.dumps(out,indent=2)+'\n');print('402 prepared, not integrated; root final identity and asset audit still required')
