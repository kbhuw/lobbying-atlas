import json,gzip
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));ids=['e07a29bdebc07399','012e4c7ecdf2a97f']
b=json.load(open(r/'featured310-before.json'))
assert not any(i in b for i in ids)
b.update({i:p[i] for i in ids});(r/'featured310-before.json').write_text(json.dumps(b,indent=2,ensure_ascii=False)+'\n')
n='The official APTA About page identifies the American Public Transportation Association as a nonprofit and gives 1300 I Street NW, Suite 1200 East, Washington DC. The 2016 self-registration and 2019 client registration with the parenthetical APTA acronym use this same address and transit-association activity. Both records represent the same organization; the acronym variant is consolidated while all original filings, intermediaries and source IDs are preserved.'
for i in ids:
 p[i].update(review_outcome='confirmed',ownership='Nonprofit',website_status='verified',checked_at='2026-09-14',notes=n,identity_evidence=n)
 p[i]['sources'].append({'url':'https://www.apta.com/about/','label':'Official APTA About body inspected September 14, 2026','claim':n})
mp=Path('lobbying-map/research/verified-entity-merges.json');m=json.load(open(mp));assert not any(set(ids)&set(x['source_ids']) for x in m)
(r/'featured310-merge-before.json').write_text(json.dumps(m,indent=2)+'\n')
d=json.load(gzip.open('lobbying-map/public/data/directory-v3.json.gz','rt'));cards={c['id']:c for c in d['companies'] if c['id'] in ids};assert len(cards)==2
(r/'featured310-cards-before.json').write_text(json.dumps(cards,indent=2)+'\n')
m.append({'canonical_id':ids[0],'source_ids':ids,'rationale':n,'sources':[{'url':'https://www.apta.com/about/','label':'Official APTA About page','claim':'Full name, acronym, nonprofit status and Washington DC address.'},{'url':'https://disclosurespreview.house.gov/data/LD/2016_Registrations_XML.zip','label':'Self-registration 300779926.xml','claim':'Full-name association at 1300 I Street NW Suite1200East, DC20005.'},{'url':'https://disclosurespreview.house.gov/data/LD/2019_Registrations_XML.zip','label':'Client registration 301042210.xml','claim':'Same full name plus APTA acronym, same exact client address and transit-policy activity.'}],'reviewed_at':'2026-09-14'})
mp.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
(r/'reviewed.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');(r/'featured310-decisions.json').write_text(json.dumps({i:p[i] for i in b},indent=2,ensure_ascii=False)+'\n')
print('APTA identities confirmed and duplicate consolidated with original evidence retained.')
