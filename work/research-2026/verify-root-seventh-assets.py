import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-348-548.json'))
choices={'9d02410fef54e8c5':1,'1b628e1e577774c9':2,'fe25ea1ec3aab132':7,'9a38a11860ca733f':0,'348e062a4bf00048':1,'b11cf14f9c7aee29':2,'441c3314dc3f38c2':0,'36e2bb4082f67e1c':3,'6f28334cef3e6d00':2,'8f2959b3985139dc':1,'1269e27fef4598f4':1,'d5959c094a48a86a':1,'646c4536a63da388':2,'6441a71b42802129':0,'77c0990d64bef98d':2,'609d08c4e33e8ec6':2,'9d3d95a39f0d95d2':0,'6d3acfd6167001f8':0}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-seventh-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
