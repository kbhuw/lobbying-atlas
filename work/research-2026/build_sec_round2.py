import json,pathlib
r=pathlib.Path('work/research-2026');out={}
for label in ['a','b','c']:
 base={x['id']:x for x in json.load(open(r/f'sec-round2-{label}-input.json'))}
 p=json.load(open(r/(f'sec-round2-{label}-'+('fixed.json' if label=='a' else 'researched.json'))))
 assert set(p)==set(base)
 for k,v in p.items():
  x=base[k];d=json.load(open('work/organization-research/sec-submissions/'+x['registry']['id']+'.json'))['data'];a=json.load(open(r/'website-cache'/f'{k}.json'))
  v.update(kind='Business',ownership=x['ownership'],status='sourced',review_outcome='confirmed',website_status='verified',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved')
  if label=='c':v['notes']='Current activities individually checked against the official company source. SEC issuer and House disclosure name/location evidence are retained; this does not verify every historical alias.'
  for s in v['sources']:
   s.setdefault('label','Official organization evidence')
   if 'data.sec.gov/submissions/' in s['url']:s['claim']='SEC issuer '+d['name']+'; '+', '.join(e.upper()+': '+t for e,t in zip(d['exchanges'],d['tickers']))+'. Listing information from the retrieved SEC company record.'
  if a.get('logo_http_status')==200 and len(a.get('text',''))>80 and k not in ['05e92dd310e0a548']:
   for f in ['logo_url','logo_kind','logo_source_url']:v[f]=a[f]
   if 'favicon' in v['logo_url'].lower():v['logo_kind']='site_icon'
   v['logo_status']='official_site_asset';v['sources'].append({'label':'Official website branding','url':v['logo_source_url'],'claim':'Official site supplies this '+v['logo_kind'].replace('_',' ')+'. Image response checked.'})
  out[k]=v
v=out['72ce79d44a4034ce'];c=json.load(open(r/'sec-round2-a-corrections.json'))['corrections']['72ce79d44a4034ce'];v['description']=c['recommended_description'];v['sources'] += [dict(label='Official company information',**s) for s in c['evidence']]
fix={
'401c190bcaa2135e':'Makes optical communication components and equipment for data centers, telecommunications and cable networks.',
'126c92f285f4aec9':'Develops medicines for kidney and digestive diseases, including high phosphate levels in chronic kidney disease and irritable bowel syndrome with constipation.',
'b42c117bc9f7e457':'Makes surgical devices for irregular heart rhythms, related heart conditions and pain management.',
'6b528b0a8489417d':'Develops oral antiviral medicines for serious viral infections.',
'a1465e0f2940d03c':'Develops self-driving truck technology and operates autonomous freight services.',
'1e60153b82d7d98e':'Makes automotive safety products, including airbags, seatbelts and steering wheels.',
'557e013df1d841fa':'Develops medicines for neurological diseases, immune-system conditions and cancer.',
'c1103d65dc3bb3f4':'Develops medicines for conditions including post-bariatric hypoglycemia, Wolfram syndrome and ALS.',
'06c6510f2a4aea3e':'Provides online and campus-based higher education, including programs for military communities, nursing and health sciences.',
'42f64c0d5817d272':'Develops medicines that silence disease-causing genes using RNA interference.',
'd2f27cfc1f8d6184':'Develops high-energy lithium-ion batteries for aviation, electric mobility and other applications.'}
for k,s in fix.items():out[k]['description']=s
for k,n in {'ae420c9e0901c5f1':'Applied Aerospace & Defense','e0eadba5b3e7cddf':'Bath & Body Works','61fbed264654c2d2':'Best Buy','9fb73d5962cb1e53':'BioMarin Pharmaceutical','7e4388f6885fa6c3':'AVITA Medical','e08c143b1469dd9c':'BETA Technologies'}.items():out[k]['name']=n
out['e0eadba5b3e7cddf'].update(website_status='unavailable',review_outcome='partial')
out['e0eadba5b3e7cddf']['notes']+=' Corporate website could not be fetched in the current check; the address and activities are retained from the sourced review.'
for k in ['61fbed264654c2d2','e0eadba5b3e7cddf','def0613fd0bbe1e9','5eb3b94c00d999cf','2a1b8226ab7b9de5']:out[k]['featured']=True
assert len(out)==45
(r/'sec-round2-rootchecked.json').write_text(json.dumps(out,indent=2)+'\n')
print('45 root-checked profiles staged')
