import json,pathlib,re
r=pathlib.Path('work/research-2026');g=r/'dotgov';p=json.load(open(g/'unmatched132-correcting.json'));inputs={x['id']:x for l in 'abc' for x in json.load(open(g/f'unmatched-{l}-input.json'))};locs={x['id']:x for l in 'abc' for x in json.load(open(g/f'unmatched-{l}-location-audit-input.json'))};source=json.load(open(g/'source.json'))['url']
for k,v in json.load(open(g/'unmatched-a-site-repairs.json')).items():
 # Keep original House evidence and append repaired official source.
 v['sources']=p[k].get('sources',[])+v.get('sources',[]);p[k].update(v)
for l in 'bc':
 for x in json.load(open(g/f'unmatched-{l}-site-repairs.json'))['repairs']:
  v=p[x['id']];v['website']=x.get('current_primary_website',x.get('official_website'));v.setdefault('sources',[]).extend(x.get('sources',[{'url':x.get('source_url'),'label':'Official primary government site','claim':x.get('reason','')}]))
(g/'unmatched132-websites-final.json').write_text(json.dumps(p,indent=2))
out={}
for k,v in p.items():
 x=inputs[k];sources=[]
 for s in v.get('sources',[]):
  if not s.get('url') or 'CISA' in s.get('label','') or 'disclosurespreview.house.gov' in s['url']:continue
  sources.append({'url':s['url'],'label':s.get('label','Official source'),'claim':s.get('claim',s.get('claims',''))})
 for c in x['candidates']:sources.append({'url':source,'label':'CISA .gov candidate record','claim':f"Candidate domain {c['Domain name']} registered to {c['Organization name']}, {c['City']}, {c['State']}. Candidate records alone do not prove the filing identity or a live primary website."})
 ds=locs[k]['disclosures'] or x['disclosures'][:2]
 for d in ds:
  sources.append({'url':d['source_url'],'label':'House disclosure — '+d['source_member'],'claim':f"Client {d['name']}; reported location {d.get('city') or 'not supplied'}, {d.get('state') or 'not supplied'}; member {d['source_member']}; signed {d.get('signed_date')}."})
 name=v['name'];name=re.sub(r'\b(Of|IN|ST|ANA|SAN|BAY|MID|SAC|FOX)\b',lambda m:{'Of':'of','IN':'in','ST':'St.','ANA':'Ana','SAN':'San','BAY':'Bay','MID':'Mid','SAC':'Sac','FOX':'Fox'}[m[0]],name);name=name.replace('CIty','City').replace('Hood River-white','Hood River-White')
 desc=v.get('description','');unresolved=v.get('review_outcome')=='unresolved'
 if unresolved:desc='The disclosed name has not been linked to a single government with sufficient evidence. Locations and candidate records are listed in the sources.'
 elif desc.lower().startswith(name.lower()+' is '):desc=desc[len(name)+4:];desc=desc[0].upper()+desc[1:]
 kind=v.get('kind','Public agency');kind={'City':'Municipal government','County':'County government','Tribal':'Tribal government'}.get(kind,kind) or 'Government entity'
 o=dict(name=name,description=desc,kind=kind,ownership='Unknown' if unresolved else 'Government body',website='' if unresolved else v.get('website',''),sources=sources,identity_evidence=v.get('identity_evidence',''),status='unresolved' if unresolved else 'sourced',review_outcome=v.get('review_outcome','partial'),website_status='unresolved' if unresolved else 'filed',checked_at='2026-09-05',as_of='2026-09-05',notes='Government organization; public does not mean publicly traded. '+('A single entity is not established; do not attribute all grouped filing totals to one government.' if unresolved else 'Historical filings and uncertain identity links remain visible in the sources.'),featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved')
 cfile=r/'website-cache'/f'{k}.json';c=json.load(open(cfile)) if cfile.exists() else {}
 if not unresolved and c.get('requested_url','').rstrip('/')==o['website'].rstrip('/') and c.get('http_status')==200 and len(c.get('text',''))>100 and 'Parked Domain' not in c['text']:
  o['website_status']='verified';o['website']=c.get('final_url',o['website'])
  if c.get('logo_http_status')==200 and k not in ['1962d040727cee72','503039a011cac7b2']:
   for f in ['logo_url','logo_kind','logo_source_url']:o[f]=c.get(f,'')
   o['logo_status']='official_site_asset';o['sources'].append({'url':o['logo_source_url'],'label':'Official website branding','claim':'Official page supplies the linked '+o['logo_kind'].replace('_',' ')+'. Image response checked.'})
 elif not unresolved:o['review_outcome']='partial'
 assert o['identity_evidence'];out[k]=o
assert len(out)==132;(g/'unmatched132-rootchecked.json').write_text(json.dumps(out,indent=2)+'\n');print('132 built; refresh after corrected website fetch')
