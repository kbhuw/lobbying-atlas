import json,time,urllib.request,urllib.parse,pathlib
base=pathlib.Path(__file__).parent
params={'filing_year':2025,'filing_specific_lobbying_issues':'"artificial intelligence"','page_size':25,'format':'json','ordering':'dt_posted'}
page=1
while True:
    dest=base/f'page-{page:04d}.json'
    if dest.exists():
        d=json.loads(dest.read_text())
    else:
        url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode(dict(params,page=page))
        for attempt in range(5):
            try:
                with urllib.request.urlopen(url,timeout=60) as r: d=json.load(r)
                dest.write_text(json.dumps(d)); break
            except Exception as e:
                print('retry',page,str(e),flush=True); time.sleep(15+attempt*10)
        else: raise RuntimeError('page failed '+str(page))
        time.sleep(4.4)
    if page%10==0 or page==1: print('page',page,'of',(d['count']+24)//25,'count',d['count'],flush=True)
    if not d.get('next'): break
    page+=1
print('COMPLETE',page,flush=True)
