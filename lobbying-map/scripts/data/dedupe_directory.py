import json,gzip,pathlib,collections,sys
from organization_names import normalized,parts,display
from cleaning import period
root=pathlib.Path(__file__).resolve().parents[2];public=root/'public/data'
d=json.loads(gzip.decompress((public/'index.json.gz').read_bytes()))
families=collections.defaultdict(set)
for c in d['companies']:
 b,f=parts(c['name'])
 if f:families[b].add(f)
groups={};member_group={}
for c in d['companies']:
 b,f=parts(c['name']);k=b if len(families[b])<=1 else normalized(c['name'])
 g=groups.setdefault(k,{'id':c['id'],'name':display(b if len(families[b])<=1 else c['name']),'aliases':[],'members':[],'years':{},'issues':[]})
 g['aliases'].append(c['name']);g['members'].append(c['id']);g['issues']+=c['issues'];member_group[c['id']]=k
latest={};total=0
for p in (public/'reports').glob('*.json.gz'):
 for cid,rs in json.loads(gzip.decompress(p.read_bytes())).items():
  k=member_group[cid]
  for r in rs:
   total+=1;t=period(r['kind'])
   if not t:continue
   slot=(k,normalized(r['registrant']),r['year'],t);stamp=r['posted_iso'];active='No Activity' not in r['kind'];prev=latest.get(slot)
   if not prev or stamp>prev[0]:latest[slot]=(stamp,active)
   elif stamp==prev[0]:latest[slot]=(stamp,active and prev[1])
for (k,firm,y,t),(stamp,active) in latest.items():
 if active:groups[k]['years'][str(y)]=groups[k]['years'].get(str(y),0)+1
for g in groups.values():g['issues']=sorted(set(g['issues']));g['aliases'].sort();g['members'].sort()
companies=sorted((g for g in groups.values() if g['years']),key=lambda g:g['name'].upper())
result={**{k:v for k,v in d.items() if k!='companies'},'companies':companies,'original_names':len(d['companies']),'merged_name_variants':sum(len(g['members'])-1 for g in groups.values()),'cleanup_version':2}
(public/'directory-v2.json.gz').write_bytes(gzip.compress(json.dumps(result,separators=(',',':')).encode(),mtime=0))
assert sum(len(g['members']) for g in groups.values())==len(d['companies'])
a=[g for g in companies if g['name']=='Anthropic'];assert len(a)==1 and len(a[0]['members'])==3
assert len({c['id'] for c in companies})==len(companies)
print(json.dumps({'organizations':len(companies),'merged_variants':result['merged_name_variants'],'preserved_report_records':total,'anthropic':a[0]},indent=2))
