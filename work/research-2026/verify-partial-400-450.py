import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-400-450.json'))
choices={'d3ae0fd354238e11': 1, 'b316b860098202cf': 0, '50340466fd12f0ce': 1, '740ac444837f8d12': 0, 'a2ac2b7d180173fe': 0, 'f7eb7e6e5d5360a9': 1, '832777f0c65c9c0f': 1, '6086d3b7bdbd5921': 7, '1f9f2acaa8cb8cb9': 1, '49c82af514dea501': 0, '10a60592ea0433c8': 2, 'cffc737a77cc3d12': 0, '6319152cb61c3e17': 3, '0ff6cfe7173c32dd': 3, 'd2797867f410ceac': 0, '33b7dbc4cc5b749a': 1}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-400-450.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
