import csv,json,pathlib,re,collections,urllib.parse
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'))
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def host(s):return urllib.parse.urlparse(s if '://' in s else 'https://'+s).netloc.lower().removeprefix('www.')
idx=collections.defaultdict(list)
with (r/'sbir-awards-no-abstract.csv').open(encoding='utf-8-sig') as f:
 for v in csv.DictReader(f):idx[norm(v['Company'])].append(v)
result=[]
for i,v in p.items():
 if v.get('review_outcome')=='confirmed':continue
 rows=idx.get(norm(v['name']),[])
 if not rows:continue
 groups={}
 for a in rows:
  key=(a['UEI'],a['City'],a['State'],a['Company Website'])
  if key not in groups or a['Award Year']>groups[key]['Award Year']:groups[key]=a
 result.append(dict(id=i,name=v['name'],website=v.get('website'),same_domain=any(host(a['Company Website'])==host(v.get('website','')) and host(a['Company Website']) for a in rows),records=[{k:a[k] for k in ['Company','UEI','Company Website','City','State','Address1','Award Year','Award Title']} for a in groups.values()]))
(r/'sbir-unresolved-candidates.json').write_text(json.dumps(result,indent=2)+'\n')
print('exact normalized-name candidates',len(result),'same domain',sum(bool(v['same_domain']) for v in result))
for v in result: print(json.dumps(v))
