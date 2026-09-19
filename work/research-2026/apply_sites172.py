import json,copy,pathlib,zipfile
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured172-before.json').exists()
v=json.load(open(r/'legal-sites169-review.json'))[2];rows=[v];before={};dec=[]
v['fetched_evidence']=[json.load(open(r/'featured172-acxiom-tos-evidence.json')),json.load(open(r/'featured172-acxiom-extra.json'))[1]]
extra={}
notes={v['id']:'Official U.S. terms of service dated July 1, 2026 explicitly identify Acxiom LLC as the service provider. The U.S. About page describes marketing data, identity and technology services. The former acxiom.co.uk privacy page names Acxiom Limited, a different regional legal entity; the canonical website is corrected to acxiom.com. The privacy page retains older Interpublic references while the current About page describes Omnicom; no unsupported ownership percentage is inferred.'}
for row in rows:
 i=row['id'];assert p[i]['review_outcome']!='confirmed';before[i]=copy.deepcopy(p[i]);note=notes[i]
 p[i].update(description=row['description'],review_outcome='confirmed',website_status='verified',notes=note,identity_evidence=note,checked_at='2026-09-13',as_of='2026-09-13')
 p[i]['website']='https://www.acxiom.com/'
 p[i]['description']='Provides consumer data, identity-resolution and marketing technology services to brands and agencies.'
 evidence=copy.deepcopy(row['fetched_evidence'])
 if i in extra:evidence.append(extra[i])
 ss={s['url']:s for s in p[i]['sources']}
 for e in evidence:
  assert e['http_status']==200
  s=BeautifulSoup(open(e['cache_path']).read(),'html.parser')
  for t in s(['script','style','nav','header']):t.decompose()
  e['reviewed_body']=s.get_text(' ',strip=True);ss[e['url']]={'url':e['url'],'label':'Primary identity evidence','claim':note}
 p[i]['sources']=list(ss.values());dec.append(dict(id=i,name=p[i]['name'],notes=note,evidence=evidence))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured172-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(len(dec),'confirmed')
