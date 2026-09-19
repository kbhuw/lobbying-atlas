import json,pathlib,gzip,re,html
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round57-input.json'));e={};p={}
for part in ['first33','second33','third34']:e.update(json.load(open(r/f'round57-{part}-evidence.json')))
for part in ['first33','second33','third34','audit','extra','ownership-extra','second-extra','root']:
 f=r/f'round57-{part}-corrections.json'
 if f.exists():
  for k,v in json.load(open(f)).items():
   if k not in e or k not in {row["id"] for row in rows}:continue
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
 add(i,name,desc,v.get('website',''),kind=('Organization' if v.get('kind') in ['Private company','Public company','Nonprofit / tax-exempt'] else v.get('kind','Organization')),own=own,sources=src,notes=notes,outcome=out,featured=i in [1,13,18,19,23,25,27,28,29,38,39,41,42,43,46,48,54,55,56,58,61,62,63,68,69,70,73,74,78,79,82,83,84,85,86,91,95,98,99])
(r/'general-round57-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
