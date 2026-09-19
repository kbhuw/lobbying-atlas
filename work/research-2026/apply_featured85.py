import json,pathlib,datetime
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
rows=json.load(open(r/'featured85-first10.json'))+json.load(open(r/'featured85-middle10.json'))
extra={
2:[src('https://lda.gov/filings/public/filing/bcb05123-01e9-4947-9f61-e66ad4e52cdb/print/','2026 registration identifies State Farm at 1 State Farm Plaza, Bloomington, IL 61710, providing insurance.')],
3:[src('https://lda.gov/filings/public/filing/c2ed4b71-7fae-4dea-84c1-69470f1c2d7c/print/','Registration identifies State Farm Insurance Companies at One State Farm Plaza, Bloomington, IL 61710, providing insurance.')],
4:[src('https://lda.gov/filings/public/filing/e6b20039-1ad1-43ea-8df7-b1dd2a0615a7/print/','Registration uses generic State Farm Insurance Company at One State Farm Plaza A-3, Bloomington. Address connects it to State Farm but does not identify a specific insurer in the group.')],
5:[src('https://www.statefarm.com/simple-insights/insurance/what-is-a-mutual-insurance-company','Official explanation identifies State Farm Mutual as a mutual insurer with policyholder members.')],
11:[src('https://www.sec.gov/Archives/edgar/data/1013934/000110465918048548/a18-17787_18k.htm','August 2018 transaction filing states Strayer Education changed its name to Strategic Education. Capella survived the merger as a subsidiary; the filed Capella FKA is not a verified legal rename.')],
16:[src('https://www.studentsforlifeaction.org/supporters/','Official supporter page identifies Students for Life Action as a 501(c)(4) organization, separate from Students for Life of America.')],
17:[src('https://studentsforlife.org/supporters/','Official supporter page identifies Students for Life of America as a registered 501(c)(3) organization within the Pro-Life Generation family.')],
18:[src('https://www.studyfetch.com/legal/tos','August 16, 2026 official terms identify StudyFetch, Inc., registered in California at 345 N Maple Drive, Suite 340, Beverly Hills. This identifies the AI learning platform; promotional ranking claims are not adopted.')],
19:[src('https://suffolk.com/people/john-fish/','Official chairman biography identifies Suffolk as a national contractor and real-estate enterprise and explicitly describes it as privately held.')]
}
names=['Standard Chartered Bank','Starfish Space','State Farm (insurance group)','State Farm (insurance group)','State Farm Insurance Company (entity unspecified)','State Farm Mutual Automobile Insurance Company','State Street Bank and Trust Company','State Street Global Advisors Trust Company','STIIIZY, Inc.','Stillwater Mining Co. (reported DBA Sibanye-Stillwater)','Strand Therapeutics','Strategic Education (reported FKA Capella Education)','Strategy (formerly MicroStrategy)','Stride Health, Inc.','Strider Technologies','StubHub, Inc.','Students for Life Action','Students for Life of America','StudyFetch','Suffolk Construction']
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','website']};f.update(name=names[idx],ownership='Unknown',review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[src(d['official_url'],d['exact_official_excerpt'])]
 for x in d.get('sources',[]):
  if x.get('excerpt'):s.append(src(x['url'],x['excerpt']))
 s+=extra.get(idx,[])
 if idx in [0,6,7,15]:f['ownership']='Subsidiary'
 if idx in [2,3]:f.update(review_outcome='confirmed',ownership='Mutual insurance group',description='State Farm insurance group based in Bloomington, Illinois. This group-level reporting name covers its insurance businesses; the exact mutual insurer is listed separately.');s.append(src('https://newsroom.statefarm.com/2023-financial-results/','Official financial release identifies State Farm Mutual Automobile Insurance Company as parent of the State Farm family of companies.'))
 if idx==4:f.update(review_outcome='partial',website_status='partial',description='A State Farm insurance client reported under a generic company name. The registration matches the Bloomington headquarters, but the specific insurance entity is unresolved.')
 if idx==5:f.update(ownership='Cooperative',legal_form='Mutual insurance company',description='Policyholder-member mutual automobile insurer and parent of the State Farm family of insurance companies.')
 if idx==9:
  f['ownership']='Subsidiary';s=[src('https://www.sibanyestillwater.com/business/pgm-operations-americas/stillwater-east-boulder/','Current official operating page names Stillwater Mining Company and the 2017 acquisition. The filed DBA remains a reported label.'),src('https://reports.sibanyestillwater.com/2025/download/SSW-IR25.pdf','2025 integrated report identifies wholly owned subsidiary Stillwater Mining Company LLC. No listed-parent status is transferred to the U.S. mining entity.')];f['notes']=f['identity_evidence']='Current official operating page identifies the acquired Stillwater Mining Company business; 2025 report identifies wholly owned Stillwater Mining Company LLC. Filed Co. and DBA wording are retained as reported, without imposing a different suffix.'
 if idx==10:
  s=[src('https://www.strandtx.com/about','Official company page identifies the Boston programmable mRNA therapeutics business. The filed label has no legal suffix.')];f['notes']=f['identity_evidence']='Official company page establishes Strand Therapeutics and its mRNA therapeutics activity; ownership remains unknown.'
 if idx==11:f.update(review_outcome='partial',ownership='Unknown',website_status='partial',description='Lobbying label naming Strategic Education with a reported Capella former name. The corporate records show Capella became a subsidiary while Strayer was renamed Strategic Education; the label’s legal continuity is unresolved.')
 if idx==12:f['ownership']='Public company';f['notes']='Official issuer announcement documents the legal name change from MicroStrategy Incorporated to Strategy Inc effective August 11, 2025.';f['identity_evidence']=f['notes'];s=[src(d['official_url'],f['notes'])]
 if idx==15:f['website']='https://www.stubhub.com/'
 if idx in [16,17]:f.update(review_outcome='confirmed',ownership='Nonprofit',kind='Anti-abortion advocacy nonprofit');f['description']='Anti-abortion advocacy organization focused on legislation, elections and organizing; the 501(c)(4) partner of Students for Life of America.' if idx==16 else 'Anti-abortion education and organizing nonprofit working with students and communities; distinct from Students for Life Action.'
 if idx==18:f['review_outcome']='confirmed'
 if idx==19:f.update(review_outcome='confirmed',ownership='Private company')
 if idx in extra:f['notes']=' '.join(x['claim'] for x in extra[idx]);f['identity_evidence']=f['notes']
 if idx==0:f.update(logo_url='https://www.sc.com/en/uploads/sites/66/content/images/sc-lock-up-english-grey-rgb.png',logo_source_url='https://www.sc.com/en/media',logo_kind='logo',logo_status='official_site_asset',logo_background='light');s.append(src('https://www.sc.com/en/media','Official downloadable Standard Chartered brand logo fetched and visually verified.'))
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes']))
(r/'featured85-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured85-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
mfile=pathlib.Path('lobbying-map/research/verified-entity-merges.json');m=json.load(open(mfile));ids=['233fd7cfafd68e99','d79f18d1f6af6a06'];assert not any(set(ids)&set(x['source_ids']) for x in m)
claim='Consolidate the State Farm and State Farm Insurance Companies group-brand reporting labels. Both registrations identify insurance activity at One State Farm Plaza, Bloomington; the corporate financial release identifies the State Farm family of companies. Preserve group-level scope, all source reports, and the separate exact mutual insurer and ambiguous singular-company records.'
m.append(dict(canonical_id=ids[0],source_ids=ids,rationale=claim,sources=[dict(url=x['url'],claim=x['claim']) for x in extra[2]+extra[3]]+[dict(url='https://newsroom.statefarm.com/2023-financial-results/',claim='Identifies the State Farm family of companies and its mutual parent.')],reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()));mfile.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()),'merges',len(m))
