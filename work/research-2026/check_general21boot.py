import pathlib,json,concurrent.futures
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
p=json.load(open('work/research-2026/general-round21-c-rootchecked.json'))
p={k:v for k,v in p.items() if k=='4fc596bfffd5ae94'}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for k,c in ex.map(one,p.items()):print(k,c.get('http_status'),c.get('error',''),flush=True)
