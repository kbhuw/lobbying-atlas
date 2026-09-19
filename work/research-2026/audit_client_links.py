"""Compare each LDA client link to the input record's exact names and aliases.
Flags need review; a flag is not by itself a finding of incorrect identity.
"""
import argparse,json,pathlib,re,sqlite3
ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('evidence',nargs='+');ap.add_argument('--output',required=True);args=ap.parse_args()
rows={v['id']:v for v in json.load(open(args.input))}
con=sqlite3.connect('work/organization-research/research.sqlite')
clients={str(i):n for i,n in con.execute('select id,name from lda_clients')}
def norm(n):return re.sub(r'[^a-z0-9]','',n.lower())
records=[]
for path in args.evidence:
 data=json.load(open(path));data=data.get('corrections',data)
 for key,v in data.items():
  if key not in rows or not isinstance(v,dict):continue
  row=rows[key];names={norm(s) for s in [row['name']]+row.get('aliases',[]) if isinstance(s,str)}
  for src in v.get('sources',[]):
   match=re.search(r'/api/v1/clients/(\d+)(?:/|\?)',src['url'])
   if not match:continue
   client=clients.get(match[1]);status='exact_name_or_alias' if client and norm(client) in names else 'needs_review'
   records.append(dict(id=key,input_name=row['name'],client_id=match[1],client_name=client,status=status,file=path,url=src['url']))
pathlib.Path(args.output).write_text(json.dumps(records,indent=2)+'\n')
flags=[v for v in records if v['status']=='needs_review']
print(json.dumps(dict(links=len(records),needs_review=flags),indent=2))
