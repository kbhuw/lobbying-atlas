import json,pathlib,re,urllib.parse,concurrent.futures,requests,time
from bs4 import BeautifulSoup
BASE=pathlib.Path(__file__).resolve().parent;ROOT=BASE.parents[2]
p=json.load(open(ROOT/'work/research-2026/reviewed.json'));q=json.load(open(ROOT/'work/research-2026/registration-evidence-queue.json'))
rows=[x for x in q if x['id'] in p and p[x['id']].get('review_outcome')=='partial' and p[x['id']].get('website') and x['evidence']]
rows.sort(key=lambda x:p[x['id']]['name'].casefold());rows=rows[:100]
(BASE/'queue.json').write_text(json.dumps(rows,indent=2))
def norm(s):
 s=re.sub(r'[^A-Z0-9 ]',' ',s.upper())
 for a,b in [('STREET','ST'),('AVENUE','AVE'),('ROAD','RD'),('BOULEVARD','BLVD'),('SUITE','STE'),('PARKWAY','PKWY'),('NORTHWEST','NW'),('SOUTHWEST','SW'),('SOUTHEAST','SE'),('NORTHEAST','NE'),('DRIVE','DR')]:s=re.sub(r'\b'+a+r'\b',b,s)
 return ' '.join(s.split())
def work(x):
 out=BASE/(x['id']+'.json')
 if out.exists():return
 profile=p[x['id']];url=profile['website'];record={'id':x['id'],'name':profile['name'],'initial_url':url,'pages':[],'matches':[],'checked_at':'2026-09-12'}
 try:
  urls=[url]
  for j in range(3):
   if j>=len(urls):break
   u=urls[j]
   try:
    r=requests.get(u,timeout=(5,10),headers={'User-Agent':'Mozilla/5.0 (compatible; public-records-research)'});s=BeautifulSoup(r.content[:1500000],'html.parser')
    for e in s(['script','style','noscript']):e.decompose()
    t=s.get_text(' ',strip=True);record['pages'].append({'url':r.url,'status':r.status_code,'text':t[:120000],'logos':[{'url':urllib.parse.urljoin(r.url,i.get('src','')),'alt':i.get('alt','')} for i in s.find_all('img') if 'logo' in str(i).lower()][:5]})
    if r.status_code!=200:continue
    nt=norm(t)
    for e in x['evidence']:
     addr=norm(e['address']);city=norm(e['city'])
     if len(addr)>=12 and len(city)>=3 and addr in nt and city in nt:
      record['matches'].append({'page_url':r.url,'registration':e,'method':'Full normalized street and city occur in official candidate page; requires human review of context and identity.'})
    if j==0:
     host=urllib.parse.urlparse(r.url).hostname
     links=[]
     for a in s.find_all('a',href=True):
      href=urllib.parse.urljoin(r.url,a['href']);label=a.get_text(' ',strip=True).lower()
      if urllib.parse.urlparse(href).hostname==host and any(z in label for z in ['contact','about us']) and href not in urls+links:links.append(href)
     urls.extend(links[:2])
   except Exception as e:record['pages'].append({'url':u,'error':type(e).__name__})
 except Exception as e:record['error']=type(e).__name__
 out.write_text(json.dumps(record,indent=2,ensure_ascii=False));print(x['id'],profile['name'],'matches',len(record['matches']),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:list(ex.map(work,rows))
summary=[]
for x in rows:
 d=json.load(open(BASE/(x['id']+'.json')))
 if d['matches']:summary.append({'id':d['id'],'name':d['name'],'matches':d['matches']})
(BASE/'matches.json').write_text(json.dumps(summary,indent=2));print('FINISHED',len(rows),'profiles;',len(summary),'candidate matches',flush=True)
