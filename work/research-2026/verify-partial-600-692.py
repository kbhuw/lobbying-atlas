import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-600-692.json'))
choices={'b999d504e72fb98a': 4, 'f235db9087dd27ca': 0, 'c52bed9cfdbd36a0': 1, '985c2ff6975a8a24': 2, '8805d62b610109af': 0, '8bbf35539bc61e7a': 0, 'c50c31d0eef37d94': 3, '74b8c54ac0f3a727': 2, 'edbbe4fa01fd34d4': 0, '66b6a95439952975': 0, '1cf176054341a40d': 0, '3373f5307e82e032': 1, 'c350503e1cbceacf': 0, '798ca157270f93d1': 1, '4c8cca02b17bdee5': 3, 'db4e9239cc89ebb7': 1, 'd1977ff07697c861': 1, '228578699ea93c03': 1, 'b34561b6c60f6222': 0, '98eca5b98971db7b': 1, 'c7180535ca7a145d': 2, '021ce66ab20a39aa': 1, 'fd8715256788e35b': 0, '4c50b15244f658c7': 3}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-600-692.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
