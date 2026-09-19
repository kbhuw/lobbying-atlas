import json,copy,pathlib,zipfile
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured174-before.json').exists()
v=json.load(open(r/'legal-sites169-review.json'))[29];rows=[v];before={};dec=[]
v['fetched_evidence']=[e for e in v['fetched_evidence'] if e['http_status']==200]
extra={v['id']:json.load(open(r/'featured174-amp-evidence.json'))}
notes={v['id']:'Official December 14, 2021 announcement explicitly identifies Amp Americas II LLC as Amp Americas and describes dairy-waste renewable-gas projects. Current About body describes developing, owning and operating waste-to-fuel assets. This establishes the legal-name-to-brand bridge. Historical acquisition, investor and operating quantities remain dated; carbon-negative performance is a company claim, not independently verified.'}
for row in rows:
 i=row['id'];assert p[i]['review_outcome']!='confirmed';before[i]=copy.deepcopy(p[i]);note=notes[i]
 p[i].update(description=row['description'],review_outcome='confirmed',website_status='verified',notes=note,identity_evidence=note,checked_at='2026-09-13',as_of='2026-09-13')
 p[i]['description']='Develops, owns and operates projects that convert dairy and other waste into renewable natural gas and other fuels.'
 evidence=copy.deepcopy(row['fetched_evidence'])
 if i in extra:evidence.append(extra[i])
 ss={s['url']:s for s in p[i]['sources']}
 for e in evidence:
  assert e['http_status']==200
  s=BeautifulSoup(open(e['cache_path']).read(),'html.parser')
  for t in s(['script','style','nav','header']):t.decompose()
  e['reviewed_body']=s.get_text(' ',strip=True);ss[e['url']]={'url':e['url'],'label':'Primary identity evidence','claim':note}
 p[i]['sources']=list(ss.values());dec.append(dict(id=i,name=p[i]['name'],notes=note,evidence=evidence))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured174-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(len(dec),'confirmed')
