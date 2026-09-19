import json,copy,pathlib,zipfile
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured168-before.json').exists()
x=json.load(open(r/'filed-sites167-followups.json'));v=json.load(open(r/'verified-sites163-next100-review.json'))[33];rows=[x[0],x[1],v];before={};dec=[]
extra={x[1]['id']:json.load(open(r/'featured168-nebraska-evidence.json')),v['id']:json.load(open(r/'featured168-vulncheck-evidence.json'))}
notes={x[0]['id']:'2024 Form 990 names American Horticulture Industry Association, EIN 46-4411915, Columbus, Ohio, reports americanhort.org and subsection 501(c)(6). The current AmericanHort site confirms horticultural advocacy, education and industry programs. The tax filing establishes the legal-name-to-brand connection.',x[1]['id']:'House registration 301779790.xml in the 2025 archive names University of Nebraska at 3835 Holdrege Street, Lincoln, NE 68583. The official University of Nebraska System contact page gives the exact same address; homepage describes its constituent campuses. This confirms the system-level client rather than selecting a single campus.',v['id']:'Official VulnCheck privacy policy explicitly names VulnCheck Inc. and its Lexington, Massachusetts headquarters. Its homepage describes exploit and vulnerability intelligence products. Legal identity is established without inferring ownership or independently certifying product performance.'}
for row in rows:
 i=row['id'];assert p[i]['review_outcome']!='confirmed';before[i]=copy.deepcopy(p[i]);note=notes[i]
 p[i].update(description=row['description'],review_outcome='confirmed',website_status='verified',notes=note,identity_evidence=note,checked_at='2026-09-13',as_of='2026-09-13')
 if i==x[0]['id']:p[i]['ownership']='Nonprofit'
 evidence=copy.deepcopy(row['fetched_evidence'])
 if i in extra:evidence.append(extra[i])
 ss={s['url']:s for s in p[i]['sources']}
 for e in evidence:
  assert e['http_status']==200
  s=BeautifulSoup(open(e['cache_path']).read(),'html.parser')
  for t in s(['script','style','nav','header']):t.decompose()
  e['reviewed_body']=s.get_text(' ',strip=True);ss[e['url']]={'url':e['url'],'label':'Primary identity evidence','claim':note}
 p[i]['sources']=list(ss.values());dec.append(dict(id=i,name=p[i]['name'],notes=note,evidence=evidence))
with zipfile.ZipFile('work/federal-directory/raw/2025_Registrations_XML.zip') as z:
 n=next(n for n in z.namelist() if n.endswith('301779790.xml'));(r/'featured168-nebraska-registration.xml').write_bytes(z.read(n))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured168-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(len(dec),'confirmed')
