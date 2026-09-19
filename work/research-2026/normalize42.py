import json,pathlib,gzip,re
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round42-input.json'));e={};p={}
for part in ['first25','second25','third25','root']:e.update(json.load(open(r/f'round42-{part}-evidence.json')))
for part in ['audit','first-audit','root']:
 f=r/f'round42-{part}-corrections.json'
 if f.exists():
  for k,v in json.load(open(f)).items():
   if k not in e:continue
   old=e[k];src=old['sources'];old.update(v);old['sources']=v.get('sources',src)
exec((r/'filing_evidence.py').read_text());s=(r/'research30c_root.py').read_text();helper=s[s.index('def add('):s.index("add(0,'Carbon")].replace("filing=json.load(gzip.open('lobbying-map/public/data/reports/'+row['id'][:2]+'.json.gz','rt'))[row['id']][0]","filing,filing_member=latest_filing(row)");exec(helper)
for i,row in enumerate(rows):
 v=e[row['id']];own='Subsidiary' if i==56 else v['ownership'];out=v.get('review_outcome','partial');notes=v.get('notes','')
 if own not in ['Government body','Nonprofit / tax-exempt','Public company','Subsidiary','Private company','Not applicable','Unknown']:notes+=' '+own;own='Unknown'
 if own=='Unknown' and out=='confirmed':out='partial'
 name=re.sub(r'\b(For|Of|And|TO|ON|IN|BY|The)\b',lambda m:m[0].lower(),v['name'])
 names={3:'CRRC MA Corporation',21:'CSRA Alliance for Fort Gordon',26:'CTIA',27:'CTIA — The Wireless Association',35:'CUBRC',40:'Cultural Care Au Pair',46:'TruStage (formerly CUNA Mutual Group)',51:'Curie Bio Operations, LLC',59:'Curtiss-Wright',69:'City Water, Light and Power (CWLP)'}
 name=names.get(i,name)
 src=[(s['url'],s['claim']) for s in v.get('sources',[]) if s.get('url') not in ['https://lda.gov/','https://lda.gov/api/v1/clients/']]
 desc=v['description']
 if i==69:desc='Municipal electric and water utility serving Springfield, Illinois.'
 if out=='unresolved':
  prof=row.get('profile') or {}
  if not desc and prof.get('description'):desc='Lobbying client reporting: '+prof['description'].strip().rstrip('.')+'.'
  src += [(s['url'],s['claim']) for s in prof.get('sources',[])]
 add(i,name,desc,v.get('website',''),kind=v.get('kind','Organization') if v.get('kind') not in ['Private company','Public company','Subsidiary','Government body','Nonprofit / tax-exempt'] else {0:'Maritime services company',1:'Communications infrastructure company',7:'Cruise industry trade association',10:'Capital markets platform',11:'Capital markets platform',14:'Materials and semiconductor company',22:'Public university',23:'Rail transportation company',24:'Freight railroad',33:'Defense and transportation technology company',45:'Power systems manufacturer',51:'Biotechnology investment firm',55:'Radiopharmaceutical company',59:'Engineered products manufacturer',66:'Health-care company',67:'Health-care company'}.get(i,'Organization'),own=own,sources=src,notes=notes,outcome=out,featured=i in [20,21,22,25,26,27,29,30,33,34,35,37,42,42,50,56,60,67,69,70,71,73,78,82,84,90,95,98,99])
(r/'general-round42-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
