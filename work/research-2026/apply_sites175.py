import json,copy,pathlib,zipfile
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured175-before.json').exists()
v=json.load(open(r/'legal-sites169-review.json'))[6];rows=[v];before={};dec=[]
v['fetched_evidence']=[e for e in v['fetched_evidence'] if e['http_status']==200]
extra={}
notes={v['id']:'LDA client 68460 explicitly names Akin Gump Strauss Hauer & Field LLP on behalf of TP-Link Systems Inc., with Ballard Partners as registrant. Official U.S. TP-Link privacy policy explicitly names TP-Link Systems Inc. and its network/smart-home products. These independent sources establish the represented company and reported intermediary roles. The original filing label and intermediary relationship are preserved; no entities are merged.'}
for row in rows:
 i=row['id'];assert p[i]['review_outcome']!='confirmed';before[i]=copy.deepcopy(p[i]);note=notes[i]
 p[i].update(description=row['description'],review_outcome='confirmed',website_status='verified',notes=note,identity_evidence=note,checked_at='2026-09-13',as_of='2026-09-13')
 p[i]['description']='TP-Link Systems makes networking and smart-home products. In this filing, Ballard Partners reports lobbying for Akin Gump acting on behalf of TP-Link.'
 p[i]['kind']='Company represented through intermediary'
 evidence=copy.deepcopy(row['fetched_evidence'])
 if i in extra:evidence.append(extra[i])
 ss={s['url']:s for s in p[i]['sources']}
 for e in evidence:
  assert e['http_status']==200
  s=BeautifulSoup(open(e['cache_path']).read(),'html.parser')
  for t in s(['script','style','nav','header']):t.decompose()
  e['reviewed_body']=s.get_text(' ',strip=True);ss[e['url']]={'url':e['url'],'label':'Primary identity evidence','claim':note}
 p[i]['sources']=list(ss.values());dec.append(dict(id=i,name=p[i]['name'],notes=note,evidence=evidence))
api=json.load(open(r/'featured175-tplink-client.json'));assert api['http_status']==200
dec[0]['lda_client_evidence']=api
for name,value in [('before',before),('decisions',dec)]: (r/f'featured175-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(len(dec),'confirmed')
