import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-548-886.json'))
choices={'87525684a0c01afe':1,'7377c3fe4977960b':0,'f5ce74bf8ce3331e':0,'34a4f4e5a2373f7b':0,'906466384a766f30':0,'db7e59467b007737':3,'2f8f794a731c47b5':3,'edcd3ea3e352423c':0,'5b4a225038cf9d48':1,'a2f20b6c14e765e6':0,'ecf86285086af240':0,'d9d1350c5f409f58':0,'2e31758807340a70':2,'45fc51fdd67d0fec':4,'6bbdab9757d91543':0,'b21091eb430b8943':0,'b13456b55bfe2c41':0,'05b1abd46f76e941':0,'9256cabf03afe3c5':0,'039e079ffe59a271':1}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-thirteenth-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
