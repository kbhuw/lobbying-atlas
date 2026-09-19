import pathlib,json,concurrent.futures
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
p={}
for x in 'ac':
 d=json.load(open(f'work/research-2026/general-round25-{x}-researched.json'));p.update({v['id']:v for v in d} if isinstance(d,list) else d)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for k,c in ex.map(one,p.items()):print(k,c.get('http_status'),c.get('error',''),flush=True)
