import pathlib
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
profiles=json.load(open(root/'general-round19-root-draft.json'))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for result in pool.map(one,[(k,v) for k,v in profiles.items() if v.get('website')]):
  print(result,flush=True)
