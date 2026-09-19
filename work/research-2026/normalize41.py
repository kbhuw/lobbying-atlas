import json,pathlib,gzip,re
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round41-input.json'));e={};p={}
for part in ['first25','second25','third25','root']:e.update(json.load(open(r/f'round41-{part}-evidence.json')))
for part in ['first25','second25','third25','owner','root-special','second-extra','final-identities','root']:
 f=r/f'round41-{part}-corrections.json'
 if f.exists():
  for k,v in json.load(open(f)).items():
   old=e[k];src=old['sources'];old.update(v);old['sources']=v.get('sources',src)
exec((r/'filing_evidence.py').read_text());s=(r/'research30c_root.py').read_text();helper=s[s.index('def add('):s.index("add(0,'Carbon")].replace("filing=json.load(gzip.open('lobbying-map/public/data/reports/'+row['id'][:2]+'.json.gz','rt'))[row['id']][0]","filing,filing_member=latest_filing(row)");exec(helper)
for i,row in enumerate(rows):
 v=e[row['id']];own=v['ownership'];out=v.get('review_outcome','partial');notes=v.get('notes','')
 if own not in ['Government body','Nonprofit / tax-exempt','Public company','Subsidiary','Private company','Not applicable','Unknown']:notes+=' '+own;own='Unknown'
 if own=='Unknown' and out=='confirmed':out='partial'
 name=re.sub(r'\b(For|Of|And|TO|ON|IN|BY|The)\b',lambda m:m[0].lower(),v['name'])
 src=[(s['url'],s['claim']) for s in v.get('sources',[]) if s.get('url') not in ['https://lda.gov/','https://lda.gov/api/v1/clients/']]
 desc=v['description']
 if out=='unresolved':
  prof=row.get('profile') or {}
  if not desc and prof.get('description'):desc='Lobbying client reporting: '+prof['description'].strip().rstrip('.')+'.'
  src += [(s['url'],s['claim']) for s in prof.get('sources',[])]
 add(i,name,desc,v.get('website',''),kind=v.get('kind','Organization'),own=own,sources=src,notes=notes,outcome=out,featured=i in [20,21,22,25,26,27,29,30,33,34,35,37,41,42,50,56,60,67,69,70,71,73,78,82,84,90,95,98,99])
(r/'general-round41-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
