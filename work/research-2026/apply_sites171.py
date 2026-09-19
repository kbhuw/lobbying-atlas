import json,copy,pathlib,zipfile
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured171-before.json').exists()
xs=json.load(open(r/'legal-sites169-review.json'));rows=[xs[n] for n in [17,18]];before={};dec=[]
extra={xs[18]['id']:json.load(open(r/'featured171-evidence.json'))[1]}
notes={'90e6bb98a11d66c1': 'Official AFGE Council 220 homepage identifies the council and representation of Social Security Administration field-office, teleservice-center and workload-support employees. Council identity is kept separate from the national union and individual locals. Policy and staffing assertions are not independently verified.', 'a1119f66a62aa526': 'Official AFGE Local 476 About page explicitly names the American Federation of Government Employees affiliation, Council 222 relationship and HUD workplaces represented. This is the local union, not the national AFGE organization; membership counts are attributed to the site.'}
for row in rows:
 i=row['id'];assert p[i]['review_outcome']!='confirmed';before[i]=copy.deepcopy(p[i]);note=notes[i]
 p[i].update(description=row['description'],review_outcome='confirmed',website_status='verified',notes=note,identity_evidence=note,checked_at='2026-09-13',as_of='2026-09-13')
 if i==xs[17]['id']:p[i]['description']='A union council representing Social Security Administration employees in field offices, teleservice centers and workload-support units.'
 if i==xs[18]['id']:p[i]['description']='A local federal-employee union representing HUD workers at its headquarters, Washington field office and Los Angeles Departmental Enforcement Center.'
 evidence=copy.deepcopy([e for e in row['fetched_evidence'] if e['http_status']==200])
 if i in extra:evidence.append(extra[i])
 ss={s['url']:s for s in p[i]['sources']}
 for e in evidence:
  assert e['http_status']==200
  s=BeautifulSoup(open(e['cache_path']).read(),'html.parser')
  for t in s(['script','style','nav','header']):t.decompose()
  e['reviewed_body']=s.get_text(' ',strip=True);ss[e['url']]={'url':e['url'],'label':'Primary identity evidence','claim':note}
 p[i]['sources']=list(ss.values());dec.append(dict(id=i,name=p[i]['name'],notes=note,evidence=evidence))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured171-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(len(dec),'confirmed')
