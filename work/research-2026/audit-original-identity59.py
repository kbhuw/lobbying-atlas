import json,gzip,re,unicodedata
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));b={v['id']:v for v in json.load(gzip.open('lobbying-map/research/directory-base.json.gz','rt'))['companies']}
stop=set('the and of for inc incorporated llc corporation company co corp ltd limited group holdings services international usa us america american association foundation national partners lp plc'.split())
def tok(s):return set(re.findall('[a-z0-9]+',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()))-stop
out=[]
for i,v in p.items():
 orig=b[i]['aliases'];pt=tok(v['name']);ot=set().union(*(tok(s) for s in orig))
 if pt and ot and not(pt&ot):out.append(dict(id=i,original_aliases=orig,profile_name=v['name'],website=v.get('website'),review_outcome=v.get('review_outcome'),evidence=v.get('identity_evidence')))
(r/'identity-name-disjoint59.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print('No shared distinctive name tokens:',len(out));print(json.dumps(out[:45],ensure_ascii=False,indent=2))
