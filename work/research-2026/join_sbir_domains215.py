import csv,json,pathlib,urllib.parse,collections
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'))
def host(s):
 if not s:return ''
 return urllib.parse.urlparse(s if '://' in s else 'https://'+s).netloc.lower().removeprefix('www.')
idx=collections.defaultdict(dict)
for a in csv.DictReader(open(r/'sbir-awards-no-abstract.csv',encoding='utf-8-sig')):
 h=host(a['Company Website']);key=(a['Company'],a['UEI']);old=idx[h].get(key)
 if not old or a['Award Year']>old['Award Year']:idx[h][key]=a
out=[]
for i,v in p.items():
 if v['review_outcome']=='confirmed' or not v.get('website'):continue
 rows=list(idx.get(host(v['website']),{}).values())
 if not rows:continue
 out.append(dict(id=i,name=v['name'],website=v['website'],description=v['description'],notes=v['notes'],records=[{k:a[k] for k in ['Company','UEI','Company Website','City','State','Address1','Award Year','Award Title']} for a in rows]))
(r/'sbir-domain-candidates215.json').write_text(json.dumps(out,indent=2)+'\n');print('candidates',len(out))
for a in out: print(a['id'],a['name'],'=>',[(x['Company'],x['UEI']) for x in a['records']])
