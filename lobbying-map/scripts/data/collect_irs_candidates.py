"""Download official IRS extracts and retain exact-name candidates, not confirmed identities."""
import csv,concurrent.futures,datetime,gzip,json,pathlib,urllib.request,shutil,collections
from organization_names import normalized
root=pathlib.Path(__file__).resolve().parents[3]/'work/organization-research'
manifest=json.loads((root/'irs-manifest.json').read_text())
raw=root/'irs';raw.mkdir(exist_ok=True)
cs=json.load(gzip.open(root.parents[1]/'lobbying-map/public/data/directory-v2.json.gz'))['companies']
names=collections.defaultdict(set)
for c in cs:
 for a in c['aliases']:names[normalized(a)].add(c['id'])
def download(u):
 p=raw/u.rsplit('/',1)[-1]
 if not p.exists():
  temp=p.with_suffix('.tmp')
  with urllib.request.urlopen(u,timeout=120) as r,temp.open('wb') as f:shutil.copyfileobj(r,f)
  temp.replace(p)
 return p
matches=[];count=0
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for p in ex.map(download,manifest['urls']):
  with p.open(newline='',encoding='utf-8-sig') as f:
   for r in csv.DictReader(f):
    count+=1
    for id in names.get(normalized(r['NAME']),[]):
     matches.append({'company_id':id,'irs':r,'source_url':'https://www.irs.gov/pub/irs-soi/'+p.name,'source_date':manifest['data_date']})
  print(p.name,count,'rows',len(matches),'candidates',flush=True)
(root/'irs-candidates.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2))
(root/'irs-progress.json').write_text(json.dumps({'rows':count,'candidate_records':len(matches),'candidate_organizations':len(set(r['company_id'] for r in matches)),'complete':True,'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
