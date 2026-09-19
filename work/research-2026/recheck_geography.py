"""Resume saved filing checks; cache successes and stop on LDA throttling."""
import datetime, gzip, json, pathlib, time, urllib.error, urllib.request
root=pathlib.Path(__file__).resolve().parent
site=root.parent.parent/'lobbying-map'
queue=json.loads((root/'unresolved-geography-recheck-queue.json').read_text())
cards={c['id']:c for c in json.loads(gzip.decompress((site/'research/directory-base.json.gz').read_bytes()))['companies']}
output=root/'unresolved-geography-filing-results.json'
prior={x['id']:x for x in json.loads(output.read_text())} if output.exists() else {}
stop=False
for x in queue:
 reports=[]
 for member in cards[x['id']]['members']:
  reports.extend(json.loads(gzip.decompress((site/f'public/data/reports/{member[:2]}.json.gz').read_bytes())).get(member,[]))
 ids=list(dict.fromkeys(v['id'] for v in reports if v['year']==2026))[:2]
 row=prior.setdefault(x['id'],dict(x,checked_filings=[],total_2026_filings=len([v for v in reports if v['year']==2026])))
 checked={z['url']:z for z in row['checked_filings'] if z.get('url')}
 for fid in ids:
  url=f'https://lda.gov/api/v1/filings/{fid}/';cache=root/f'geo-filing-{fid}.json'
  if cache.exists():d=json.loads(cache.read_text());result={'url':url,'status':200,'client':d.get('client'),'registrant':d.get('registrant',{}).get('name')}
  else:
   try:
    with urllib.request.urlopen(url,timeout=25) as response:d=json.load(response)
    cache.write_text(json.dumps(d,indent=2)+'\n');result={'url':url,'status':200,'client':d.get('client'),'registrant':d.get('registrant',{}).get('name')}
   except urllib.error.HTTPError as e:
    result={'url':url,'status':e.code,'retry_after':e.headers.get('Retry-After')}
    if e.code==429:stop=True
   except Exception as e:result={'url':url,'error':type(e).__name__};stop=True
   if not stop:time.sleep(5)
  checked[url]=result;row['checked_filings']=list(checked.values())
  output.write_text(json.dumps([prior[v['id']] for v in queue if v['id'] in prior],indent=2)+'\n')
  if stop:print('Stopped; saved response:',result,flush=True);break
 if stop:break
print('Saved completed observations. HTTP errors are not absent geography.')
