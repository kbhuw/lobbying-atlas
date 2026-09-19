import json,pathlib,datetime,re,gzip,collections
root=pathlib.Path('work/research-2026');site=pathlib.Path('lobbying-map');sample={c['id']:c for c in json.load(open(root/'sample.json'))};old=json.load(open(site/'research/profiles.json'));ps={}
for b in 'abc':
 rows=json.load(open(root/('output-'+b+'.json')));assert set(rows)=={c['id'] for c in json.load(open(root/('input-'+b+'.json')))}
 ps.update(rows)
assert len(ps)==100
# Apply concrete QA corrections; keep rejected claims out of citations too.
p=ps['65a085bed4d3b491'];p['ownership']='Unknown'
p=ps['7595bb424fff28dc'];p['sources']=[s for s in p['sources'] if 'activateglobally' not in s['url'] and 'civic' not in s['claim'].lower() and 'privacy-policy' not in s['url']]
p=ps['0667298c4d614051'];p['sources']=[s for s in p['sources'] if 'modernstates' not in s['url']];p['ownership']='Unknown';p['notes']='The filing uses this former-name qualifier; it does not independently establish continuity with every FS-branded legal entity.'
p=ps['0abe5b7cf46d3470'];p['kind']='Business';p['ownership']='Subsidiary of public company';p['sources'].append({'label':'Yamaha U.S. subsidiary announcement','url':'https://global.yamaha-motor.com/news/2026/0226/subsidiary.html','claim':'Yamaha Motor Corporation, U.S.A. is the U.S. subsidiary. The listed parent is Yamaha Motor Co., Ltd.'})
p=ps['b79f47c3c98aceed'];p['kind']='Business';p['ownership']='Subsidiary';p['notes']='Fitch Ratings is part of Fitch Group, wholly owned by Hearst. This profile does not label Fitch Ratings as a separately traded company.';p['sources'].append({'label':'Fitch Group ownership history','url':'https://www.fitch.group/history/','claim':'Fitch Group became a wholly owned Hearst subsidiary in 2018.'})
# Remove unsupported private classifications instead of inferring from lack of ticker.
for p in ps.values():
 if p.get('ownership') in ('Private','Privately held'):p['ownership']='Unknown';p['notes']=(p.get('notes','')+' Current private ownership needs a specific ownership source.').strip()
# Company-published CEO statement explicitly supports this one.
p=ps['f7a61c56647f3407'];p['ownership']='Privately held';p['sources'].append({'label':'Imagine360 CEO on company ownership','url':'https://www.imagine360.com/news/news-philadelphia-inquirer-imagine360-helping-companies-save-money-employee-health-coverage/','claim':'Company-published interview describes Imagine360 as privately owned.'})
for id,url,claim in [('5a6652fedd970007','https://investors.fiserv.com/','Fiserv investor relations identifies NASDAQ: FISV.'),('769235308e8175bc','https://www.eaton.com/us/en-us/company/investor-relations/financial-presentations-webcasts.html','Eaton Corporation plc investor relations identifies NYSE: ETN.')]:
 ps[id]['sources'].append({'label':'Official investor relations','url':url,'claim':claim})
for id,p in ps.items():
 base=sample[id].get('profile',{});p.setdefault('featured',base.get('featured',False));p.setdefault('legal_form','');p.setdefault('notes','');p.setdefault('as_of',p.get('checked_at','2026-09-04'));p['checked_at']=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
 if p.get('ownership','').startswith('Joint venture'):p['notes']+=' '+p['ownership'];p['ownership']='Joint venture'
 if p.get('ownership')=='Government body':p['ownership']='Not applicable'
 if re.search(r'government|public authority|public water agency|tribal',p.get('kind',''),re.I):p['kind']='Government';p['ownership']='Not applicable'
 if p.get('kind') in ('Private company','Public company','Alternative asset manager'):p['kind']='Business'
 p['name']=p['name'].replace('Mckendree','McKendree').replace('Bethune Cookman','Bethune-Cookman').replace('Mufg','MUFG').replace('Basf Corp','BASF Corp.').replace('Ymca Of The USA','YMCA of the USA').replace('National Alliance TO END','National Alliance to End').replace('Sscafca -','SSCAFCA —')
 p['status']='unresolved' if p.get('review_outcome')=='unresolved' or 'exact lobbying client could not' in p['description'].lower() else 'sourced'
 if p['status']=='unresolved':p['website']='';p['website_status']='unresolved'
 p['review_outcome']='confirmed' if p['status']=='sourced' and p.get('website') and p.get('ownership') not in ('Unknown','') and p.get('kind')!='Unknown' else ('unresolved' if p['status']=='unresolved' else 'partial')
 # Retain registry identity evidence; add filing links without copying raw contact data.
 evidence=p.get('identity_evidence',[])
 if isinstance(evidence,list):
  for e in evidence[:2]:p['sources'].append({'label':'Original lobbying disclosure — '+e.get('source_member',''),'url':e['source_url'],'claim':e.get('claim') or 'Disclosed client '+str(e.get('name',''))+'; '+str(e.get('city') or '')+', '+str(e.get('state') or '')+'; '+str(e.get('description') or '')})
 p['sources']=list({(s['url'],s['claim']):s for s in p['sources'] if s.get('url','').startswith('https://') and 'undefined' not in s['url']}.values())
 # Status checks rely on direct SEC registry record too, not only ticker formatting.
 if p['ownership']=='Publicly traded':
  sec=next((s for s in p['sources'] if 'data.sec.gov/submissions/' in s['url']),None)
  if sec:
   cik=str(int(re.search(r'CIK(\d+)',sec['url']).group(1)));f=pathlib.Path('work/organization-research/sec-submissions')/(cik+'.json')
   if f.exists():
    d=json.load(open(f))['data'];sec['claim']+=' '+', '.join(e.upper()+': '+t for e,t in zip(d.get('exchanges') or [],d.get('tickers') or []) if e and t)
  # Other primary claims use conventional exchange names; normalize presentation only.
  for s in p['sources']:s['claim']=re.sub(r'NYSE under ticker ([A-Z]+)',r'NYSE: \1',s['claim'])
 p['logo_url']='';p['logo_kind']='';p['logo_source_url']='';p['logo_status']='unresolved'
 f=root/'website-cache'/(id+'.json')
 if f.exists():
  a=json.load(open(f))
  if a['requested_url']==p.get('website') and a.get('logo_http_status')==200:
   for k in ('logo_url','logo_kind','logo_source_url'):p[k]=a[k]
   p['logo_status']='official_site_asset';p['sources'].append({'label':'Official website branding','url':a['logo_source_url'],'claim':'This website supplies the displayed '+('site icon' if a['logo_kind']=='site_icon' else 'logo')+'. Image URL responded successfully when checked.'})
 ps[id]=p
# Preserve subsequent verified batches and corrections when replaying the pilot.
existing=site/'research/reviewed-2026.json'
if existing.exists():ps.update(json.loads(existing.read_text()))
(root/'reviewed.json').write_text(json.dumps(ps,ensure_ascii=False,indent=2)+'\n')
# Publication overlay is reproducible and separate from the original manual ledger.
(site/'research/reviewed-2026.json').write_text(json.dumps(ps,ensure_ascii=False,indent=2)+'\n')
print({'reviewed':len(ps),'outcomes':dict(collections.Counter(p['review_outcome'] for p in ps.values())),'websites':sum(bool(p['website']) for p in ps.values()),'logos':dict(collections.Counter(p['logo_kind'] or 'unresolved' for p in ps.values()))})
