import json,pathlib,gzip
r=pathlib.Path('work/research-2026');cs={c['id']:c for c in json.load(open(r/'general-round14-b-input.json'))};f=r/'general-round14-b-root-partial.json';p=json.load(open(f)) if f.exists() else {}
def add(k,desc,kind,own,site,url,claim):
 c=cs[k];v=dict(c.get('profile',{}));v.update(name=c['name'],description=desc,kind=kind,ownership=own,website=site,status='sourced',review_outcome='partial' if own=='Unknown' else 'confirmed',identity_evidence='Official organization source matches disclosed name and activity.',notes='Individually researched using primary organization evidence; filing name retained.'+(' Ownership not established by reviewed sources.' if own=='Unknown' else ''),as_of='2026-09-05',checked_at='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='');v['sources']=v.get('sources',[])
 if not v['sources']:
  rid=json.load(gzip.open(f'lobbying-map/public/data/reports/{k[:2]}.json.gz'))[k][0]['id'];v['sources']=[{'url':f'https://lda.gov/filings/public/filing/{rid}/print/','label':'Lobbying disclosure','claim':'Original disclosed client name.'}]
 v['sources'].append({'url':url,'label':'Official organization evidence','claim':claim});p[k]=v
add('ddfadce2925ed35f','Provides software for automating business processes and workflows in enterprises and government organizations.','Company','Publicly traded','https://appian.com/','https://investors.appian.com/','Current investor-relations page identifies Appian and its process-automation business, NASDAQ: APPN.')
for k in ['7880bbc5c88285b9','0137405595802ede']:
 add(k,'Provides scientific and engineering research, systems development, modeling, testing and technical services for defense, infrastructure, health and energy applications.','Company','Employee-owned','https://www.ara.com/','https://www.ara.com/','Applied Research Associates identifies itself as 100% employee-owned and describes its science and engineering capabilities.')
add('cfe27636ca34754c','Develops software and AI systems for autonomous vehicles, robotics and other machines, including simulation, vehicle operating systems and self-driving technology.','Company','Unknown','https://www.appliedintuition.com/','https://www.appliedintuition.com/','Applied Intuition describes its vehicle-intelligence tools, vehicle operating system and self-driving platform.')
p['cfe27636ca34754c']['featured']=True
f.write_text(json.dumps(p,indent=2)+'\n');print(len(p))
