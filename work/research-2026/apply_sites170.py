import json,copy,pathlib,zipfile
from bs4 import BeautifulSoup
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured170-before.json').exists()
xs=json.load(open(r/'legal-sites169-review.json'));rows=[xs[n] for n in [9,12,19,28]];before={};dec=[];extra={}
notes={'405b80eaef25fecd': 'Official body explicitly names Alliance for Financing U. S. Infrastructure Inc., states 501(c)(6) status and describes federal infrastructure-bank advocacy. Spacing in U.S. is not a different identity. The proposed bank and bill are not treated as an operating bank or enacted law.', '1f465a247cc706bd': 'Official privacy page explicitly describes America First Agriculture advocacy for federal cannabis reform and names America First Agriculture Inc. in its footer. The unfinished homepage does not negate this substantive legal-page evidence. Announced campaign budget is not verified spending.', 'e80505e84faa7681': 'Official AFSCME body describes union representation and its footer spells out American Federation of State, County and Municipal Employees, AFL-CIO. Punctuation differences do not create a separate identity. International union and local affiliates remain separate.', 'dd7b97abbad10d7c': 'Official AMIkids body describes nationwide community and residential youth programs, education, workforce development, treatment and service coordination. AMI Kids is a spacing variant of the displayed brand; individual local programs remain separate. Claimed success rates are not independently established.'}
for row in rows:
 i=row['id'];assert p[i]['review_outcome']!='confirmed';before[i]=copy.deepcopy(p[i]);note=notes[i]
 p[i].update(description=row['description'],review_outcome='confirmed',website_status='verified',notes=note,identity_evidence=note,checked_at='2026-09-13',as_of='2026-09-13')
 if i=='1f465a247cc706bd':p[i]['description']='Advocates for federal cannabis-policy reform through public-affairs campaigns and industry coordination.'
 evidence=copy.deepcopy([e for e in row['fetched_evidence'] if e['http_status']==200])
 if i in extra:evidence.append(extra[i])
 ss={s['url']:s for s in p[i]['sources']}
 for e in evidence:
  assert e['http_status']==200
  s=BeautifulSoup(open(e['cache_path']).read(),'html.parser')
  for t in s(['script','style','nav','header']):t.decompose()
  e['reviewed_body']=s.get_text(' ',strip=True);ss[e['url']]={'url':e['url'],'label':'Primary identity evidence','claim':note}
 p[i]['sources']=list(ss.values());dec.append(dict(id=i,name=p[i]['name'],notes=note,evidence=evidence))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured170-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(len(dec),'confirmed')
