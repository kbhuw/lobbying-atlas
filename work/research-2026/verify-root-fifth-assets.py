import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-148-348.json'))
choices={'c4793648c06a3816':1,'f3ae1cac3cdcdaf9':0,'7156aee85c612bea':1,'b59e93a6d7729a19':3,'ad626c346310d31b':0,'b713263b21624f57':0,'c0d8f8fa128202b6':3,'f82d27df865d6541':1,'8b43dd5a20cb963a':1,'6d7698ed7fa24e71':0,'8758b1265efc121d':2,'d42fbf2839b74083':1,'f3e31d5485ab3a3e':2,'baca81783ef0473c':0,'b73a87f5a917d821':4,'cec958ca702755fe':3,'84aa080f0cc3fc5e':0,'6fec2fb0e7b981cb':0,'6d4599a3a5c9e641':2,'76da3bb8a2915dbd':1,'f0c513f6d68f54ae':4,'81f0e054f326bfe4':0,'c0447a46c2f30a4b':0,'ba5f8c450f583772':2,'a639e211fd1aa47d':1,'c4edd9f12124cf83':1,'f984f2864239e499':0,'7f02b86304b761e8':0,'69a720d98bb91df4':1,'f1d24821f7436e74':0,'e2bf82d1ed965180':3,'e27c857a126c7fb4':2,'b9c87e62aa1edae1':3,'d2c1cfc66f285381':1,'b43f3f70938b564d':0,'a7e214dbdfc04e7d':1,'85a42cd8fcea3d27':0,'69f88a4e784dc729':1,'aaa81a2ec8142190':3,'7a0d4a3bbce587a4':0,'b7781f6026a0e8f4':1,'a30679cc5e08bfc2':2,'f2eba82c0a25e848':1,'68b5ff36db323e80':3,'e97ad8e4ffb70d9c':2,'eb9584922d4e7c33':1,'816e85480a9b6ea8':1,'c4d466569bb62d36':0,'944096f8fb257b7a':0,'7bb579b315f2f130':5,'ab0af2834a548050':1,'6916621417e5cc03':2,'9d6b171bf7aec95e':3,'b59de5d48a169bb4':0,'8c1bc5b9110674bd':6,'ab79082827d5e29e':3}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-fifth-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
