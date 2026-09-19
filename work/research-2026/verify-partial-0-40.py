import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-0-40.json'))
choices={'ff5c1e72224a00d2': 0, '0667298c4d614051': 0, '22d318baa932dd0f': 0, '92ea97837b064ada': 0, 'ba8aeee6eac76de7': 1, '5ab98cf17653316e': 1, '1fbadf50904cc196': 3, '4228cb17ea6c1892': 0, 'ce5c81386d9d6b69': 0, 'd5ebeb5d2d59e1b4': 0, 'cdea73eb0eae0b96': 1, 'a127050f8b5bc6b6': 1, '5cc7aae81ebb22a5': 0, '253b90282f7fa044': 0, 'ec78a0a25b0d8b39': 3, 'e4b647b42ca664c5': 0, '0d8647eaa305e688': 1, '4363ee7818038a87': 1}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-0-40.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
