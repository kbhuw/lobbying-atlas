import json,pathlib,copy,datetime,gzip
w=pathlib.Path('work/research-2026');p=json.load(open(w/'reviewed.json'));a=json.load(open(w/'featured50-verified.json'));b={x['id']:x for x in json.load(gzip.open('lobbying-map/research/directory-base.json.gz','rt'))['companies']};q={x['id']:x for x in json.load(open(w/'registration-evidence-queue.json'))};s={}
for x in a:
 if x['name'].startswith('City'):
  s[x['id']]=(x['official_page_url'],x['evidence']+' Original reported aliases: '+', '.join(b[x['id']]['aliases'])+'.')
s['8145a2464502d4a2']=('https://www.kcmo.gov/home/','Official Kansas City Missouri government site identifies municipal services and 414 E.12th Street, matching registration.')
s['e75675ebce51f89a']=('https://www.phoenix.gov/','Official City of Phoenix Arizona website matches original CITY OF PHOENIX AZ filing identity. Corrected the prior website to phoenix.gov.')
s['ccc69caf27164711']=('https://www.sanjoseca.gov/your-government/departments-offices/office-of-the-city-manager/employee-relations/retirement/police-fire-department-retirement-plan','Official San Jose government page identifies City Hall at 200 East Santa Clara Street and city services, matching original municipal identity.')
s['260733aabf7f8986']=('https://www.miami.gov/Home','Official City of Miami government site identifies municipal departments and services, matching original City of Miami Florida filing.')
s['a9674ab070f39574']=('https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231xex211.htm','Chipotle 2025 SEC subsidiary exhibit explicitly lists CMG Strategy Co., LLC, matching original filed label CMG STRATEGY CO., LLC DBA CHIPOTLE MEXICAN GRILL, INC. Preserve the filed DBA label and separate the subsidiary from the parent.')
s['f55be7453a3cf9e3']=('https://cognition.com/legal/privacy-policy','Official March 2026 privacy notice identifies Cognition AI, Inc. as operator of Devin and Windsurf, matching original exact filing alias.')
for i in ['dd3375f3115db65b','999ddc36e9cd3988']:s[i]=('https://www.sec.gov/Archives/edgar/data/21665/000002166526000006/cl-20251231.htm','2025 SEC Form 10-K identifies Colgate-Palmolive Company and consumer-products operations. Original Colgate-Palmolive brand registration at 300 Park Avenue matches issuer headquarters; exact Company filing identifies same company.')
(w/'featured50-root-before.json').write_text(json.dumps({i:copy.deepcopy(p[i]) for i in s},indent=2,ensure_ascii=False)+'\n');audit=[]
for i,(u,e) in s.items():
 x=p[i];x.update(review_outcome='confirmed',website_status='verified',identity_evidence=e,checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat());x['sources'].append({'url':u,'label':'Verified primary identity','claim':e});audit.append({'id':i,'source':u,'evidence':e,'original_aliases':b[i]['aliases'],'registration_evidence':q.get(i,{}).get('evidence',[])})
 if i=='e75675ebce51f89a':x['website']='https://www.phoenix.gov/'
 if i=='a9674ab070f39574':x['ownership']='Subsidiary of public company'
(w/'featured50-root-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
for f,pretty in [(w/'reviewed.json',True),(pathlib.Path('lobbying-map/research/reviewed-2026.json'),False),(pathlib.Path('outputs/2026-research-trial/profiles.json'),True)]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2 if pretty else None)+('\n' if pretty else ''))
print('applied',len(s),'confirmed',sum(x.get('review_outcome')=='confirmed' for x in p.values()))
