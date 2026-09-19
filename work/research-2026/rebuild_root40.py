import json,pathlib,datetime,re,urllib.parse
r=pathlib.Path('work/research-2026');descriptions=dict(line.split('\t',1) for line in (r/'root40-descriptions.tsv').read_text().splitlines());out={};holds=json.load(open('lobbying-map/research/registry-match-holds.json'))
# Root checked the cached page identities; redirects to renamed/ambiguous organizations remain filed.
ambiguous={'01d431c321afa175','04dd6f1441fda94b','0af2c635ea108bdb','0d94f9ea5b9a5578','1012388cb95f7c53','11b9da3cd20fcaec'}
for x in json.load(open(r/'root-next-40.json')):
 k=x['id']
 if k in holds or k not in descriptions:continue
 d=x['tax_evidence'];a=json.load(open(r/'website-cache'/f'{k}.json'));base=x['registry_profile'];v={'name':x['name'],'description':descriptions[k],'kind':base.get('kind','Nonprofit / initiative'),'ownership':'Not applicable','website':a.get('requested_url',''),'sources':list(base['sources']),'status':'sourced','featured':False,'legal_form':'','checked_at':'2026-09-05','as_of':'2026-09-05','notes':'Description reviewed against this organization’s filed mission. Website identity was checked separately; filed links may be historical.','identity_evidence':'EIN '+d['ein']+'; filed legal name '+d.get('organization_name','')+'; matched to the lobbying disclosure using the original registry evidence.','logo_url':'','logo_kind':'','logo_source_url':'','logo_status':'unresolved'}
 for old,new in [(' RED ',' Red '),(' TO ',' to '),(' ON ',' on '),(' LAW ',' Law '),(' GAS ',' Gas '),('For ALL','for All'),('Issue ONE','Issue One'),('Medstar','MedStar'),('Naadac','NAADAC'),('Jobsohio','JobsOhio'),('GBS Cidp','GBS-CIDP'),('Dance/usa','Dance/USA'),('Ctia ','CTIA '),('Womens','Women’s'),('Usagainstalzheimers','UsAgainstAlzheimer’s')]:v['name']=v['name'].replace(old,new)
 v['sources'].append({'label':'Filed mission and website — EIN '+d['ein'],'url':d['source_url'],'claim':'Form 990 reports the mission and website for '+d.get('organization_name','')+'. The description is a plain-English paraphrase of this record.'})
 verified=a.get('http_status')==200 and len(a.get('text',''))>50 and k not in ambiguous
 v['website_status']='verified' if verified else 'filed';v['review_outcome']='confirmed' if verified else 'partial'
 if verified:
  v['sources'].append({'label':'Official organization website','url':a['final_url'],'claim':'Page identity and activity reviewed against the organization name and filed mission.'})
  if a.get('logo_http_status')==200:
   for field in ['logo_url','logo_kind','logo_source_url']:v[field]=a[field]
   v['logo_status']='official_site_asset';v['sources'].append({'label':'Official website branding','url':a['logo_source_url'],'claim':'Page supplies this '+a['logo_kind'].replace('_',' ')+'. Asset returned successfully when checked.'})
 if k=='2d36d8908aa74571':v['description']='Provides primary healthcare and offers Medicare and TRICARE health plans.'
 if not v['website']:v['website_status']='unresolved';v['review_outcome']='partial'
 v['sources']=[s for s in v['sources'] if s.get('url','').startswith('https://') and s.get('claim')]
 out[k]=v
assert len(out)==38
(r/'root-reviewed-40.json').write_text(json.dumps(out,indent=2)+'\n');print('Rebuilt',len(out),'profiles from original ID-keyed evidence; held 2 records needing more source detail.')
