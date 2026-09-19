import pathlib,json,concurrent.futures
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
p=json.load(open('work/research-2026/general-round22-c-rootchecked.json'))
p={k:v for k,v in p.items() if k in ['07c8d88950e272e1', 'f6483ebb944082fe', '623c68e6095752da', 'e209397e8642b3fd']}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for k,c in ex.map(one,p.items()):print(k,c.get('http_status'),c.get('error',''),flush=True)
