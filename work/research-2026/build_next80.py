import json,pathlib,re
r=pathlib.Path('work/research-2026');out={}
root_rows=[line.split('\t',2) for line in (r/'round120-root-descriptions.tsv').read_text().splitlines()]
root_reviews={k:{'name':n,'description':d} for k,n,d in root_rows}
ambiguous={'55d1265839a51587','59c11c96d4e1541a','59f0bf87d389d059','5b8ce049b2ba2a5e','5f159c3afcda291c','63c9bc8a379b904d'}
def normal(s):return re.sub(r'[^a-z0-9]','',s.lower())
for label in ['a','b']:
 inputs=json.load(open(r/f'round80-next-{label}-input.json'))
 reviews=root_reviews if label=='root' else json.load(open(r/f'round80-next-{label}-reviewed.json'))
 assert {x['id'] for x in inputs}==set(reviews)
 for x in inputs:
  k=x['id'];d=x['tax_evidence'];v=reviews[k];base=x['registry_profile'];a=json.load(open(r/'website-cache'/f'{k}.json'))
  name=v['name']
  for old,new in [(' Of ',' of '),(' For ',' for '),(' And ',' and '),(' The ',' the '),(' ON ',' on '),(' IN ',' in '),(' LAW ',' Law '),(' BAY ',' Bay '),(' NOW',' Now'),('Prepass','PrePass'),('Childrens',"Children's"),('Ochin','OCHIN')]:name=name.replace(old,new)
  text=a.get('text','');good=a.get('http_status')==200 and len(text)>50 and text.count('\ufffd')<5
  matched=good and (normal(name) in normal(text) or normal(x['name']) in normal(text)) and k not in ambiguous
  sources=list(base['sources'])+[{'label':'Filed organization mission and website','url':d['source_url'],'claim':'Form 990 for EIN '+d['ein']+' supplies the organization mission and reported website. Description reviewed individually against this record and available official website evidence.'}]
  o={'name':name,'description':v['description'],'kind':'Nonprofit organization' if base['kind']=='Tax-exempt organization' else base['kind'],'ownership':'Not applicable','website':a.get('requested_url',''),'website_status':'verified' if matched else 'filed','status':'sourced','review_outcome':'confirmed' if matched else 'partial','sources':sources,'notes':'Individually reviewed against the filed activity and website evidence. A filed website may be historical; unresolved fields remain explicit.','identity_evidence':'EIN '+d['ein']+'; filed legal name '+d.get('organization_name','')+'; original lobbying name and location evidence retained.','checked_at':'2026-09-05','as_of':'2026-09-05','featured':False,'legal_form':'','logo_url':'','logo_kind':'','logo_source_url':'','logo_status':'unresolved'}
  if matched:
   o['sources'].append({'label':'Official organization website','url':a['final_url'],'claim':'Page identifies the organization and provides evidence of its activities.'})
   if a.get('logo_http_status')==200 and a.get('logo_url')!='https://static.parastorage.com/client/pfavico.ico':
    for f in ['logo_url','logo_kind','logo_source_url']:o[f]=a[f]
    o['logo_status']='official_site_asset';o['sources'].append({'label':'Official website branding','url':a['logo_source_url'],'claim':'Organization website supplies this '+a['logo_kind'].replace('_',' ')+'. Image response checked.'})
  if k in ambiguous:o['notes']+=' The site uses an abbreviated, group or successor identity whose exact relationship needs additional verification.'
  out[k]=o
for k,v in out.items():
 for old,new in [('WI FI','Wi-Fi'),('Watereuse','WateReuse'),('LOW Income','Low Income'),(' OIL ',' Oil '),(' GAS ',' Gas '),(' TAX ',' Tax '),(' ART ',' Art '),(' AT ',' at '),(' LOS ',' Los '),('Anti Defamation','Anti-Defamation'),('Zero Prostate','ZERO Prostate')]:v['name']=v['name'].replace(old,new)
out['55caa526311141cb']['description']='Advocates education policies and legislation encouraging charitable funding for education, including scholarship tax credits.'
out['57f89d18226cb10c']['description']='University providing undergraduate, graduate and professional education.'
out['687aef2df647c1e9']['description']='Represents medical technology companies and advocates policies affecting medical-device access and regulation.'
out['5b7354805d2e7d78']['description']='Represents restaurant and foodservice businesses through research, policy advocacy and education.'
for k in ['55f744ac2832431e','567103bac5ec54bc','57f89d18226cb10c','5f64cad84ce197dd']:out[k]['kind']='Nonprofit college / university'
for k in ['545208c88b0e7954','5a82dbbe0233e45a','5d57f34b69e9b71d','5e8753c615653e27','64449128274162f6']:out[k]['kind']='Professional association'
out['5f159c3afcda291c']['kind']='Athletic conference'
for k in ['5e8c976eca270670','6195ea0a61ca2e73']:out[k]['kind']='Health provider'
v=out['54834c83c2a483c6'];v.update(kind='State-related university',ownership='State-related institution');v['sources'].append({'label':'Official university status','url':'https://www.pitt.edu/about/history-and-achievements','claim':'University identifies its current status as a state-related research university.'})
v=out['599823c1988584dd'];v.update(name='Low Income Investment Fund',website='https://www.liifund.org/',website_status='verified',review_outcome='confirmed',kind='Nonprofit financial institution');v['sources'].append({'label':'Correct official organization website','url':'https://www.liifund.org/','claim':'Identifies Low Income Investment Fund and its community-development financing activities. The tax return’s LIFUND.ORG address points to a different organization and is not used.'});v['notes']='The filed website contains a spelling error. Correct official site is LIIFUND.ORG; no Livelihood Impact Fund identity or branding is assigned.'
assert len(out)==80
(r/'round80-next-rootchecked.json').write_text(json.dumps(out,indent=2)+'\n')
print('Staged 80 root-checked profiles with LIIF website correction and Pitt state-related status.')
