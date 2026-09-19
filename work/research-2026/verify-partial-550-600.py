import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-550-600.json'))
choices={'7d4084833ff58526': 4, 'e4f7a23f31d144e6': 0, '002bad04a7ca7ff0': 0, 'fe5b2f39407d74c5': 1, '97c32f423088becb': 4, '3c6a9d205659dce7': 2, '399fb36fc1bf3d96': 1, '68870ee459174fc9': 0, 'f031a5fca16b935d': 0, '2247f4d0df2a2251': 0, '0879615371ecf099': 1, 'ad31586c79aa8bad': 1, '26c87e6951f11834': 0, '4925e15dd28957f0': 1, 'f6307dc1e449a91d': 1, 'a442cdbae9126fbc': 0, 'b54bfc0c4d453a47': 0, '003942092fa7a2b5': 1, 'a5c7059e4bbd66ab': 0}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-550-600.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
