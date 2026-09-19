import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-450-500.json'))
choices={'e4623f789e15fc59': 1, '3e7ee1ea44aa4e04': 1, '910678276ed9fa96': 6, 'ec60a1bbc1754e21': 0, 'fd37803cb9e2665f': 2, '3dc222c006f4e613': 0, 'ef677536be5c897b': 0, 'c31feb7db6f83476': 4, '77a558bdb2f380f5': 0, '400055f3854a6add': 0, 'a0f98ade9a177fbf': 2, '3d2fe6718db4e07b': 0, 'd6f3d8941151481c': 3, '3e91c46e61cc5396': 0, '12b408fa389ce8d3': 1, 'ca8fcbb57b4890ca': 0, 'fd310be229de514c': 0, 'ad5628c10de7d3b4': 1, 'efb357d9717dbc05': 2, 'ece171b692601f86': 1, '019b430191c77b6a': 5, '502a68a2fe1a3e48': 1, 'c7ea8c687c3bebc7': 0, '42f6595bb1d6c2f4': 2, 'd235e43e5c0cf827': 4}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-450-500.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
