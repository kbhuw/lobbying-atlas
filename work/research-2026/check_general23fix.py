import pathlib,json,concurrent.futures
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
p=json.load(open('work/research-2026/general-round23-root-draft.json'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for k,c in ex.map(one,[(k,p[k]) for k in ['14ee16d0ae8f6222','43bb1d455acc8edb']]):print(k,c.get('http_status'),c.get('error',''),flush=True)
