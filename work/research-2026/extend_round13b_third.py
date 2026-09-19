import json,pathlib,gzip
r=pathlib.Path('work/research-2026');cs={c['id']:c for c in json.load(open(r/'general-round13-b-input.json'))};f=r/'general-round13-b-root-partial.json';p=json.load(open(f))
def add(k,desc,kind,own,site,url,claim):
 c=cs[k];v=dict(c.get('profile',{}));v.update(name=c['name'],description=desc,kind=kind,ownership=own,website=site,status='sourced',review_outcome='partial' if own=='Unknown' else 'confirmed',identity_evidence='Official organization source matches disclosed name and activity.',notes='Individually researched using primary organization evidence; filing name retained.'+(' Ownership not established by reviewed sources.' if own=='Unknown' else ''),as_of='2026-09-05',checked_at='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='');v['sources']=v.get('sources',[])
 if not v['sources']:
  rid=json.load(gzip.open(f'lobbying-map/public/data/reports/{k[:2]}.json.gz'))[k][0]['id'];v['sources']=[{'url':f'https://lda.gov/filings/public/filing/{rid}/print/','label':'Lobbying disclosure','claim':'Original disclosed client name.'}]
 v['sources'].append({'url':url,'label':'Official organization evidence','claim':claim});p[k]=v
add('17657bc809a21991','Manufactures IOSAT potassium iodide tablets used for thyroid protection during radioactive-iodine emergencies.','Company','Unknown','https://www.anbex.com/','https://www.anbex.com/','Anbex Inc. identifies itself as the manufacturer of IOSAT potassium iodide tablets.')
add('b1b23abbe58a918c','Develops artificial-intelligence systems for threat detection in passenger, baggage and package security screening.','Company','Unknown','https://www.analyticalai.com/','https://www.analyticalai.com/','Analytical AI describes its security-screening machine-learning products and Birmingham, Alabama location.')
f.write_text(json.dumps(p,indent=2)+'\n');print(len(p))
