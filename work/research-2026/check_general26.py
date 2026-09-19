import pathlib,json,concurrent.futures
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
p={}
for s in 'abc':
 x=json.load(open(f'work/research-2026/general-round26-{s}-researched.json'));p.update({v['id']:v for v in x} if isinstance(x,list) else x)
p.update(json.load(open('work/research-2026/general-round26-b-corrections.json')))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for k,c in ex.map(one,[(k,v) for k,v in p.items() if v.get('website')]):print(k,c.get('http_status'),c.get('error',''),flush=True)
