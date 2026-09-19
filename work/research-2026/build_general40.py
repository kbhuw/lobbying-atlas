import json,pathlib,collections,urllib.parse
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round40-root-draft.json'))
rows=json.load(open(r/'general-round40-input.json'))
# Hold parent assets where the exact subsidiary branding has not been established.
allow={0,2,5,6,7,9,10,13,15,16,17,18,19,20,22,24,29,31,32,34,35,37,38,39,41,42,43,44,45,46,49,50,52,53,56,58,59,60,61,63,64,65,67,69,70,76,78,79,80,81,82,84,85,86,87,88,89,90,91,92,93,94,97,98,99}
hold={row['id'] for i,row in enumerate(rows) if i not in allow}
for k,v in p.items():
 v.pop('id',None);v.pop('logo_decision',None)
 v.update(as_of='2026-09-06',checked_at='2026-09-06',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved');v.setdefault('featured',False);v.setdefault('legal_form','')
 c=json.load(open(r/f'website-cache/{k}.json')) if (r/f'website-cache/{k}.json').exists() else {}
 def norm(u):
  q=urllib.parse.urlsplit(u or '');return q.hostname,q.path.rstrip('/')
 same=v.get('website') and norm(v['website']) in [norm(c.get('requested_url')),norm(c.get('final_url'))]
 v['website_status']='partial' if v.get('website') else 'unresolved'
 if v['review_outcome']=='unresolved':v.update(website='',website_status='unresolved')
 elif same and c.get('http_status')==200 and len(c.get('text',''))>150:
  v['website_status']='verified'
  if k not in hold and c.get('logo_http_status')==200 and c.get('logo_url','').startswith('https://'):
   for f in ['logo_url','logo_kind','logo_source_url']:v[f]=c[f]
   v['logo_status']='official_site_asset'
 elif v['review_outcome']=='confirmed':v['review_outcome']='partial'
 v['status']='unresolved' if v['review_outcome']=='unresolved' else 'sourced'
 if v['ownership'] in ['Privately held','Family-owned company','Private company, taken private by an affiliate of Thomas H. Lee Partners in May 2024']:
  old=v['ownership'];v['ownership']='Private company';v['notes']=v.get('notes','')+' '+old+'.'
 if v['ownership'] in ['Nonprofit organization','Nonprofit health system','Tax-exempt nonprofit','Tax-exempt organization','Nonprofit association']:v['ownership']='Nonprofit / tax-exempt'
 if v['ownership'] in ['Labor union','Union','Union federation','Trade association']:v['ownership']='Not applicable'
 if v['ownership'] in ['Public agency','Municipal government']:v['ownership']='Government body'
 v['sources']=[dict(url=s['url'],label=s.get('label','Organization evidence'),claim=s['claim']) for s in v['sources']]
 seen=set();v['sources']=[s for s in v['sources'] if not ((s['url'],s['claim']) in seen or seen.add((s['url'],s['claim'])))]
 assert all(s['url'].startswith('https://') and s['claim'] for s in v['sources']),k
 assert v['sources'] and v['identity_evidence'] and len(v['description'])>25,k
assert len(p)==100
(r/'general-round40-100-rootchecked.json').write_text(json.dumps(p,indent=2)+'\n')
print(collections.Counter(v['review_outcome'] for v in p.values()),'websites',sum(bool(v['website']) for v in p.values()),'logos',sum(bool(v['logo_url']) for v in p.values()))
