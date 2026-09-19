import json,pathlib,datetime
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def source(u,c):return {'url':u,'label':'Official organization evidence','claim':c}
rows=json.load(open(r/'featured74-first10.json'))+json.load(open(r/'featured74-middle10.json'))
for d in rows:
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','ownership','website']};f.update(review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced')
 if f['review_outcome']=='confirmed':f['website_status']='verified'
 s=[source(d['official_url'],d['exact_official_excerpt'])]
 if i=='4cdf0c01a517cb40':f.update(description='U.S. entity in Magna’s automotive components and mobility technology group.',notes='Exact Inc. entity is named in Magna’s 2019 privacy appendix; that dated source establishes identity, not current ownership.')
 if i=='9dc74bd43a73ddc3':f['ownership']='Subsidiary';f['notes']='Manitou’s 2025 results, published March 2026, report 100% group interest in Manitou America Holding Inc.'
 if i=='106207252b253227':f['notes']='SEC 2021 filing identifies Manna Drone Delivery Inc.; current Manna brand supplies drone deliveries. Current ownership remains unverified.'
 if i in ['b36f3458ad6db61f','325c7c2d37bd917d']:
  f.update(ownership='Mutual insurance group',description='Life insurer providing insurance, annuities, retirement and financial services; operates for policyowners rather than outside shareholders.',notes='Exact filed insurer name retained. MassMutual Financial Group is a company brand; this does not treat every group subsidiary as the same legal entity.')
  s.extend([source('https://www.massmutual.com/about-us/corporate-governance','Company describes its mutual structure and policyowners rather than shareholders.'),source('https://www.massmutual.com/legal/terms-of-use','Names Massachusetts Mutual Life Insurance Company and identifies MassMutual Financial Group among its company or subsidiary marks.')])
 if i=='191856e041d0c3fe':
  f.update(review_outcome='confirmed',website_status='verified',notes='Official French legal terms explicitly identify Mastercard International Incorporated as doing business under the name Mastercard Worldwide. This is a trading-name bridge, not an inference from similar branding.',identity_evidence='Official legal terms establish the Worldwide trading name of Mastercard International Incorporated.')
 if i=='a43d7506e764fbbc':
  f.update(ownership='Public company',notes='August 31, 2026 investor release identifies Mattel, Inc. (NASDAQ: MAT).',logo_url='https://cdn.builder.io/api/v1/image/assets%2F8be5a791274f462fa36ba4e5344b7513%2Fb435f1e62dd0476b95d4d11fa240b066',logo_kind='logo',logo_source_url='https://corporate.mattel.com/',logo_status='official_site_asset',logo_background='light')
  s.append(source('https://investors.mattel.com/news/news-details/2026/Mattel-to-Participate-in-Upcoming-Investor-Events/default.aspx','August 31, 2026 release names Mattel, Inc. and NASDAQ: MAT.'));s.append(source('https://corporate.mattel.com/','Header asset labelled Mattel Logo; fetched and visually verified red Mattel wordmark.'))
 if i=='578e2d0dc1ba5f4e':f['ownership']='Unknown';f['notes']='Official about page names MCR Health, Inc.; tax status not established by the quoted identity evidence.'
 if i=='9d5a23d53d06181e':f.update(description='Filing names McKesson Corporation and its US Oncology affiliate. The precise affiliate and former-name relationship remain unresolved.',kind='Healthcare company and affiliate disclosure',notes='Original combined name retained. It is not recast as an on-behalf-of intermediary filing; exact affiliate and former-name relationship remain unresolved.')
 p[i].update(f)
 seen={v['url'] for v in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append({'id':i,'decision':f['review_outcome'],'notes':f['notes']})
(r/'featured74-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured74-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
mfile=pathlib.Path('lobbying-map/research/verified-entity-merges.json');m=json.load(open(mfile));(r/'featured74-merges-before.json').write_text(json.dumps(m,indent=2)+'\n')
ids=['ca2d1b497489a6dc','191856e041d0c3fe'];assert not any(set(ids)&set(x['source_ids']) for x in m)
claim='Official French terms identify Mastercard International Incorporated as doing business under the name Mastercard Worldwide; these source groups differ by this explicit trading name.'
m.append({'canonical_id':ids[0],'source_ids':ids,'rationale':claim,'sources':[{'url':'https://www.mastercard.com/fr/fr/conditions-utilisation.html','claim':claim}],'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});mfile.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('20 updates; confirmations',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()),'; 1 logo; 1 merge')
