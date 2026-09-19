import json,pathlib,gzip,re,datetime
p=pathlib.Path('lobbying-map/research/profiles.json');allp=json.loads(p.read_text());cs={c['id']:c for c in json.load(gzip.open('lobbying-map/public/data/directory-v2.json.gz'))['companies']}
for batch in ['c','d']:
 rows=json.load(open('work/organization-research/batch-'+batch+'.json'))
 if batch=='c':rows['0f6187133c1bd69e']=rows.pop('0f6187133c1bd69c')
 for id,x in rows.items():
  assert id in cs and id not in allp
  x['as_of']=x.pop('asof',x.get('as_of','2026-09-04'));x.pop('claim',None)
  for s in x['sources']:
   if 'undefined' in s['url']:
    c=cs[id];shard=json.load(gzip.open('lobbying-map/public/data/reports/'+c['members'][0][:2]+'.json.gz'));fid=shard[c['members'][0]][0]['id'];s['url']='https://lda.gov/filings/public/filing/'+fid+'/print/';s['claim']='Original lobbying filing belonging to this directory entry.'
   if 'SEC submissions metadata'==s['label'] and id!='005a36a209d27215':
    cik=str(int(re.search(r'CIK(\d+)',s['url']).group(1)));d=json.load(open('work/organization-research/sec-submissions/'+cik+'.json'))['data'];assert d['tickers'] and d['exchanges'];s['claim']='SEC issuer '+d['name']+'; '+', '.join(e.upper()+': '+t for e,t in zip(d['exchanges'],d['tickers']) if e and t)+'.'
   s['claim']=re.sub(r'New York Stock Exchange under ticker ([A-Z]+)',r'NYSE: \1',s['claim'])
   s['claim']=re.sub(r'Nasdaq Global Select Market under ticker ([A-Z]+)',r'NASDAQ: \1',s['claim'])
   if id=='973a4a818d799636' and 'investor FAQ' in s['label']:s['claim']='IBM common stock is listed on NYSE and NYSE Texas under ticker IBM (NYSE: IBM).'
  if id=='1874b6e11d321e66':
   for s in x['sources']:
    if '2025 Form 10-K' in s['label']:s['label']='Intel 2024 annual report, filed 2025'
  if id=='005a36a209d27215':
   x['ownership']='Subsidiary of public company'
   x['as_of']='2026-07-01'
   x['notes']='Exxon Mobil Corporation became a wholly owned subsidiary of ExxonMobil Holdings Corporation on July 1, 2026. The new parent succeeded it as the publicly traded issuer (NYSE: XOM); historical lobbying filings retain the original corporation name.'
   x['sources']=[s for s in x['sources'] if s['label']!='SEC submissions metadata']
   x['sources'].extend([
    {'label':'ExxonMobil July 1, 2026 reorganization filing','url':'https://investor.exxonmobil.com/sec-filings/all-sec-filings/content/0001193125-26-291990/d71068d8k12b.htm','claim':'ExxonMobil Holdings Corporation replaced Exxon Mobil Corporation as the listed issuer; NYSE: XOM.'},
    {'label':'ExxonMobil Holdings subsidiary list, July 1, 2026','url':'https://investor.exxonmobil.com/sec-filings/all-sec-filings/content/0001193125-26-291990/d71068dex21.htm','claim':'Exxon Mobil Corporation, New Jersey, is 100 percent owned by the registrant.'}])
  allp[id]=x
p.write_text(json.dumps(allp,ensure_ascii=False,indent=2)+'\n');print('Profiles after merged batches',len(allp))
start=json.load(open('work/organization-research/benchmark-start.json'))
now=datetime.datetime.now(datetime.timezone.utc)
start['review_completed_at']=now.isoformat();start['elapsed_seconds']=(now-datetime.datetime.fromisoformat(start['launched_at'])).total_seconds();start['reviewed_profiles']=16;start['caveat']='Known public brands only; includes parent review and fixes. Not representative of obscure historical organizations. Token cost unavailable.'
pathlib.Path('work/organization-research/benchmark-cd.json').write_text(json.dumps(start,indent=2))
