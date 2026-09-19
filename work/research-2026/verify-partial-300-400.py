import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-300-400.json'))
choices={'ff84d473f08143ae': 1, 'e3599edb4c567bf5': 0, '468f566305af4946': 0, '6bc081c172b76fe3': 0, '8fb509d4766629e0': 1, '98fc4e4bcdb8a4c3': 1, '9a5161bec8f862b9': 1, 'c67d855213fa4905': 1, '11ccf0d6be17d238': 1, 'dc67482939c62489': 0, '0a9de684dd130284': 0, 'be6428bc4c37755e': 1, 'a3194bcb4082652c': 1, 'd1fc1273754145ba': 0, 'd982b760d11193f3': 1, '031d1fcbda617d31': 0, 'ff5abfaba0ca9e3d': 1, '8e9998ccb7642cdf': 0, '40dde5e44eb0b2a4': 0, '86688a345037dca4': 1, '6f08e047b260533e': 1, 'fb0495809a465db3': 1, '269f917d11349107': 1, 'aff8cac099014827': 1, '3bde04761f9852d9': 1, '67337d306106a9ca': 1, '064671aec2175479': 0, '18e6fb306d0386ce': 0, '6635f49c07412ea0': 1, '70a8e6f71eb951ef': 0, '2d25dec28aa3a0a7': 0, 'a0627b03288bd63e': 0, '6dbc442cc5ff8c8e': 0, '18eae43a97206f0b': 1, 'cd7177230cbac0b3': 0, '23d7329122ab1894': 1, 'be5be1eebf7e96ea': 0, 'ba3e9278afc96e21': 0, 'b146b173457ed983': 0, 'b742cea0a7c96428': 1, '1d7f94c011e6b66b': 1, 'f76026dbba929ea1': 1, 'b413dcbc1f8461bb': 1, '396fd20b0b732f72': 0, '7f014677f9b6666f': 0}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-300-400.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
