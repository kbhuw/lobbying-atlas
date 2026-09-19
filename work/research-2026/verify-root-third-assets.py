import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-48-148.json'))
choices={'fd142d43b1517176':8,'fc4553072d954b26':3,'346b138a0f417520':2,'4e760bcde235f5c8':2,'51e1305491bb7484':1,'533ff30325e80fb0':0,'4ff8fb88092e9f25':0,'5bda17c9bfb6fa75':0,'61534fe0b36d34f1':0,'13694ee29ef2cf94':0,'a227ffbe1d3158fb':2,'accd170e45c1f1e6':4,'c5a464fb40abee73':0,'e15fe134cabaf472':4,'61fbed264654c2d2':1,'05e92dd310e0a548':2,'546c84323874bbae':5,'f626360d6db50f6a':1,'d1f6c467dc488a8a':1,'e4a7774dfe0cb6c7':1,'f4c636b784758363':0,'d114063315b60c7d':0,'11fc7ca672fa2895':1,'4cef5b114748037c':0,'37342aace96261d0':0,'528330e1ee018227':3,'354ebfd7b026200f':3,'ec125b676d848925':2,'9336f77c7e3f1015':0,'0a7a47d70930625f':1,'d6f90011e5bf9b81':5,'8fa5a16dc4ac0161':2,'f422497ec02bf797':1,'c560a37fc6fd7a61':1,'f183bf1effe44d7f':1,'8f66f19ea25457fd':4,'1e3bad41a5d736d3':0,'bc2e3a88891199d1':2,'3b219532492f1d57':0}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-third-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
