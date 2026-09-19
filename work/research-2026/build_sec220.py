import json,pathlib,re,urllib.parse
r=pathlib.Path('work/research-2026');out={}
for rnd in [5,6]:
 for l in 'abc':
  p=json.load(open(r/f'sec-round{rnd}-{l}-researched.json'));p={v['id']:v for v in p} if isinstance(p,list) else p
  inputs={v['id']:v for v in json.load(open(r/f'sec-round{rnd}-{l}-input.json'))};assert set(p)==set(inputs)
  for k,v in p.items():
   c=json.load(open(r/'website-cache'/f'{k}.json'));o={f:v.get(f,'') for f in ['name','description','website','identity_evidence','notes']}
   o.update(kind='Business',ownership=v.get('ownership','Publicly traded'),status='sourced',review_outcome=v.get('review_outcome','partial'),website_status='filed',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved',sources=[{'url':s['url'],'label':s.get('label','Primary source'),'claim':s.get('claim',s.get('claims',''))} for s in v['sources']])
   assert o['identity_evidence']
   o['notes']='Individual company review. Original disclosure names remain available; current issuer details do not by themselves prove every historical alias refers to the same legal entity.'
   if c.get('http_status')==200 and len(c.get('text',''))>100:
    o['website']=c['final_url'];o['website_status']='verified'
   else:o['review_outcome']='partial'
   o['website']=re.sub(r'([?&])cacheBuster=[^&]*&?',r'\1',o['website']).rstrip('?&')
   secid=inputs[k].get('registry',{}).get('id');f=pathlib.Path('work/organization-research/sec-submissions')/(str(secid).zfill(10)+'.json')
   if not f.exists():f=pathlib.Path('work/organization-research/sec-submissions')/(str(secid)+'.json')
   if f.exists():
    raw=json.load(open(f));d=raw.get('data',raw);pairs=[f'{e.upper()}: {t}' for e,t in zip(d.get('exchanges',[]),d.get('tickers',[]))];o['sources'].append({'url':raw.get('source_url',f'https://data.sec.gov/submissions/CIK{str(secid).zfill(10)}.json'),'label':'SEC issuer listing snapshot','claim':d.get('name','')+'; '+', '.join(pairs)+'.'})
   if c.get('logo_http_status')==200 and len(c.get('text',''))>100:
    for f in ['logo_url','logo_kind','logo_source_url']:o[f]=c.get(f,'')
    o['logo_status']='official_site_asset';o['sources'].append({'url':o['logo_source_url'],'label':'Official website branding','claim':'Official page supplies this '+o['logo_kind'].replace('_',' ')+'. Image response checked.'})
   # Make descriptions readable without repeating the title.
   o['description']=re.sub('^'+re.escape(v['name'])+r' is an? ','',o['description'],flags=re.I)
   if o['description']:o['description']=o['description'][0].upper()+o['description'][1:]
   out[k]=o
names={'dd7c584bdaad9898':'NeoVolta','974dd2f18cf648b3':'NETGEAR','45e8cb52778ac514':'Old Dominion Freight Line','15c3676840dbeb99':'One Stop Systems','6243841f8cc99699':'OPKO Health','f628b605eb217317':'PepsiCo','8848fcb780eb9b86':'Plains All American Pipeline','0192a489b2362ceb':'PriceSmart','a9e41702ca42ac5d':'Red Cat Holdings','e92dcc6d2df7b488':'Red Rock Resorts','b05b2692dae3143b':'REGENXBIO','f7861e6196041d80':'Silver Bow Mining','8165d1b89d9b863f':'Smith & Wesson Brands','80667bed47e5cd47':'SoFi Technologies','4728456f8477f5a4':'Sturm, Ruger & Co.','0a6976bc5b7986ff':'TriNet Group','8de7c7a4375e1499':'TransMedics Group','c08e585dab8ea281':'Via Transportation','bb16d17def93bb0a':'W&T Offshore','0d45eb04379502b8':'SentinelOne','7cd71b5815aa1450':'Stanley Black & Decker','554f4b4e05423d7b':'VivoSim Labs'}
for k,n in names.items():out[k]['name']=n
out['13e97c7e3f4683ea']['description']='Biopharmaceutical holding company focused on developing Trappsol Cyclo for Niemann-Pick disease type C1 through its Cyclo Therapeutics subsidiary, alongside other investments.'
out['13e97c7e3f4683ea']['sources'].append({'url':'https://www.sec.gov/Archives/edgar/data/1713863/000121390026067560/R7.htm','label':'SEC quarterly report, April 2026','claim':'Primary focus is completion of the pivotal Phase 3 Trappsol Cyclo trial and regulatory approval; one remaining real estate asset.'})
for rnd,l in [(5,'b'),(5,'c'),(6,'b'),(6,'c')]:
 a=json.load(open(r/f'sec-round{rnd}-{l}-final-audit.json'))
 for fix in a.get('corrections',[]):
  k=fix['id']
  if fix.get('name')=='Owens Corning':k='88ace3cf90ebced0' # Audit mistakenly supplied HP id.
  assert k in out
  if 'proposed' in fix:out[k][fix['field']]=fix['proposed']
  for f in ['website','description']:
   if f in fix:out[k][f]=fix[f]
  out[k]['sources'].append({'url':fix['source_url'],'label':'Current company evidence','claim':fix.get('evidence',fix.get('reason',fix.get('correction','')))})
out['df7cdaadb87b1d1c']['ownership']='Publicly traded'
out['df7cdaadb87b1d1c']['notes']+=' Smithfield returned to Nasdaq in January 2025; public trading and WH Group control coexist.'
out['df7cdaadb87b1d1c']['sources'].append({'url':'https://www.smithfieldfoods.com/press-room/smithfield-foods-to-announce-second-quarter-fiscal-2026-results-on-august-11-2026','label':'Smithfield 2026 announcement','claim':'Smithfield Foods, Inc. is listed as Nasdaq: SFD.'})
for k in ['59991c72c6730aed','d5b5e2401b509d86','41b0af713703ec7a','54c68d88f519b8aa','1c59c02a80322d98','51b9fc24f523b193','15356b5451ae16ea','3361333683d0837b','9e493be4f6efb5ff','f628b605eb217317','019f657fbd5e8525','8ca31f24ef318955','cee99645d3d81547','3f37b6a836ba5013','89cb4b15ec527317','647b9a17e91f0696','8f9c76dadf9feed8','d830a8cc1b1ff117','83bc1e5841cdd37e','95310c0f8bedc858','0a1f8d575dac93fb','6ee6f299b664727b','278353e770b87e69','0f1a5239e1cc5432','71473afde707a002']:out[k]['featured']=True
assert len(out)==220
(r/'sec-round5-6-staged.json').write_text(json.dumps(out,indent=2)+'\n');print('220 staged; pending final asset and divestiture repairs')
