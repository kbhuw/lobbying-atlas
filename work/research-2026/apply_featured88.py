import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
assert not (r/'featured88-before.json').exists()
rows=json.load(open(r/'featured88-first10.json'))+json.load(open(r/'featured88-middle10.json'))
names=['Terradepth','TerraPower LLC','Terrestrial Energy Inc.','Terumo BCT','Tether Operations, S.A. de C.V.','Tetra Pak','Textron','Thales USA','Thatch Health, Inc.','ThayerMahan Inc.','Avangrid (via The Abraham Group)','Acutronic','The ALS Association','The Baldwin Group','Blackstone (formerly The Blackstone Group)','The Carlyle Group','The Chemours Company','City University of New York (CUNY)','Uber (via The Doerrer Group)','The GEO Group']
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','website']};f.update(name=names[idx],ownership='Unknown',review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[src(d['official_url'],d['exact_official_excerpt'])]
 for x in d.get('sources',[]):
  if x.get('excerpt'):s.append(src(x['url'],x['excerpt']))
 if idx in [2,14,15,16,19]:f['ownership']='Public company'
 if idx==3:f['ownership']='Subsidiary'
 if idx==12:f['ownership']='Nonprofit'
 if idx==17:f['ownership']='Public institution'
 if idx in [6,7,13]:f.update(review_outcome='partial',website_status='partial')
 if idx==6:f['notes']=f['identity_evidence']='Textron Inc. and its public listing are established. TEXTRON CORP remains an unbridged filed alias; no legal rename or equivalence is asserted.'
 if idx==13:f['notes']=f['identity_evidence']='The Baldwin Insurance Group, Inc. is the public issuer previously named BRP Group, Inc. This does not establish the filed The Baldwin Group, Inc. alias as its legal name; brand context established, exact Inc variant unverified.'
 if idx in [10,18]:
  who='The Abraham Group' if idx==10 else 'The Doerrer Group';client='Avangrid' if idx==10 else 'Uber Technologies, Inc.';reg='d3955860-6c7c-44fd-9f3a-7f6490d75e8e' if idx==10 else 'e50c43d6-f610-4fd8-883e-0f8e2faf69b2';report='1af25741-d534-4e53-9523-99e159717ca6' if idx==10 else 'fba5dbad-b856-435a-a155-3357513056a0'
  f.update(review_outcome='confirmed',ownership='Not applicable',kind='Represented-client filing label',description=f'{who} acting on behalf of {client}. '+('Avangrid operates energy utilities and renewable-energy businesses.' if idx==10 else 'Uber provides ride-hailing, delivery and freight technology services.'))
  s+=[src(f'https://lda.gov/filings/public/filing/{reg}/print/',f'Original registration explicitly names {who} on behalf of {client} and describes consulting/government affairs activity.'),src(f'https://lda.gov/filings/public/filing/{report}/print/',f'2026 second-quarter filing retains the explicit {who} on behalf of {client} relationship.')];f['notes']=f['identity_evidence']='Original registration and current 2026 report establish the represented-client label. Preserve both intermediary and client; this is not a corporate ownership relationship.'
 if idx==14:
  s=[src('https://www.sec.gov/Archives/edgar/data/1393818/000119312521239233/d188135d10q.htm','SEC filing records the completed legal name change from The Blackstone Group Inc. to Blackstone Inc., effective August 6, 2021.')];f['notes']=f['identity_evidence']=s[0]['claim']
 if idx==15:s.append(src('https://ir.carlyle.com/static-files/4ec44a7d-ea16-48e1-977a-f2f5b8aa7fc9','February 2026 issuer update identifies Carlyle as NASDAQ CG, a global investment firm.'))
 if idx==16:s=[src('https://www.chemours.com/en/news-media-center/all-news/press-releases/2026/the-chemours-company-reports-second-quarter-results','August 2026 results identify The Chemours Company, NYSE CC, and its industrial and specialty chemicals businesses.')]
 if idx==19:s.append(src('https://investors.geogroup.com/static-files/1f07849f-9af5-4d49-9b1d-484eda283140','2025 annual report identifies The GEO Group, Inc. and its NYSE GEO common stock.'))
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes']))
x=next(x for x in json.load(open(r/'featured88-logo-candidates.json'))['candidates'] if x['id']=='c813336416c273a1')
p[x['id']].update(logo_url=x['asset_url'],logo_source_url=x['source_page'],logo_kind='logo',logo_status='official_site_asset',logo_background='light');p[x['id']]['sources'].append(src(x['source_page'],x['evidence']))
(r/'featured88-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured88-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()));print('Status changes',[(i,b.get('status'),p[i]['status']) for i,b in before.items() if b.get('status')!=p[i]['status']])
