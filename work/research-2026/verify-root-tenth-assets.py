import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-548-886.json'))
choices={'2ecd78a7841d116e':1,'397624fd60197f08':1,'c987068dfd8fb57a':0,'3522d2796870bb08':0,'e7aa0e40ad589ff1':0,'4916a92ee1609b14':0,'f587ed51d5074b50':3,'76f9b07725964d51':0,'cadff9ac31140b5f':0,'45eceeab9211f7d9':0,'e1401b2e2a663579':4,'07596c5273d34e57':0,'9acf87c278dc3cac':2,'54e8d4d722e6d224':2,'83dc33f5e13d0c0f':0,'bd12b9297e45bf5b':0,'363a387cb178a0b5':0,'98e184059cb5720b':0,'fcc3ca78c6ac4bdc':0,'cbd06433d2cd9577':0,'4b74324a3be06704':1,'886cbd00331e602e':3,'f8530e7867b482b8':0,'4ce8ee5e6fa71f87':2,'5bf09013e1464437':2,'b9be1a5aac89ee02':0,'bb952ee4c77995eb':1,'38b48930a778e213':0,'8e94265a1298e8d8':2}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-tenth-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
