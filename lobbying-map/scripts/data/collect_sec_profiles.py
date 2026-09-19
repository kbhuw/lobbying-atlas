"""Collect SEC metadata for exact-name candidates, retaining unverified match status."""
import concurrent.futures,datetime,json,pathlib,time,threading,urllib.request
root=pathlib.Path(__file__).resolve().parents[3]/'work/organization-research'
out=root/'sec-submissions';out.mkdir(exist_ok=True)
rows=json.loads((root/'sec-candidates.json').read_text());lock=threading.Lock();next_at=0

def one(r):
 global next_at
 cik=r['sec']['cik'];p=out/f'{cik}.json'
 if p.exists():return 'cached'
 u=f'https://data.sec.gov/submissions/CIK{cik:010d}.json'
 for attempt in range(3):
  with lock:
   delay=max(0,next_at-time.monotonic());next_at=max(next_at,time.monotonic())+.65
  time.sleep(delay)
  try:
   req=urllib.request.Request(u,headers={'User-Agent':'LobbyingTransparencyResearch contact kush@puffle.ai'})
   with urllib.request.urlopen(req,timeout=30) as response:d=json.load(response)
   p.write_text(json.dumps({'source_url':u,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'data':d}))
   return 'downloaded'
  except Exception as e:
   if attempt==2:return 'error: '+type(e).__name__
   time.sleep(10*(attempt+1))
counts={}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for result in ex.map(one,rows):
  counts[result]=counts.get(result,0)+1
  progress={'total_candidates':len(rows),'processed':sum(counts.values()),'counts':counts,'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Unverified exact-name SEC candidates; not independent identity confirmation.'}
  (root/'sec-progress.json').write_text(json.dumps(progress,indent=2))
  if sum(counts.values())%50==0:print(progress,flush=True)
print(progress,flush=True)
