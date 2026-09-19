import pathlib,json,concurrent.futures
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
p=json.load(open('work/research-2026/general-round22-b-rootchecked.json'))
p={k:v for k,v in p.items() if k in ['d34e45116ab02360', '70ec4d13e03f7d73', '59c45f5121f58c23', '2035ac31ea866c71', 'f822ff58e856c90f', '901129de98c259c8', '9b9088cecabbfc4d', 'deb315a0993a2e12', '34afa5781ac8ef99', '600b411e2b4f7afa', '5ee878439e8786e1']}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for k,c in ex.map(one,p.items()):print(k,c.get('http_status'),c.get('error',''),flush=True)
