import pathlib,json,concurrent.futures,urllib.parse
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
p={}
for x in 'abc':
 for k,v in json.load(open(f'work/research-2026/general-round24-{x}-rootchecked.json')).items():
  f=pathlib.Path(f'work/research-2026/website-cache/{k}.json');c=json.load(open(f)) if f.exists() else {}
  if v.get('website') and v['website']!=c.get('requested_url'):p[k]=v
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for k,c in ex.map(one,p.items()):print(k,c.get('http_status'),c.get('error',''),flush=True)
