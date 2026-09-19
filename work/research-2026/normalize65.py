import json,pathlib,gzip,re,html
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round65-input.json'));e={};p={}
for part,start,end in [('first33',0,33),('second33',33,66),('third34',66,100)]:
 data=json.load(open(r/f'round65-{part}-evidence.json'))
 expected={row['id'] for row in rows[start:end]}
 assert set(data)==expected, f'{part}: missing={expected-set(data)}, extra={set(data)-expected}'
 e.update(data)
for part in ['first33-audit','second33-audit','third34-audit','first33-extra','second33-extra','third34-extra','second33-final','logo-root','root']:
 f=r/f'round65-{part}-corrections.json'
 if f.exists():
  for k,v in json.load(open(f)).items():
   assert k in e and k in {row["id"] for row in rows}, f"Unknown correction ID {k} in {f}"
   old=e[k];src=old['sources'];old.update(v);old['sources']=v.get('sources',src)
exec((r/'filing_evidence.py').read_text());s=(r/'research30c_root.py').read_text();helper=s[s.index('def add('):s.index("add(0,'Carbon")].replace("filing=json.load(gzip.open('lobbying-map/public/data/reports/'+row['id'][:2]+'.json.gz','rt'))[row['id']][0]","filing,filing_member=latest_filing(row)");exec(helper)
for i,row in enumerate(rows):
 v=e[row['id']];own=v['ownership'];out=v.get('review_outcome','partial');notes=v.get('notes','')
 if own not in ['Government body','Nonprofit / tax-exempt','Public company','Subsidiary','Private company','Not applicable','Unknown']:notes+=' '+own;own='Unknown'
 if own=='Unknown' and out=='confirmed':out='partial'
 name=re.sub(r'\b(For|Of|And|TO|ON|IN|BY|The)\b',lambda m:m[0].lower(),html.unescape(v['name']))
 src=[(s['url'],s['claim']) for s in v.get('sources',[]) if s.get('url') not in ['https://lda.gov/','https://lda.gov/api/v1/clients/']]
 desc=v['description']
 if out=='unresolved':
  prof=row.get('profile') or {}
  if not desc and prof.get('description'):desc='Lobbying client reporting: '+prof['description'].strip().rstrip('.')+'.'
  src += [(s['url'],s['claim']) for s in prof.get('sources',[])]
 add(i,name,desc,v.get('website') or '',kind=('Organization' if v.get('kind') in ['Private company','Public company','Nonprofit / tax-exempt'] else v.get('kind','Organization')),own=own,sources=src,notes=notes,outcome=out,featured=i in [0,1,2,3,4,5,6,7,8,9,10,11,12,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,34,36,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,56,58,59,60,61,62,63,64,65,66,67,69,71,72,73,74,75,76,79,80,82,83,84,85,87,88,89,90,91,92,93,94,95,97,98,99])
(r/'general-round65-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
