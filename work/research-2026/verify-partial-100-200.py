import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-100-200.json'))
choices={'34c0cd4214fad667': 0, '6df713ac1b3ad73e': 1, '7144764393b052a4': 0, 'd3e5871b006477e0': 1, '016d6fa8d7a0423d': 1, 'd3ed27628898125e': 1, '0257c6d2080bf7c4': 1, 'd8a1dd0d78d8fb72': 0, '26a5b178a511e44b': 1, '82425b4b6da0b383': 0, 'f95b85b77efbf74d': 0, '369c6dc842ba93a7': 1, '68d880b44027b0dd': 0, 'f19c35f1531a135e': 1, '8725c4cb16c748cf': 1, '5306b5451d64803f': 0, '0d89458e1a9d3a87': 1, 'd52260625be7e51d': 0, '2add3941d22f2b59': 0, '724774049838dd12': 0, '6563e9be00be19b9': 0, '24aaced9578ba4ea': 1, '0cc5c2585e979c54': 1, 'df3881450000b7f5': 0, 'ebb83085e5492732': 0, '62e6ede5fbff8a82': 0}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-100-200.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
