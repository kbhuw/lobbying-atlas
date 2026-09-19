import json,pathlib,re
r=pathlib.Path('work/research-2026');out={}
root_rows=[line.split('\t',2) for line in (r/'round120-root-descriptions.tsv').read_text().splitlines()]
root_reviews={k:{'name':n,'description':d} for k,n,d in root_rows}
ambiguous={'306171986618050a','311d6d2e3b0f2756','491d7b29bb0f1eab','5130d941c6707232','523365b049b00fd9','42223eb35434f641'}
def normal(s):return re.sub(r'[^a-z0-9]','',s.lower())
for label in ['a','b','root']:
 inputs=json.load(open(r/f'round120-{label}-input.json'))
 reviews=root_reviews if label=='root' else json.load(open(r/f'round120-{label}-reviewed.json'))
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
fix={
 '1e0cd03a6efe0228':'Advocates laws and policies opposing abortion and builds coalitions supporting that goal.',
 '2a226f8e6d556712':'Provides legal representation and related services in child-dependency court proceedings in California.',
 '2f24191ab8733556':'Organizes Jewish healthcare professionals to combat discrimination and antisemitism in medicine.',
 '31c7c782b20d968a':'Represents space-industry interests and advocates policies supporting U.S. space exploration, science and international cooperation.',
 '31da5b1097431efe':'Provides multidisciplinary cancer care to patients throughout Arkansas.',
 '32fb0e5d3d35b5a7':'Supports economic opportunities for its member communities through sustainable use of Bering Sea resources.',
 '42ee16d0531e50bc':'Opposes abortion and provides support related to unexpected pregnancy and early-childhood care.',
 '46903ae17db29ffa':'Represents meat and poultry businesses through industry advocacy and member services.'}
for k,description in fix.items():out[k]['description']=description
for k in ['2a7e4d2a1c3876cd','355e9c62b0a2f49f','37d359005b3a26c1','3cfe3e5ad579d388','491d7b29bb0f1eab','4b2ba8955385262d','52464543439b9654','5266d114f123c33e']:out[k]['kind']='Nonprofit college / university'
for k in ['311d6d2e3b0f2756','31da5b1097431efe','39ab8f7b2672a24a','3bed0a65ecaabde3','3e77402e290f2fbb','42223eb35434f641','422c88def6b38803','4284b4fdca6b90ac','49691a8efabb6e7c','4aab60e062f2670b']:out[k]['kind']='Hospital / health provider'
for k in ['3469a702443aebf6','346b138a0f417520','3ad9cd6923052aee','43cb9a88951fcf3a','4e760bcde235f5c8','5130d941c6707232']:out[k]['kind']='Professional association'
out['47c18225f0239b38']['kind']='Athletic conference'
for k in ['494b8bcb79740488','538e752663ebed41','3c2019149e5ce906']:out[k]['featured']=True
out['5133f9387dc9273e']['sources'].append({'label':'Official grantmaking process','url':'https://www.calfund.org/our-process/','claim':'Describes community philanthropy and grantmaking across Los Angeles County.'})
z=out['51514eaae0e51611'];z.update(kind='Industry association',website='https://www.zeta.org/',website_status='verified',review_outcome='confirmed',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved',identity_evidence='Original lobbying name and Washington, DC location match the association’s official about page. Earlier tax-return evidence pointed to its education affiliate and is excluded.',notes='ZETA and the ZETA Education Fund are affiliated but separate organizations. No education-fund tax ID or financial data is assigned to this association.')
z['sources']=[s for s in z['sources'] if s['label'].startswith('House')]+[{'label':'Official association activities','url':'https://www.zeta.org/about','claim':'Identifies the Zero Emission Transportation Association, its Washington, DC address and federal EV policy work.'},{'label':'Separate education affiliate','url':'https://www.zeta.org/education-fund','claim':'The education fund identifies itself as a nonprofit affiliate of the association.'}]
assert len(out)==120
(r/'round120-rootchecked.json').write_text(json.dumps(out,indent=2)+'\n')
print('Built 120 individually reviewed, exact-ID profiles with explicit website uncertainty.')
