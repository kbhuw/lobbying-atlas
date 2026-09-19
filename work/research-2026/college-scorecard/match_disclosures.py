import json,pathlib,sqlite3,re,collections
r=pathlib.Path('work/research-2026/college-scorecard');candidates=json.load(open(r/'2026-candidates.json'))
def norm(s):return re.sub('[^a-z0-9]','',(s or '').lower())
keys={norm(a) for x in candidates for a in x['aliases']+[x['name']]};db=sqlite3.connect('work/organization-research/bulk-profiles.sqlite');db.row_factory=sqlite3.Row;db.create_function('wanted',1,lambda s:int(norm(s) in keys));rows=collections.defaultdict(list)
for q in db.execute('SELECT name,description,state,city,principal_state,principal_city,source_url,source_member,signed_date,report_year FROM descriptions WHERE wanted(name)'):
 d=dict(q);rows[norm(d['name'])].append(d)
out=[]
for c in candidates:
 obs=[d for a in set(c['aliases']+[c['name']]) for d in rows[norm(a)]];matches=[]
 for school in c['candidates']:
  good=[d for d in obs if any(norm(st)==norm(school['STABBR']) and norm(city)==norm(school['CITY']) for st,city in [(d['state'],d['city']),(d['principal_state'],d['principal_city'])])]
  if good:
   good.sort(key=lambda d:(str(d['report_year'] or ''),str(d['signed_date'] or '')),reverse=True);matches.append({'school':school,'disclosure':good[0]})
 out.append({**c,'location_matches':matches,'match_status':'name_city_state' if len(matches)==1 else 'ambiguous_or_unmatched'})
(r/'2026-location-matches.json').write_text(json.dumps(out,indent=2)+'\n');good=[x for x in out if len(x['location_matches'])==1];print(len(good),'name+city+state supported candidates;',len(out)-len(good),'unresolved');
for label,part in [('a',good[:30]),('b',good[30:60]),('c',good[60:90])]: (r/f'review-{label}-input.json').write_text(json.dumps(part,indent=2)+'\n')
