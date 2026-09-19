import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));ids={x['id'] for x in json.load(open(r/'featured63-input.json'))[:20]};(r/'featured63-agents-before.json').write_text(json.dumps({i:p[i] for i in ids},indent=2)+'\n');dec=[]
def put(i,ev,urls,patch):
 assert i in ids;p[i].update(patch);p[i].update(review_outcome='confirmed',website_status='verified',identity_evidence=ev,notes=ev,status='sourced',checked_at='2026-09-13',as_of='2026-09-13')
 for u in urls:
  if u not in [s['url'] for s in p[i]['sources']]:p[i]['sources'].append(dict(url=u,label='Primary organization evidence',claim=ev))
 dec.append(dict(id=i,decision='confirmed',evidence=ev,urls=urls))
for x in json.load(open(r/'featured63-first10.json')):
 if x['decision']!='confirm':continue
 patch=x['proposed'];ev=x['evidence']
 if x['originalID']=='153e192d73989e17':patch['ownership']='Unknown';ev+=' ASTM relationship is dated2017 and not treated as newly verified ownership.'
 put(x['originalID'],ev,[s['url'] for s in x['exact_quotes']],patch)
for i,u,ev,o in [('25aaf0ffbf62952e','https://hargrove-epc.com/careers-2/','Official Hargrove Engineers & Constructors careers page explicitly states100%employee-owned and operated. Original filed brand and engineering activity match.','Employee-owned'),('26577b2fe8656f86','https://harrison.ai/about-us/','Official About page identifies Harrison.ai and radiology/pathology diagnostic-support tools. Original unsuffixed filed brand matches.','Unknown'),('2606f8fe771c0355','https://www.hartreepartners.com/hartree-legal-notice/','Official legal notice explicitly identifies Hartree Partners LP and preserves separate affiliates. Official Who We Are identifies founders, senior staff and Oaktree-managed funds as owners.','Private: founders, senior staff and Oaktree-managed funds'),('b78f1e9553ad9d6a','https://www.harmonybiosciences.com/wp-content/uploads/2025/03/Harmony-Consumer-Health-Data-Privacy-Notice.pdf','Official health-data privacy notice explicitly lists Harmony Biosciences LLC separately from Holdings Inc. Original LLC identity confirmed; public status of Holdings is not transferred.','Unknown')]:put(i,ev,[u],dict(ownership=o))
p['2606f8fe771c0355']['sources'].append(dict(url='https://www.hartreepartners.com/who-we-are/',label='Ownership',claim='Names founding partners, senior staff and Oaktree-managed funds as owners.'))
p['35a94972466b5041']['kind']='Agricultural technology';dec.append(dict(id='35a94972466b5041',decision='partial correction',evidence='Correct erroneous County government category to Agricultural technology; exact LLC still unverified.'))
a=p['3bce437667cd4b00'];a['ownership']='Unknown';a['notes']+=' Terms carry2014copyright; CB-HDT relationship is historical source context and not verified currentownership.';a['identity_evidence']=a['notes'];a['sources'].append(dict(url='https://www.hdtglobal.com/wp-content/uploads/2026/03/HDT_C2-Datasheet-Book_07.pdf',label='Current exact identity',claim='March2026 datasheet names HDT Expeditionary Systems Inc.,30500AuroraRoadSolon.'))
seen={x['id'] for x in dec};dec += [dict(id=i,decision='hold',evidence='Exact legal identity or continuity requires further evidence.') for i in ids-seen];(r/'featured63-agents-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f,c in [(r/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:f.write_text(json.dumps(p,ensure_ascii=False,indent=None if c else 2)+('' if c else '\n'))
print('10new confirmed plus Halter category correction and dated HDT ownership correction')
