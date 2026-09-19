import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
rows=json.load(open(r/'featured86-first10.json'))+json.load(open(r/'featured86-middle10.json'))
names=['3M (via Sullivan Strategies)','Sumitomo Pharma America, Inc.','Sun Life Financial (U.S.) Services Company, Inc.','Sun Pharmaceutical Industries, Inc.','Suncor Energy (U.S.A.) Inc.','Suniva, Inc.','Superior Essex International Inc.','Superior Group of Companies','Susan G. Komen','Taiwan Semiconductor Manufacturing Company (TSMC)','Tanium','Targa Resources','Taseko Mines Limited','Tata Consultancy Services','Tata Steel International (Americas), Inc.','Taurus Holdings, Inc.','Taylor Morrison, Inc.','TD Bank, N.A.','TE Connectivity','Teal Drones']
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','website']};f.update(name=names[idx],ownership='Unknown',review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[src(d['official_url'],d['exact_official_excerpt'])]
 for x in d.get('sources',[]):
  if x.get('excerpt'):s.append(src(x['url'],x['excerpt']))
 if idx in [1,2,3,4,14,17,19]:f['ownership']='Subsidiary'
 if idx in [7,9,11,12,13]:f['ownership']='Public company'
 if idx==8:f['ownership']='Nonprofit'
 if idx==0:
  f.update(review_outcome='confirmed',ownership='Not applicable',kind='Represented-client filing label',description='Sullivan Strategies LLC acting on behalf of 3M, the technology and manufacturing company serving industrial, safety, transportation, electronics and consumer markets.');s=[src('https://lda.gov/filings/public/filing/4d98cc6e-57ca-4ad0-82e5-07ac2d4ebce9/print/','July 2026 registration explicitly identifies Sullivan Strategies LLC on behalf of 3M; both intermediary and represented company are retained.'),src('https://investors.3m.com/financials/sec-filings/content/0000066740-26-000246/mmm-20260630.htm','2026 issuer filing describes 3M continuing segments: Safety and Industrial, Transportation and Electronics, Consumer.')];f['notes']=f['identity_evidence']=s[0]['claim']
 if idx==5:f['website']='https://suniva.com/'
 if idx in [6,18]:f.update(review_outcome='partial',website_status='partial',ownership='Unknown')
 if idx==11:
  s=[src('https://www.sec.gov/Archives/edgar/data/1389170/000119312526059296/trgp-20251231.htm','2025 annual report identifies Targa Resources Corp. as publicly traded Delaware corporation (NYSE TRGP), operating midstream energy infrastructure.')];f['notes']=f['identity_evidence']=s[0]['claim']
 if idx==12:
  f['website']='https://tasekomines.com/';s.append(src('https://tasekomines.com/_resources/news/nr-20260430.pdf','April 2026 issuer release identifies Taseko Mines Limited and TSX, NYSE American and LSE listings.'))
 if idx==15:
  f.update(review_outcome='confirmed',ownership='Unknown',kind='Firearms business',description='U.S. Taurus firearms business identified as Taurus Holdings, Inc. in its official website privacy policy.');s=[src('https://www.taurususa.com/privacy-policy-2/','Official Taurus USA privacy policy explicitly names Taurus Holdings, Inc. as Taurus and the website operator; current ownership was not established by this source.')];f['notes']=f['identity_evidence']=s[0]['claim']
 if idx==17:
  s=[src('https://www.td.com/us/en/about-us/investor-relations','Current official page identifies TD Bank US Holding Company and its subsidiaries, including TD Bank, N.A., collectively as TD Bank U.S.')];f['notes']=f['identity_evidence']=s[0]['claim']
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes']))
(r/'featured86-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured86-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()))
