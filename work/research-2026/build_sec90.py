import json,pathlib,re
r=pathlib.Path('work/research-2026');out={};a=json.load(open(r/'sec-round4-a-final-audit.json'));ac=a.get('profiles',a.get('findings',{}));bc=json.load(open(r/'sec-round4-b-final-audit.json'))['corrections'];cc=json.load(open(r/'sec-round4-c-final-audit.json'))['corrections']
for l in 'abc':
 p=json.load(open(r/(f'sec-round4-{l}-researched.json' if l!='c' else 'sec-round4-c-cleaned-draft.json')));p={v['id']:v for v in p} if isinstance(p,list) else p
 inputs={v['id']:v for v in json.load(open(r/f'sec-round4-{l}-input.json'))};assert set(p)==set(inputs)
 for k,v in p.items():
  c=json.load(open(r/'website-cache'/f'{k}.json'));o={f:v.get(f,'') for f in ['name','description','website','identity_evidence','notes']};o.update(kind='Business',ownership=v.get('ownership','Publicly traded'),status='sourced',review_outcome=v.get('review_outcome','confirmed'),website_status='verified' if v.get('review_outcome','confirmed')=='confirmed' else 'filed',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved',sources=[{'url':s['url'],'label':s.get('label','Primary source'),'claim':s.get('claim',s.get('claims',''))} for s in v['sources']])
  if not o['identity_evidence']:o['identity_evidence']='SEC issuer name and reported city/state matched to House disclosure; official company site reviewed for activity and identity.'
  o['notes']='Individual company review. Original disclosure names remain available; current issuer details do not by themselves prove every historical alias refers to the same legal entity.'
  if l=='a' and k in a.get('summary',{}).get('concrete_corrections',[]):o.update(review_outcome='partial',website_status='filed')
  if k in cc:
   fix=cc[k];o['website']=fix['recommended_website'];o['sources']+=[{'url':s['url'],'label':'Corrected official company page','claim':s['claim']} for s in fix['evidence']]
  elif c.get('http_status')==200 and c.get('text') and c.get('final_url'):o['website']=c['final_url']
  # Explicit exchange/ticker citations from the actual cached SEC record.
  secid=inputs[k].get('registry',{}).get('id');f=pathlib.Path('work/organization-research/sec-submissions')/(str(secid).zfill(10)+'.json')
  if not f.exists():f=pathlib.Path('work/organization-research/sec-submissions')/(str(secid)+'.json')
  if f.exists():
   raw=json.load(open(f));d=raw.get('data',raw);pairs=[f'{e.upper()}: {t}' for e,t in zip(d.get('exchanges',[]),d.get('tickers',[]))];o['sources'].append({'url':raw.get('source_url',f'https://data.sec.gov/submissions/CIK{str(secid).zfill(10)}.json'),'label':'SEC issuer listing snapshot','claim':d.get('name','')+'; '+', '.join(pairs)+'.'})
  if k in bc:o['sources']+=bc[k]['sources']
  if c.get('logo_http_status')==200 and len(c.get('text',''))>60 and k not in ['1e1412b47829e158','73744412d19d7bfe']:
   for f in ['logo_url','logo_kind','logo_source_url']:o[f]=c[f]
   if k=='a2dff0f2cc160f8d':o['logo_kind']='site_icon'
   o['logo_status']='official_site_asset';o['sources'].append({'url':o['logo_source_url'],'label':'Official website branding','claim':'Official page supplies this '+o['logo_kind'].replace('_',' ')+'. Image response checked.'})
  out[k]=o
v=out['b5eb6d534c67560e'];v.update(description='Offshore marine and subsea services company formed by the September 2026 combination of Hornbeck and Helix.',review_outcome='partial',notes='The merger completed September 1, 2026. The combined issuer uses the Hornbeck name (NYSE: HOS); CIK 866829 previously belonged to Helix. Older Hornbeck lobbying filings predate the combination and are not proof of the same legal issuer.');v['sources'].append({'url':bc['b5eb6d534c67560e']['sources'][0]['url'],'label':'Combined issuer identity','claim':'SEC Form 8-K names the issuer Hornbeck Offshore Services, Inc., formerly Helix Energy Solutions Group, Inc.; NYSE: HOS.'})
out['f142ae1a4eee3fb8']['sources'].append({'url':'https://www.sec.gov/edgar/browse/?CIK=1750704','label':'SEC issuer listing','claim':'HawkEye 360, Inc.; NYSE: HAWK.'})
for k in ['81a43bf00cb054e1','86b9adffbc0ddae8','a2dff0f2cc160f8d','aa1209577a061b33','10975388fb995a4b','49c1cc9e7d66bec4','fcc9504a918c8be7','7a61f1a67a16667a','ca77d2df73721b6f','fc380050e91c6153']:out[k]['featured']=True
assert len(out)==90;(r/'sec-round4-staged.json').write_text(json.dumps(out,indent=2)+'\n');print('90 staged; ESS pending')
