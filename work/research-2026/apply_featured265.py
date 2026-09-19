import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));b=json.load(open(r/'identity265-batch.json'))
ids=[x['id'] for x in b['records']]+['1ee5fde93ffb146a','9ca0cdc55522b05f']
f=r/'featured265-before.json';assert not f.exists();f.write_text(json.dumps({i:p[i] for i in ids},indent=2,ensure_ascii=False)+'\n')
for x in b['records']:
 q=p[x['id']];q['description']=x['description'];q['notes']=x['recommendation']+' Official page evidence includes cached captures from September 6; reviewed September 14, 2026. Ownership remains unconfirmed.';q['identity_evidence']=q['notes'];q['checked_at']='2026-09-14'
 if x['identity_status'].startswith('confirmed'):q['review_outcome']='confirmed'
 if x['id']=='f36438f68e22d4fc':q['legal_form']='LLC'
 for s in x['sources']:
  source={'url':s['url'],'label':'Original registration evidence' if s['retrieval_ref'].endswith('.xml') else 'Official organization evidence','claim':s['excerpt']}
  if source not in q['sources']:q['sources'].append(source)
q=p['1ee5fde93ffb146a'];q.update(name='Okapi Global LLC (represented by Checkmate Government Relations)',description='Reports facilitating lawful imports and exports of wildlife and wildlife products.',kind='Wildlife-trade business',website='',website_status='unresolved',checked_at='2026-09-14')
q['notes']='The LDA client record identifies Okapi Global LLC, formerly Okapi Global, as the beneficiary represented through Checkmate. Wildlife-trade activity is self-reported. Checkmate’s website belongs to the intermediary and has been removed from the beneficiary website field. Okapi’s own website and ownership remain unverified.';q['identity_evidence']=q['notes']
q=p['9ca0cdc55522b05f'];q.update(name='T1 Energy (represented by Checkmate Government Relations)',description='Solar manufacturer building U.S. solar and battery supply chains; this filing names Checkmate as an intermediary representing T1 Energy.',kind='Solar manufacturer',website='https://t1energy.com/',checked_at='2026-09-14',review_outcome='confirmed')
q['notes']='The 2026 second-quarter amendment explicitly names Checkmate Government Relations on behalf of T1 Energy, with Riverbend Navigators as registrant. T1’s official website identifies T1 Energy Inc., Austin, Texas, and solar manufacturing. The website field now points to the represented company. This entry retains the original intermediary filing label; current ownership was not rechecked in this pass.';q['identity_evidence']=q['notes'];q['sources'].append({'url':'https://t1energy.com/','label':'Official represented-company website','claim':'Official page names T1 Energy Inc., Austin, Texas, and describes domestic solar and battery supply chains; retrieved September 14, 2026.'})
(r/'featured265-decisions.json').write_text(json.dumps({i:p[i] for i in ids},ensure_ascii=False,indent=2)+'\n')
(r/'reviewed.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')))
Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
print('Updated six profiles; three identity confirmations; removed one incorrect beneficiary website.')
