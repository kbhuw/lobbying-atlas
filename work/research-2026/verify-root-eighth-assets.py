import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-348-548.json'))
choices={'eeb3e08e271a6586':1,'db2964a861bb1d4e':3,'f1d0902d9ff857ea':1,'36289e3ebe24c819':1,'2dbf663b74ddfafc':0,'ce8d1ced0ced2c31':2,'13c647380266649d':4,'7e67cbb44b42b586':0,'f748ebe505068e76':5,'db71aaee0beef2cd':5,'5735e769949c2024':5,'79b600e22f4594c8':1,'3fe7400c15798df5':6,'2bc1a65abb66c73e':0,'23a17a9e32c5b6f3':1,'3e1db3b04b508439':1,'06e2c63451e795c6':2,'13637e2874d31600':1,'2e7b60e176a810ff':1,'33394fb0c7195f44':1,'cee778e72cd6c14a':1,'ee29daf5ec359c37':0,'5e10c8f00c187076':0,'94e6f66957254c21':0,'234a9e7220eb860f':1,'1181a686653eea04':1,'5bde6487812a6d70':0,'3943840e5e003fdb':0,'4c0d94adef39ec48':0,'beeeae9f541e6a0c':4,'c8f90d0a0998593d':1}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-eighth-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
