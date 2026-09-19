import json,urllib.request,concurrent.futures,datetime,pathlib
r=pathlib.Path('work/research-2026'); rows=json.load(open(r/'official-root-logo-548-886.json'))
choices={'8dc192a6d1bca741':0,'c45f582aee3bfee8':1,'4dd22dc4c6214705':0,'586ae36115184ec8':4,'d22c9c318c77e5d8':0,'a71d0b96a1b96278':5,'2056e06589e687f9':0,'e9456d44935859a5':0,'8186ff02c864adc9':3,'0b0c2a249abf8613':0,'7d521ebe230947b2':2,'fdf554df1dc5b3de':0,'a08fc88646d0f49d':1,'1eb79020e02b37f2':0,'9a6384a566b4f975':0,'547274b0a786269d':0,'820ff3cae968b673':3,'cb4711c6345ca8ac':1,'44f45930cf60df80':0,'e2441e2ce525d849':0,'cce8bd8c8e93481f':1,'e258d94e58d10413':1,'e1e48e9a51d02dc1':0,'e7b5597579a90eb1':3,'c0e9ead5835bb0e8':0,'f473fac54f283810':0,'b9713e652efb0785':0,'ec04c553e641ceb5':0,'5a60fe445fb92457':0,'4d268ed0481f07fb':0,'1c1232fa96925ab1':1,'0aeac54e89a820db':0,'023c64829133d99b':1,'7317083d2736bf9f':1,'255e3ef64fc0ef02':0,'fe7615b08b9a8dd8':0,'5c78896b4737e436':5,'333d89708dc8068c':1,'375d0e2b95735367':0,'886aebc10728b2ed':0,'fba763dacc448bed':0,'9d0008bf27a81d50':0,'1861bc75ff08bdff':0,'2e1657501da201d5':2,'643696eaabbb7d73':0,'8a9c02e8fa44aedb':0,'937a1dd1805749f5':0,'24ada22856158d4a':0}
def check(row):
 c=row['candidates'][choices[row['id']]]; result={'id':row['id'],'name':row['name'],'source_url':row['page_url'],**c}
 try:
  with urllib.request.urlopen(urllib.request.Request(c['url'].replace(' ','%20'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as x:
   result.update(http_status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes_checked=len(x.read(3000000)),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e: result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=list(pool.map(check,[x for x in rows if x['id'] in choices]))
(r/'official-root-eleventh-assets-verified.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['name'],x.get('http_status'),x.get('content_type'),x.get('error',''))
