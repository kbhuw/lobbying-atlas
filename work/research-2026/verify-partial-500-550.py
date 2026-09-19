import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-500-550.json'))
choices={'784a42fd373f48a3': 1, 'aa625f3b0566f854': 0, '3bcd0db6a36051fa': 0, 'c66f9e5c96825407': 0, '84f8ddd73b761fa3': 1, 'a5e3d4e9a054a3fb': 3, 'a6e60717613addfa': 0, '4f15666ddc18c7bc': 1, 'e10edd5db440e676': 1, '4e4ff24dc6cf3cbf': 1, 'fd6ef8d7d2109914': 1, 'c9e26cc2734af705': 0, 'fcbaf17702baf850': 1, 'af152a70d915b2bc': 1}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-500-550.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
