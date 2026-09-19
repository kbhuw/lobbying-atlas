import json,pathlib,requests,urllib.parse,concurrent.futures
r=pathlib.Path('work/research-2026');sites={x['id']:x for x in json.load(open(r/'sbir207-sites.json'))}
sel={'0d1fb6c17635c95e':0,'3566ed2d998051c2':0,'3d5a6f21852268da':0,'3ea7aa9a67e4d794':0,'1b54d97aaf105e4c':0,'f2d2fb3e13c96374':2,'e548982f28dd6eee':2,'ca7a20f9bec03de5':0,'d53d2822441c500d':0,'f36af1616e9dc706':0,'cfb4ff0d308bfe5f':0,'1dae43f171bc4370':0,'4f252e8cc8b0c07c':0}
def run(z):
 i,n=z;s=sites[i];u=urllib.parse.urljoin(s['final_url'],s['images'][n]['src']);f=r/f'featured211-{i}.image'
 try:
  a=requests.get(u,timeout=12);a.raise_for_status();f.write_bytes(a.content);return dict(id=i,name=s['name'],url=u,source=s['final_url'],file=str(f),bytes=len(a.content))
 except Exception as e:return dict(id=i,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:a=list(ex.map(run,sel.items()))
(r/'featured211-logo-candidates.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a))
