import json,pathlib,gzip,re
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round40-input.json'));e={};p={}
for part in ['first25','second25','third25','root']:e.update(json.load(open(r/f'round40-{part}-evidence.json')))
for part in ['first25','second25','third25','sec','root']:
 f=r/f'round40-{part}-corrections.json'
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
 if 2 <= i <= 22:
  name=re.split(r' OBO ',v['name'],flags=re.I)[-1]+' (via Cornerstone Government Affairs)'
  desc=desc.replace('; Cornerstone is the filing registrant','')
  notes=re.sub(r'Cornerstone is the (?:filing )?registrant', 'Cornerstone is named as the representative in the client label',notes)
  notes+=' The original client label names Cornerstone on behalf of this beneficiary; the actual registered lobbying firm is identified in the linked disclosure.'
  v['kind']=v.get('kind','Organization').split(' (beneficiary')[0]
 name=name.replace('Id.me','ID.me').replace('Copt','COPT').replace('Hdr,','HDR,').replace('Standardaero','StandardAero').replace('Corrohealth','CorroHealth').replace('Costquest','CostQuest').replace('TAX Advisors','Tax Advisors').replace('Of Cdc','of CDC').replace('For ','for ').replace('On ','on ').replace(' LAB',' Lab')
 name=name.replace(' ON Behalf of ',' on behalf of ').replace(' OBO ',' on behalf of ')
 desc=desc.replace('Corrigan & Ussery is the registrant','Corrigan & Ussery is the named representative')
 if out=='unresolved':
  prof=row.get('profile') or {}
  if not desc and prof.get('description'):desc='Lobbying client reporting: '+prof['description'].strip().rstrip('.')+'.'
  src += [(s['url'],s['claim']) for s in prof.get('sources',[])]
 add(i,name,desc,v.get('website',''),kind=v.get('kind','Organization'),own=own,sources=src,notes=notes,outcome=out,featured=i in [3,4,5,7,9,11,12,13,14,15,17,19,20,21,25,35,37,38,39,42,43,49,52,53,77])
(r/'general-round40-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
