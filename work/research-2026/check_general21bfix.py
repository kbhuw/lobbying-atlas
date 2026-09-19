import pathlib,json,concurrent.futures
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
p=json.load(open('work/research-2026/general-round21-b-rootchecked.json'))
p={k:v for k,v in p.items() if k in ['8426ae7a200ad9f4','a426468802ca43b0','b73846303392f50f','a3ac48c6ef313207']}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for k,c in ex.map(one,p.items()):print(k,c.get('http_status'),c.get('error',''),flush=True)
