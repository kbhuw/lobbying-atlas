import json,pathlib,datetime,re,urllib.parse
r=pathlib.Path('work/research-2026');descriptions=dict(line.split('\t',1) for line in (r/'root-descriptions.tsv').read_text().splitlines());out={};holds=json.load(open('lobbying-map/research/registry-match-holds.json'))
# Root checked the cached page identities; redirects to renamed/ambiguous organizations remain filed.
ambiguous={'1099248bc32f3570','31918852d365cf16','0738c2b026e45771','09a620c286498fa8','125b6be23ec62999','1729c774f7540526','1c2f88d1b571c5a0','2486ab3ebdfc2746','254a568c8a49b1de','294aef08682683c9','2a9d3249f8f7941f','2f82f961007515bf','2fa5aac1cc13607c'}
for x in json.load(open(r/'tax-large-0.json')):
 k=x['id']
 if k in holds:continue
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
assert len(out)==98
(r/'root-reviewed-large-0.json').write_text(json.dumps(out,indent=2)+'\n');print('Rebuilt',len(out),'profiles from original ID-keyed evidence; held 2 foundation-related records.')
