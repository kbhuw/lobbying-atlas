import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));ids={x['id'] for x in json.load(open(r/'featured60-input.json'))[:20]};(r/'featured60-agents-before.json').write_text(json.dumps({i:p[i] for i in ids},indent=2)+'\n');dec=[]
for x in json.load(open(r/'featured60-first10.json')):
 i=x['originalID'];assert i in ids
 if x['decision']!='confirm':dec.append(dict(id=i,decision='hold',evidence=x['evidence']));continue
 patch=x['proposed'];ev=x['evidence']
 if i=='a4f745a8a538a486':patch['ownership']='Unknown';ev+=' The quoted sources establish its operating subsidiaries, not ownership of Flix North America itself.'
 p[i].update(patch);p[i].update(review_outcome='confirmed',website_status='verified',identity_evidence=ev,notes=ev,checked_at='2026-09-13',as_of='2026-09-13',status='sourced')
 for s in x['exact_quotes']:
  if s['url'] not in [a['url'] for a in p[i]['sources']]:p[i]['sources'].append(dict(url=s['url'],label='Primary organization evidence',claim=ev))
 dec.append(dict(id=i,decision='confirmed',evidence=ev))
for x in json.load(open(r/'featured60-middle10.json')):
 i=x['id'];assert i in ids
 if x['decision']=='hold' or i=='378de43db159ab06':dec.append(dict(id=i,decision='hold',evidence=x.get('unresolved','')));continue
 patch=x['final_patch'];ev=x['evidence'];urls=[x['source_url']]
 if i=='bfda374a5663593d':urls.append('https://formenergy.com/privacy-policy/');ev+=' Root verified official privacy policy address 30 Dane St, Somerville, matching the registration.'
 if i=='a04536c3ad4466ff':urls.append('https://www.franklintempleton.com/corporate/about-us/corporate-name-change');ev+=' Official announcement says Franklin Resources Inc became Franklin Templeton Inc effective August 17, 2026, with NYSE BEN listing unchanged. Original parent-plus-affiliates filing scope preserved.'
 if i=='a321f45810c53c8a':urls.append('https://oig.hhs.gov/documents/cias/10275/Fresno_Community_Hospital_and_Medical_Center_05072025.pdf');ev+=' HHS OIG 2025 agreement explicitly names Fresno Community Hospital and Medical Center d/b/a Community Health System and communitymedical.org contact.'
 if i=='57026e3c3477239e':patch['name']='Freedom From Religion Foundation';urls.append(x['activity_url'])
 p[i].update(patch);p[i].update(review_outcome='confirmed',website_status='verified',identity_evidence=ev,notes=ev,checked_at='2026-09-13',as_of='2026-09-13',status='sourced')
 for u in urls:
  if u not in [a['url'] for a in p[i]['sources']]:p[i]['sources'].append(dict(url=u,label='Primary organization evidence',claim=ev))
 dec.append(dict(id=i,decision='confirmed',evidence=ev))
(r/'featured60-agents-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f,c in [(r/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:f.write_text(json.dumps(p,ensure_ascii=False,indent=None if c else 2)+('' if c else '\n'))
print('confirmed',sum(x['decision']=='confirmed' for x in dec))
