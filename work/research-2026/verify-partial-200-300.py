import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'partial-verified-logo-200-300.json'))
choices={'59c000eea998d441': 1, '8290aaeafc36c006': 0, 'b243accec63d6351': 0, '96b35833b28025e0': 1, '056598b5a14a40e9': 1, '1e4afb95aa5b3276': 1, '3537cbd34c90f0f5': 0, '5414eeec922da7cc': 0, '06bd116f564ed395': 0, '8863c3070bafba13': 1, '1db117de523ce9c9': 1, 'c68f1774f1d3c7d9': 1, 'a7edd2e919ff3a68': 1, '4ee0e09f5d1ad56b': 0, 'ed3eb2cace8b5822': 1, 'b6601a9e8b4ad574': 0, '598cc50145ec629a': 0, '247afc1eb686bc6d': 0, '9d36ac919bf7d700': 1, '45452d67de9aff0b': 0, '994f06cc34ab46bb': 1, '4bada4bf6e77a230': 1, '860c02ea9b5a24a6': 1, 'df17568ead47d9c5': 1, '7e9c2640a19b61ce': 0, 'fb3147293adf76e5': 0, '2decfae4f9e32702': 1, '12769b1efbdbce42': 1, '9b14238d4d491586': 1, '313d11d1f7bb3b3b': 1, '6ed7603a43b4253b': 1, '59c29c43b7763337': 0, 'bb5fc60e1d467ee9': 1, '5321a6ba6e6d33ad': 1, '5ee43e277b4a23d6': 1, 'ff9508e3adcb1cd9': 1}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'partial-verified-assets-200-300.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
