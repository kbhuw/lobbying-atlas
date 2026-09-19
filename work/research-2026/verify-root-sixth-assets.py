import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-148-348.json'))
choices={'c4587efee38f780a':0,'b9e4f1cf5a173a6d':0,'7ccd2f618e2c7ace':4,'87dd2ebd6afbb0d4':3,'d4b164b5c1b869ae':0,'72685204f4d482d3':4,'802e92803d1e51f6':5,'bee70260414f4229':0,'be9dd504495d8248':0,'23c1b64874595cc4':1,'c356df9838f36324':1,'5f673686c8f9336b':8,'6e564087770b12c8':3,'5d28f05abc97d028':2,'6a311f93b14b8d07':1,'d84fa8efa237aa58':0,'07a3908c57a4228f':0,'a777ed96838b6593':5,'c872a79e3790faa9':5,'0e69fc1a35793c36':0,'425851f2a84e7b7f':0,'39c65f52a3f2c0f8':1,'cd5acf1baa814944':3,'7147a49b21059afe':0,'019bf2b5aefe9bcb':2,'21899ed0e8ca47b0':1,'45ac8b2227087aca':4,'416296b2947f6d50':5,'b9f0f2649dddf27c':3}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-sixth-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
