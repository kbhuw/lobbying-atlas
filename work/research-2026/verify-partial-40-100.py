import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-40-100.json'))
choices={'95b66cf670ca6ee0': 1, 'b17ace791d3d35c0': 0, '2dfd6e8ba2641c14': 0, '00cdbc0057440df6': 0, '97e192da8f72be0d': 0, '51d95d9f8f9e0836': 1, 'de6db64ef6032545': 4, '4a0f71289294ada4': 0, 'c113becf45b4e5c2': 2, '6786b72533286e62': 3, 'fb6ef2a94940196d': 1, 'b1c76d600f96d3ab': 3, '2f736509baa1bb75': 1, 'daca47ffc0a07777': 0, '54dd66aee7a76a01': 2, 'f935cfb5e2d6bc70': 1, '89398278dd1302d6': 0}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-40-100.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
