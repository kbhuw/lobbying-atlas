import pathlib,json,re,requests,concurrent.futures,urllib.parse
from bs4 import BeautifulSoup
root=pathlib.Path(__file__).resolve().parents[2];b=root/'work/research-2026/legal-pages45';b.mkdir(exist_ok=True);p=json.load(open(root/'work/research-2026/reviewed.json'));rows=json.load(open(root/'work/research-2026/relaxed-address-candidates42.json'));done={x['id'] for x in json.load(open(root/'work/research-2026/legal-pages44/queue.json'))};rows=[x for x in rows if x['id'] not in done and p[x['id']]['review_outcome']!='confirmed' and re.search(r'\b(inc|llc|corp|corporation|holdings?|lp|limited)\b',x['matches'][0]['registration']['client_name'],re.I)][:150];(b/'queue.json').write_text(json.dumps(rows,indent=2))
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
def work(x):
 f=b/(x['id']+'.json')
 if f.exists():return json.load(open(f))
 name=x['matches'][0]['registration']['client_name'];d={'id':x['id'],'filed_name':name,'original_cache':x['cache'],'pages':[],'matches':[]};urls=[p[x['id']]['website']]
 for i in range(4):
  if i>=len(urls):break
  u=urls[i]
  try:
   r=requests.get(u,timeout=(5,12),headers={'User-Agent':'Mozilla/5.0 (compatible; public-records-research)'})
   if 'pdf' in r.headers.get('content-type','').lower():d['pages'].append({'url':r.url,'status':r.status_code,'needs_pdf_review':True});continue
   s=BeautifulSoup(r.content[:1500000],'html.parser')
   for e in s(['script','style','noscript']):e.decompose()
   t=s.get_text(' ',strip=True);page={'url':r.url,'status':r.status_code,'text':t[:140000]};d['pages'].append(page)
   if r.status_code!=200:continue
   if norm(name) in norm(t):d['matches'].append({'url':r.url,'method':'Exact normalized filed name present; requires identity/context review.'})
   if i==0:
    host=urllib.parse.urlparse(r.url).hostname
    for a in s.find_all('a',href=True):
     label=a.get_text(' ',strip=True).lower();url=urllib.parse.urljoin(r.url,a['href'])
     if urllib.parse.urlparse(url).hostname==host and re.search(r'privacy|terms|legal',label) and url not in urls:urls.append(url)
    urls=urls[:4]
  except Exception as e:d['pages'].append({'url':u,'error':type(e).__name__})
 f.write_text(json.dumps(d,indent=2,ensure_ascii=False));print(x['id'],len(d['matches']),flush=True);return d
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(work,rows))
matched=[d for d in results if d['matches']];(b/'matches.json').write_text(json.dumps(matched,indent=2,ensure_ascii=False));print('FINISHED',len(rows),'profiles',len(matched),'legal-name candidates',flush=True)
