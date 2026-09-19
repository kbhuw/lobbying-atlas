import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-148-348.json'))
choices={'0b57e49fed30b87d':0,'2bc42350f530c32f':4,'51acd9dcda8ce8a9':1,'ce084197b8a715be':4,'b63a124b0b9b71b5':0,'85b35c32e6482f7e':5,'e92dcc6d2df7b488':5,'c08e585dab8ea281':0,'9cebae737c0021b1':0,'503039a011cac7b2':0,'b19a8084b7f175f0':4,'9a88cab8817466d4':0,'e7be86a971cdd62c':0,'a4e1e5cfd6f75254':2,'b7a9a1990166d1e3':1,'d4c5f8019f81a021':3,'e8e4e4998090cf59':0,'aa97b1c00df37f8b':0,'7989bbe9535b992d':0,'6d32d08907267ea6':3,'ae72b301716a264c':13,'6e99324f91fd1f0e':1,'acf313a44ccf1b98':0,'e61b531913d7a136':0,'f233bc0b9e1dcb5e':0,'f69cc96447b94533':1,'c327d6eee9041b9f':2,'adc9c3c7e4567c84':0,'6a617585f8411e11':0,'c35934a730940611':0,'76b125eb4f32729a':0,'d694aa8b9c07cb95':2,'b02b8a877a3e8c53':1,'c2bce04ddd9938d0':3,'f738cdbe95c0fa64':1,'e754135d29d815fb':0,'8640f20b12f7cd62':1,'afc0147b6f49c6e7':1,'e1df3af39fcf0115':3,'dd9c606435662eaf':2,'dc19f8ef765e1c83':2,'727929319f0e38d0':8,'c4a18b4d36a20446':0,'cb7cf65536feffc2':7,'b772e9d0799f6d4d':7}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-fourth-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
