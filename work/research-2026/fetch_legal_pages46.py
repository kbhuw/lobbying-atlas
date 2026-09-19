import pathlib,json,re,requests,concurrent.futures,urllib.parse
from bs4 import BeautifulSoup
root=pathlib.Path(__file__).resolve().parents[2];b=root/'work/research-2026/legal-pages46';b.mkdir(exist_ok=True);p=json.load(open(root/'work/research-2026/reviewed.json'));rows=json.load(open(root/'work/research-2026/relaxed-address-candidates42.json'));rows=[x for x in rows if p[x['id']]['review_outcome']!='confirmed' and re.search(r'\b(inc|llc|corp|corporation|holdings?|lp|limited|ltd|pc)\b',x['matches'][0]['registration']['client_name'],re.I)][:150];(b/'queue.json').write_text(json.dumps(rows,indent=2))
def exact_name(name,text):
 words=re.findall(r'\w+',name)
 return bool(re.search(r'(?<!\w)'+r'\W+'.join(map(re.escape,words))+r'(?!\w)',text,re.I))
def work(x):
 f=b/(x['id']+'.json')
 if f.exists():return json.load(open(f))
 name=x['matches'][0]['registration']['client_name'];d={'id':x['id'],'filed_name':name,'original_cache':x['cache'],'pages':[],'matches':[]};urls=[p[x['id']]['website']]
 for i in range(8):
  if i>=len(urls):break
  u=urls[i]
  try:
   r=requests.get(u,timeout=(5,12),headers={'User-Agent':'Mozilla/5.0 (compatible; public-records-research)'})
   if 'pdf' in r.headers.get('content-type','').lower():d['pages'].append({'url':r.url,'status':r.status_code,'needs_pdf_review':True});continue
   s=BeautifulSoup(r.content[:1500000],'html.parser')
   for e in s(['script','style','noscript']):e.decompose()
   t=s.get_text(' ',strip=True);page={'url':r.url,'status':r.status_code,'text':t[:140000]};d['pages'].append(page)
   if r.status_code!=200:continue
   if exact_name(name,t):d['matches'].append({'url':r.url,'method':'Exact normalized filed name present; requires identity/context review.'})
   if i==0:
    host=urllib.parse.urlparse(r.url).hostname
    for a in s.find_all('a',href=True):
     label=a.get_text(' ',strip=True).lower();url=urllib.parse.urljoin(r.url,a['href'])
     if urllib.parse.urlparse(url).hostname==host and re.search(r'privacy|terms|legal',label) and url not in urls:urls.append(url)
    origin=urllib.parse.urlunparse((urllib.parse.urlparse(r.url).scheme,urllib.parse.urlparse(r.url).netloc,'','','',''))
    for route in ['/privacy-policy/','/terms-of-use/','/terms-and-conditions/','/privacy/','/legal/']:
     candidate=origin+route
     if candidate not in urls:urls.append(candidate)
    urls=urls[:8]
  except Exception as e:d['pages'].append({'url':u,'error':type(e).__name__})
 f.write_text(json.dumps(d,indent=2,ensure_ascii=False));print(x['id'],len(d['matches']),flush=True);return d
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(work,rows))
matched=[d for d in results if d['matches']];(b/'matches.json').write_text(json.dumps(matched,indent=2,ensure_ascii=False));print('FINISHED',len(rows),'profiles',len(matched),'legal-name candidates',flush=True)
