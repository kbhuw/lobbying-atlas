import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def put(i,patch,ev,urls,replace=False):
 before[i]=json.loads(json.dumps(p[i]));a=p[i]
 if replace:
  for k in list(a):
   if k.startswith('logo_'):del a[k]
  a['sources']=[]
 a.update(patch);a.update(review_outcome='confirmed',website_status='verified',identity_evidence=ev,notes=ev,checked_at='2026-09-13',as_of='2026-09-13',status='sourced')
 for u in dict.fromkeys(urls):
  if u not in [s['url'] for s in a['sources']]:a['sources'].append(dict(url=u,label='Primary organization evidence',claim=ev))
 dec.append(dict(id=i,patch=patch,evidence=ev,urls=urls))
put('ba4ab3c6bd789b8d',dict(name='Addus HomeCare',description='Provides personal care, home health and hospice services.',kind='Home healthcare company',ownership='Publicly traded (Nasdaq: ADUS)',website='https://addus.com/'),'Original directory source ID identifies Addus HomeCare. Its official investor FAQ identifies Addus HomeCare Corporation and Nasdaq ADUS; service links describe home care, home health and hospice. Prior Accendra Health annotation, ACH ticker, sources and logo belonged to a different organization and were removed.',['https://addus.gcs-web.com/shareholder-services/investor-faqs','https://addus.gcs-web.com/'],True)
put('67ac8fd8a092c612',dict(name='Element US NTS (Element U.S. Space & Defense)',description='Provides laboratory testing and engineering services for aerospace, defense and other industries.',kind='Testing and engineering services',ownership='Unknown',website='https://www.elementdefense.com/'),'Original 2024 registration 301604073.xml identifies Element US NTS, testing and engineering services, at 4603B Compass Point Road, Belcamp. Official Element U.S. Space & Defense site identifies the same testing business and Compass Point facility. NIJ laboratory notice confirms Element U.S. Space & Defense at 4603 Compass Point Road. Removed unrelated Elementl Power nuclear-company annotation and logo. Legal suffix and current ownership remain unknown.',['https://www.elementdefense.com/','https://cjttec.org/files/69c59a5de9103','https://disclosurespreview.house.gov/data/LD/2024_Registrations_XML.zip'],True)
for x in json.load(open(r/'featured59-first10.json')):
 if x['decision']!='confirm':continue
 if x['originalID']=='15601d23b95ac54e':x['originalID']='15601d23b95ac54f'
 patch=x['proposed'].copy();ev=x['evidence']
 if x['originalID']=='a1c4f3d661f9a102':patch['ownership']='Unknown';ev+=' Current listing not independently established by the quoted homepage; ownership remains Unknown.'
 put(x['originalID'],patch,ev,[s['url'] for s in x['exact_quotes']])
for x in json.load(open(r/'featured59-middle10.json')):
 if x['decision']=='hold':continue
 patch=x['final_patch'].copy();ev=x['evidence'];urls=[v for k,v in x.items() if k.endswith('_url')]
 if x['id'] in ['7c24b1ac52c55238','52010d8018a2ecbe']:patch['ownership']='Unknown';ev+=' The quoted source does not independently establish current ownership or tax-exempt status; that field remains Unknown.'
 if x['id']=='52010d8018a2ecbe':ev+=' The official LLC document is hosted under a 2021 path; it establishes historical legal identity without a current parent percentage.'
 if x['id']=='dd4af5c9ad3f597a':urls.append('https://www.seattlefwc26.org/');ev+=' Root verified local site identifies Seattle Local Organizing Committee and its World Cup program.'
 if x['id']=='d1a26e8cacb2af3b':urls.append('https://bayareahostcommittee.com/');ev+=' Root verified host-committee homepage links its FIFA World Cup program.'
 put(x['id'],patch,ev,urls)
(r/'featured59-root-before.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n');(r/'featured59-root-decisions.json').write_text(json.dumps(dec,indent=2,ensure_ascii=False)+'\n')
for f,c in [(r/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:f.write_text(json.dumps(p,ensure_ascii=False,indent=None if c else 2)+('' if c else '\n'))
print(len(dec),'profiles saved')
