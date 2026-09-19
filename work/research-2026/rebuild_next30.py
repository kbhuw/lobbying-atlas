import json,pathlib,datetime,re,urllib.parse
r=pathlib.Path('work/research-2026');rows=[line.split('\t',2) for line in (r/'next30-descriptions.tsv').read_text().splitlines()];descriptions={k:d for k,n,d in rows};names={k:n for k,n,d in rows};out={};holds=json.load(open('lobbying-map/research/registry-match-holds.json'))
# Root checked the cached page identities; redirects to renamed/ambiguous organizations remain filed.
ambiguous={'03a6f1308e9e7ddd','143cee270a6ac794','1635c1fcc450c5ea','1861f44a172798b8','1a4b7779efb67fd9','1ce21285b0fc3278','1b09ea292aecc722'}
for x in json.load(open(r/'next30-input.json')):
 k=x['id']
 if k in holds or k not in descriptions:continue
 d=x['tax_evidence'];cache=r/'website-cache'/f'{k}.json';a=json.load(open(cache)) if cache.exists() else {};base=x['registry_profile'];v={'name':names[k],'description':descriptions[k],'kind':base.get('kind','Nonprofit / initiative'),'ownership':'Not applicable','website':a.get('requested_url',''),'sources':list(base['sources']),'status':'sourced','featured':False,'legal_form':'','checked_at':'2026-09-05','as_of':'2026-09-05','notes':'Description reviewed against this organization’s filed mission. Website identity was checked separately; filed links may be historical.','identity_evidence':'EIN '+d['ein']+'; filed legal name '+d.get('organization_name','')+'; matched to the lobbying disclosure using the original registry evidence.','logo_url':'','logo_kind':'','logo_source_url':'','logo_status':'unresolved'}
 for old,new in [(' RED ',' Red '),(' TO ',' to '),(' ON ',' on '),(' LAW ',' Law '),(' GAS ',' Gas '),('For ALL','for All'),('Issue ONE','Issue One'),('Medstar','MedStar'),('Naadac','NAADAC'),('Jobsohio','JobsOhio'),('GBS Cidp','GBS-CIDP'),('Dance/usa','Dance/USA'),('Ctia ','CTIA '),('Womens','Women’s'),('Usagainstalzheimers','UsAgainstAlzheimer’s')]:v['name']=v['name'].replace(old,new)
 v['sources'].append({'label':'Filed mission and website — EIN '+d['ein'],'url':d['source_url'],'claim':'Form 990 reports the mission and website for '+d.get('organization_name','')+'. The description is a plain-English paraphrase of this record.'})
 verified=a.get('http_status')==200 and len(a.get('text',''))>50 and k not in ambiguous
 v['website_status']='verified' if verified else 'filed';v['review_outcome']='confirmed' if verified else 'partial'
 if verified:
  v['sources'].append({'label':'Official organization website','url':a['final_url'],'claim':'Page identity and activity reviewed against the organization name and filed mission.'})
  if a.get('logo_http_status')==200 and a.get('logo_url')!='https://static.parastorage.com/client/pfavico.ico':
   for field in ['logo_url','logo_kind','logo_source_url']:v[field]=a[field]
   v['logo_status']='official_site_asset';v['sources'].append({'label':'Official website branding','url':a['logo_source_url'],'claim':'Page supplies this '+a['logo_kind'].replace('_',' ')+'. Asset returned successfully when checked.'})
 if k=='2d36d8908aa74571':v['description']='Provides primary healthcare and offers Medicare and TRICARE health plans.'
 if not v['website']:v['website_status']='unresolved';v['review_outcome']='partial'
 v['sources']=[s for s in v['sources'] if s.get('url','').startswith('https://') and s.get('claim')]
 
 if k=='122da9e1b275899e':v.update(kind='Cooperative',ownership='Member-owned cooperative')
 elif v['kind']=='Tax-exempt organization':v['kind']='Nonprofit organization'
 if k in ambiguous:v['notes']+=' The filed site uses a group, abbreviated or successor brand; the exact entity-to-site relationship still needs confirmation. No group logo is assigned.'
 v['featured']=k=='131bc4da86e46dd6'
 out[k]=v
assert len(out)==30
(r/'next30-reviewed.json').write_text(json.dumps(out,indent=2)+'\n');print('Reviewed',len(out),'ID-keyed records.')
