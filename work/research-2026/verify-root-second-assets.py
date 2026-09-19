import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-24-48.json'))
choices={'180766d51acc6068':1,'19e0b4250859faf5':0,'1a44e9232bd335f9':0,'52ce22442839bbb7':4,'d1a4beace327f779':0,'7a44496e89b04a7c':1,'9ff1cb5fec61b414':1,'ffa8333c232eab46':1,'ff8e623cbc08af14':0,'ff1199b113e1bb2f':1,'fecd36ea0e74902f':2,'fdb470b0f9277bc2':2}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-second-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
