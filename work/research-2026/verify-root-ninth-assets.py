import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-348-548.json'))
choices={'135ce651c1a5c905':6,'93a4f6e9176f3805':2,'f6324c661c453284':0,'7fd2106497e80e12':3,'a1b9abeb70e7f062':0,'e48b45bf4ab48bb5':14,'028e706216a92c7a':0,'7063bbf2fb9ab46c':0,'774e4d9eb23fd991':0,'17819ac72f2fb700':0,'19c91ed1a6a0ff55':0,'899ca6a8a411445a':2,'59144964e542ee62':1}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-ninth-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
