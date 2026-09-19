import urllib.request,json,pathlib,concurrent.futures,time,zipfile,hashlib
import os
project=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(os.environ.get('LOBBYING_DATA_DIR',str(project/'work'/'data')))
root.mkdir(parents=True,exist_ok=True)
(root/'raw').mkdir(exist_ok=True)
manifest=json.loads((root/'house-manifest.json').read_text())
def get(item):
 p=root/'raw'/item['file'];u='https://disclosurespreview.house.gov/data/LD/'+item['file']
 for attempt in range(4):
  try:
   if not p.exists():
    temp=p.with_suffix('.part')
    with urllib.request.urlopen(u,timeout=120) as r, temp.open('wb') as out:
     while b:=r.read(1024*1024):out.write(b)
    temp.replace(p)
   with zipfile.ZipFile(p) as z:
    count=len(z.namelist());bad=z.testzip()
   if bad: raise ValueError('CRC failed '+bad)
   d={**item,'url':u,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'members':count,'retrieved_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
   (root/'raw'/(p.name+'.meta.json')).write_text(json.dumps(d,indent=2))
   print(p.name,count,p.stat().st_size,flush=True);return d
  except Exception as e:
   print('RETRY',p.name,str(e),flush=True);time.sleep(2**attempt)
 return {**item,'error':'download failed'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: results=list(ex.map(get,manifest))
(root/'download-ledger.json').write_text(json.dumps(results,indent=2))
print('DONE',len(results),'failed',sum('error' in x for x in results),flush=True)
