import json,pathlib,urllib.parse,collections
r=pathlib.Path('work/research-2026')
def read(n):return json.load(open(r/n))
def keyed(d):
 if isinstance(d,dict):
  for f in ['records','profiles']:
   if f in d:d=d[f];break
 return {v['id']:v for v in d} if isinstance(d,list) else d
p=read('general-round3-90-draft.json');stocks=read('general-round3-stock-proof.json');tickers=dict(zip(['ba4ab3c6bd789b8d','7147a49b21059afe','66e16f9114833b3b','21899ed0e8ca47b0','3668ad043000b53e','45ac8b2227087aca','b9f0f2649dddf27c'],['NYSE: ACH','NASDAQ: ADEA','NASDAQ: ADIL','NASDAQ: ADMA','NASDAQ: ADBE','NASDAQ: ADTN','NYSE: WMS']))
for k,t in tickers.items():
 s=stocks[k];p[k]['sources'].append(dict(url=s['url'],claim=t+'. '+s['claim'],label='Stock listing evidence'));p[k]['ownership']='Publicly traded'
for k in ['86fe124d47be3ece','75013a6f4c7145df']:p[k]['ownership']='Publicly traded'
a={}
for f in ['general-round3-a-branding-audit.json','general-round3-c-branding-audit.json']:a.update(keyed(read(f)))
b=keyed(read('general-round3-b-researched.json'));ba=read('general-round3-b-final.json')['profiles']
for k,v in b.items():
 a[k]=dict(decision='keep' if v.get('logo_url') and ba[k]['decision']=='accepted' else 'hold',logo_url=v.get('logo_url',''))
# Newly fetched exact brand assets are reviewed separately from older agent cache audits.
for k in ['e790f78ba0a14e2b','e79f84eff23e23aa','0805610b4f8279b3']:
 c=read(f'website-cache/{k}.json');u=c.get('logo_url','')
 if c.get('logo_http_status')==200 and u.startswith('https://') and any(x in u.lower() for x in ['patientpoint','acxiom','advamed']):a[k]=dict(decision='keep',logo_url=u)
for k,v in p.items():
 v.pop('id',None);v.update(as_of='2026-09-05',checked_at='2026-09-05',status='unresolved' if v['review_outcome']=='unresolved' else 'sourced',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved');v.setdefault('featured',False);v.setdefault('legal_form','')
 if v['ownership']=='Nonprofit':v['ownership']='Nonprofit / tax-exempt'
 c=read(f'website-cache/{k}.json') if (r/f'website-cache/{k}.json').exists() else {}
 def norm(u):
  q=urllib.parse.urlsplit(u or '');return q.hostname,q.path.rstrip('/')
 same=v.get('website') and norm(v['website']) in [norm(c.get('requested_url')),norm(c.get('final_url'))]
 v['website_status']='partial' if v.get('website') else 'unresolved'
 if v['review_outcome']=='unresolved':v.update(website='',website_status='unresolved')
 elif same and c.get('http_status')==200 and len(c.get('text',''))>150:
  v['website_status']='verified'
  if a.get(k,{}).get('decision')=='keep' and a[k].get('logo_url')==c.get('logo_url') and c.get('logo_http_status')==200 and c.get('logo_url','').startswith('https://'):
   for f in ['logo_url','logo_kind','logo_source_url']:v[f]=c[f]
   v['logo_status']='official_site_asset'
 elif v['review_outcome']=='confirmed':v['review_outcome']='partial'
 v['sources']=[dict(url=s['url'],label=s.get('label','Organization evidence'),claim=s['claim']) for s in v['sources']]
 assert all(s['url'].startswith('https://') and s['claim'] for s in v['sources']),k
 assert v['sources'] and v['identity_evidence'] and len(v['description'])>25,k
# Invalid guessed domain excluded, without replacing it with another unproven identity.
k='b8aa7e8ac6e09cc1';p[k].update(website='',website_status='unresolved',review_outcome='partial',ownership='Unknown');p[k]['sources']=[s for s in p[k]['sources'] if 'actforultrarare.org' not in s['url']];p[k]['identity_evidence']='Supplied disclosure identifies ACT for Ultra Rare; guessed standalone domain failed DNS and was removed. Current legal identity remains partial.'
assert p[k]['sources']
for k in ['3668ad043000b53e','86fe124d47be3ece','75013a6f4c7145df','ce5c81386d9d6b69']:p[k]['featured']=True
assert len(p)==90
(r/'general-round3-90-rootchecked.json').write_text(json.dumps(p,indent=2)+'\n');print(collections.Counter(v['review_outcome'] for v in p.values()),'logos',sum(bool(v['logo_url']) for v in p.values()))
