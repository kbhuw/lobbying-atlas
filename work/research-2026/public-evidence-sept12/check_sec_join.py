import json,pathlib,urllib.request,re,concurrent.futures,time,unicodedata
w=pathlib.Path('work/research-2026');out=w/'public-evidence-sept12';d=json.loads((w/'reviewed.json').read_text());rows=json.loads((out/'new-sec-join-candidates.json').read_text());cache=out/'sec-live-join';cache.mkdir(exist_ok=True);by={r['id']:f"https://data.sec.gov/submissions/CIK{r['candidate']['cik']:010d}.json" for r in rows}
def fetch(u):
 time.sleep(.6)
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'LobbyingAtlas public records research contact kush@kush.pw'}),timeout=15) as f:x=json.load(f)
  (cache/u.rsplit('/',1)[-1]).write_text(json.dumps(x));return u,x
 except Exception as e:return u,{'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:data=dict(ex.map(fetch,sorted(set(by.values()))))
def norm(n):
 n=unicodedata.normalize('NFKD',n).lower().replace('&','and');n=re.sub(r'\b(incorporated|corporation|corp|inc|plc|limited|ltd|the)\b','',n);return re.sub(r'[^a-z0-9]','',n)
res=[]
for k,u in by.items():
 v=d[k];s=data[u];names=[v['name']]
 for src in v.get('sources',[]):
  claim=src.get('claim','')
  m=re.search(r'Disclosed client ([^;]+)',claim,re.I)
  if m:names.append(m.group(1).strip(' ."'))
 z={'id':k,'name':v['name'],'url':u,'issuer':s.get('name'),'cik':s.get('cik'),'tickers':s.get('tickers'),'exchanges':s.get('exchanges'),'error':s.get('error'),'exact_normalized_name_match':bool(s.get('name')) and norm(s['name']) in [norm(n) for n in names],'website_status':v.get('website_status'),'description':v.get('description'),'ownership':v.get('ownership')};res.append(z)
(out/'sec-join-results.json').write_text(json.dumps(res,indent=2));print(json.dumps({'profiles':len(res),'unique_requests':len(data),'fetched':sum(not r['error'] for r in res),'exact_with_listing':sum(r['exact_normalized_name_match'] and bool(r['tickers']) and bool(r['exchanges']) for r in res)},indent=2))
