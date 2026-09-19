import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-548-886.json'))
choices={'4b9738783b12f68a':0,'1c82d0a91b767134':0,'cefe24500457d3dc':0,'57b35a487f511256':3,'21b865b9073ecba3':3,'52b31de565f7c70e':0,'a215196df9bb969f':0,'68d87182eaa943a0':0,'7257ecbc2d7157a9':3,'22b12faee0d746da':2,'34678f6bc7bc115d':1,'48de6b1649885d22':0,'41e6032b5a5284e9':0,'74738279b67a8d1f':6,'b81c22480fa7462e':0,'c318be57584398b2':0,'676353ae83739b9e':0,'c7a189b5bfb185dd':0,'3630a943f34d96e9':0,'e046b4fe84962f36':0,'151d3bd71448c4d2':0,'a352a05feec019ba':4,'fe8f435b5dc5ee5a':1,'55709205248c61dc':1,'64eb48af9a9b759a':0,'8f1589e4cdbcbb5a':0,'ea2fbf407941fb17':0,'75fbb56e871db809':0,'d0f6a0713a2efc65':1,'c079d4a19f26d075':0,'32eaa1f41540df12':0}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-twelfth-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
