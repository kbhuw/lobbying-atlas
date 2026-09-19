import pathlib,json,concurrent.futures
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
p=json.load(open('work/research-2026/general-round26-root-draft.json'))
keys=[]
for k,v in p.items():
 c=json.load(open(cache/(k+'.json'))) if (cache/(k+'.json')).exists() else {}
 if v.get('website') and v['website']!=c.get('requested_url'):keys.append(k)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for k,c in ex.map(one,[(k,p[k]) for k in keys]):print(k,c.get('http_status'),c.get('error',''),flush=True)
