import json,pathlib
r=pathlib.Path('work/research-2026');g=r/'college-scorecard';inputs={v['id']:v for v in json.load(open(g/'remaining57-input.json'))};p={};out={};holds=json.load(open(g/'remaining-branding-holds.json'));source=json.load(open(g/'source.json'))['source_url'];control={'1':'Public institution','2':'Private nonprofit','3':'Private for-profit'}
for l in 'abc':
 a=json.load(open(g/f'remaining-{l}-researched.json'));a={v['id']:v for v in a} if isinstance(a,list) else a;p.update(a)
assert set(p)==set(inputs)
for k,v in p.items():
 o={f:v.get(f,'') for f in ['name','description','website','identity_evidence','notes']};o.update(kind='College / university',ownership=v.get('ownership','Unknown'),status='unresolved' if v['review_outcome']=='unresolved' else 'sourced',review_outcome=v['review_outcome'],website_status='verified' if v['review_outcome']=='confirmed' else 'filed' if v.get('website') else 'unresolved',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved',sources=[{'url':s['url'],'label':s.get('label','Official source'),'claim':s.get('claim',s.get('claims',''))} for s in v['sources']])
 candidates=inputs[k]['candidates'];c=None
 if len(candidates)==1:c=candidates[0]
 elif k=='95fa978d841b4ff8':c=next(c for c in candidates if c['STABBR']=='MN')
 if c:
  o.update(ownership=control[c['CONTROL']],institution_control_as_of='2025-05-19');o['sources'].append({'url':source,'label':'Education Department institution record — May 2025','claim':f"UNITID {c['UNITID']}: {c['INSTNM']}, {c['CITY']}, {c['STABBR']}; institutional control {control[c['CONTROL']]}; reported website {c['INSTURL']}."});o['notes']+=' Institutional control from May 2025 Education Department snapshot unless a newer source is cited.'
 if o['description'].startswith(o['name']+' is '):o['description']=o['description'][len(o['name'])+4:];o['description']=o['description'][0].upper()+o['description'][1:]
 f=r/'website-cache'/f'{k}.json';cache=json.load(open(f)) if f.exists() else {}
 if o['website'] and k not in holds and cache.get('logo_http_status')==200 and len(cache.get('text',''))>60:
  for field in ['logo_url','logo_kind','logo_source_url']:o[field]=cache[field]
  o['logo_status']='official_site_asset';o['sources'].append({'url':o['logo_source_url'],'label':'Official website branding','claim':'Official page supplies the linked '+o['logo_kind'].replace('_',' ')+'. Image response checked.'})
 out[k]=o
c=json.load(open(g/'nuc-rename-correction.json'));v=out[c['id']];v.update(name=c['current_name'],website=c['website'],description=c['description'],ownership=c['ownership'],institution_control_as_of='2026-02-02',identity_evidence=c['identity_evidence'],notes=c['notes'],review_outcome='confirmed',website_status='verified');v['sources'] += [{'url':s['url'],'label':s['label'],'claim':s['claims']} for s in c['sources']]
out['89d428754639e27a']['name']='Hillsborough College'
for k in ['cc426349efa78821','e3506989b248d04e','d94dedb961f24a66','4b6a5150a1d387aa','b405bfa47325d5ec','ba4b21cb3951fad6','a7af122388e9b9cb']:out[k]['featured']=True
(g/'57-rootchecked.json').write_text(json.dumps(out,indent=2)+'\n');print('57 normalized with source dates, exact Bethel, unresolved Anderson, Northbridge rename')
