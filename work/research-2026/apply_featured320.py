import json
from pathlib import Path
r=Path('work/research-2026'); p=json.load(open(r/'reviewed.json'))
rows=[q for n in (318,319) for q in json.load(open(r/f'identity{n}-batch.json'))['records']]
ids=[q['id'] for q in rows]+['48fd437d42918947']
b=r/'featured320-before.json'; assert not b.exists(); b.write_text(json.dumps({i:p[i] for i in ids},indent=2,ensure_ascii=False)+'\n')
for q in rows:
 i=q['id']; note=' '.join(s['excerpt'] for s in q['sources'])
 note+=' Official organization evidence reviewed September 14, 2026, including indexed official bodies. Identity confirmation does not establish fields left unknown.'
 p[i].update(description=q['description'],website=q['website'],website_status='verified',review_outcome='confirmed',checked_at='2026-09-14',identity_evidence=note,notes=note)
 for s in q['sources']:
  p[i]['sources'].append({'url':s['url'],'label':'Official organization evidence reviewed September 14, 2026','claim':s['excerpt']})
for i in ['d1fd6e0e438d2c00','6e70d667326de209','fa619ea2bd426dbd','a5ed69f83191ceaf']:
 p[i]['ownership']='Nonprofit / tax-exempt'
for i in ['0aff537af70861c7','2942ce1430e38108','63b2f3ebf26ca85c']:
 p[i]['legal_form']='Corporation'
p['e346c74388dae9e8']['ownership']='Government body'
p['9025d31a944f6922']['description']='Coalition of community foundations educating the public and policymakers about community philanthropy and local needs.'
p['fa619ea2bd426dbd']['description']='New York nonprofit corporation forming part of The New York Community Trust, which manages donor-advised and other charitable funds. It shares governance and a tax return with an associated organization of charitable trusts.'
p['fa619ea2bd426dbd']['website']='https://thenytrust.org/'
i='48fd437d42918947'; note='The official membership website identifies the Commissioned Officers Association of the USPHS Inc. and its representation of USPHS commissioned officers, including Capitol Hill advocacy and member benefits. The association is distinct from the federal Public Health Service itself. Direct official body retrieved September 14, 2026; tax status remains unknown.'
p[i].update(review_outcome='confirmed',checked_at='2026-09-14',identity_evidence=note,notes=note,legal_form='Corporation')
p[i]['sources'].append({'url':'https://coausphs.org/','label':'Official association membership website, retrieved September 14, 2026','claim':note})
(r/'featured320-decisions.json').write_text(json.dumps({i:p[i] for i in ids},indent=2,ensure_ascii=False)+'\n')
(r/'reviewed.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')))
Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
print('Saved 11 independently corroborated identities.')
