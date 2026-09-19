import json,pathlib,urllib.request,concurrent.futures,sys
from logo_candidates import Page
r=pathlib.Path('work/research-2026');out=r/'logo-ranker-fixtures';out.mkdir(exist_ok=True)
cases=[('ncpdp','National Council for Prescription Drug Programs','https://www.ncpdp.org/'),('ndrn','National Disability Rights Network','https://www.ndrn.org/'),('core','National Community Renaissance','https://nationalcore.org/'),('nfff','National Fallen Firefighters Foundation','https://www.firehero.org/'),('cdcf','CDC Foundation','https://www.cdcfoundation.org/'),('ncssma','National Council of Social Security Management Associations','https://www.ncssma.com/')]
def one(c):
 key,name,url=c;f=out/(key+'.html')
 try:
  if not f.exists():f.write_bytes(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read())
  p=Page(name,url);p.feed(f.read_text(errors='replace'));return {'name':name,'url':url,'top':sorted(p.candidates)[:3]}
 except Exception as e:return {'name':name,'error':str(e)}
results=list(concurrent.futures.ThreadPoolExecutor(6).map(one,cases));(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
for x in results:print(json.dumps(x))
