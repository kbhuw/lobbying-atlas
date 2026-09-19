import json,pathlib,datetime
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return {'url':u,'label':'Primary organization evidence','claim':c}
extra={
'1a75ddf2fd378a48':('https://investors.rxo.com/stock-info/default.aspx','Official investor page identifies NYSE RXO.'),
'ce9454bcb1c7c20c':('https://s29.q4cdn.com/690959130/files/doc_downloads/investor-fact-book/2016-Investor-Fact-Book.pdf','Company fact book confirms McGraw Hill Financial changed its name to S&P Global on April 27, 2016.'),
'2ce45a3186bf0d44':('https://scjohnson.com/en/faq','Official FAQ identifies SC Johnson as a private family company with no publicly held stock.'),
'0e51c4427709bcb6':('https://www.saab.com/globalassets/markets/usa/saab-grayling-qa_december_2024.pdf','Official December 2024 company Q&A identifies Saab, Inc. as U.S. subsidiary of Saab AB, headquartered in Syracuse.'),
'30ca03f7487576ac':('https://www.sec.gov/Archives/edgar/data/1831481/000201238326000716/0002012383-26-000716-index.htm','SEC Sable Offshore Corp. record matches 845 Texas Avenue Suite 2920 Houston address and oil/gas activity in the source registration; extra f in filed Offfshore retained as original spelling.'),
'4f0835100e63b0d9':('https://www.saildrone.com/forecast/terms','Official service terms identify Saildrone, Inc. as service provider.'),
'0bfa05e8ccfd9839':('https://www.multistate.us/contact','MultiState contact address matches combined filing at 1000 Wilson Blvd Suite 1800 Arlington. Original combined client wording does not establish a single company or explicit on-behalf-of relationship.'),
'd4031c8bc387b05b':('https://www.san.org/about-the-authority/','Official authority history identifies the independent agency established in 2003 to manage San Diego International Airport.'),
'b84842fb7dac038a':('https://www.sdcwa.org/about-us/history/','Official history identifies San Diego County Water Authority as a public agency created by California Legislature in 1944.'),
'd42159f9196363fe':('https://www.sandiegofoodbank.org/','Official homepage identifies Jacobs & Cushman San Diego Food Bank as a 501(c)(3) nonprofit.'),
'7f8d43708b4d331b':('https://sanfranciscobayferry.com/our-history/','Official history states WETA adopted San Francisco Bay Ferry as its consumer-facing agency brand in 2011.'),
'2585655b345ab640':('https://sanfranciscobayferry.com/our-history/','Official history states WETA adopted San Francisco Bay Ferry as its consumer-facing agency brand in 2011.')}
names=['RXO','S&P Global','SC Johnson','Saab, Inc.','Sable Offshore Corp.','Sacramento Municipal Utility District','Safari Club International','SAG-AFTRA','Saildrone','Samsara / MultiState Associates (combined filing)','San Diego Community College District','San Diego County','San Diego County Regional Airport Authority','San Diego County Water Authority','San Diego Food Bank','San Diego Metropolitan Transit System','San Diego Unified School District','San Francisco Bay Area Water Emergency Transportation Authority (WETA)','San Francisco Bay Ferry (WETA)','San Joaquin Regional Rail Commission']
rows=json.load(open(r/'featured81-first10.json'))+json.load(open(r/'featured81-middle10.json'))
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','ownership','website']};f.update(name=names[idx],review_outcome='confirmed',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[src(d['official_url'],d['exact_official_excerpt'])]
 if i in extra:
  u,c=extra[i];s.append(src(u,c));f.update(notes=c,identity_evidence=c)
 if idx>=10 and i!='d42159f9196363fe':f['ownership']='Government body'
 if i=='1a75ddf2fd378a48':f.update(ownership='Public company',kind='Freight brokerage and transportation company',description='Arranges freight transportation through brokerage, managed transportation, and related logistics services.')
 if i=='ce9454bcb1c7c20c':f.update(ownership=before[i]['ownership'],kind='Financial information and analytics company',description='Provides credit ratings, market benchmarks, financial data, and analytics; formerly named McGraw Hill Financial.')
 if i=='2ce45a3186bf0d44':f.update(ownership='Private company',kind='Household consumer products manufacturer',description='Family-owned maker of household cleaning, pest-control, storage, and other consumer products.')
 if i=='0e51c4427709bcb6':f.update(ownership='Subsidiary',kind='Defense and aerospace technology company',website='https://www.saab.com/markets/united-states',description='U.S. defense and aerospace business of Saab, supplying military technology and air-traffic systems. The filed Inc. entity is distinct from Swedish parent Saab AB.')
 if i=='30ca03f7487576ac':f.update(ownership=before[i]['ownership'],kind='Offshore oil and gas company',description='Houston-based oil and gas company focused on the Santa Ynez Unit offshore California. Filed with an extra f in Offfshore; address and activity match Sable Offshore Corp.')
 if i=='6e2ff9e2a6e6f46f':f.update(ownership='Government body',kind='Public electric utility',description='Community-owned electric utility serving Sacramento County and adjoining parts of Placer County.')
 if i=='764d3c467da43273':f.update(ownership='Not applicable',description='Labor union representing actors, broadcasters, recording artists, and other media professionals.')
 if i=='4f0835100e63b0d9':f.update(kind='Uncrewed maritime technology company',description='Designs and operates uncrewed surface vessels for ocean data collection, mapping, and maritime surveillance.')
 if i=='0bfa05e8ccfd9839':f.update(review_outcome='partial',website_status='partial',ownership='Unknown',kind='Combined lobbying client label',description='Combined filing naming Samsara, a connected-operations technology business, and MultiState Associates, a government-affairs firm. The exact relationship remains unresolved.')
 if i=='7f8d43708b4d331b':f['website']='https://sanfranciscobayferry.com/about-us/'
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append({'id':i,'decision':f['review_outcome'],'notes':f['notes']})
(r/'featured81-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured81-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
mfile=pathlib.Path('lobbying-map/research/verified-entity-merges.json');m=json.load(open(mfile));ids=['2585655b345ab640','7f8d43708b4d331b'];assert not any(set(ids)&set(x['source_ids']) for x in m)
claim='WETA official history explicitly identifies San Francisco Bay Ferry as the consumer-facing brand adopted for the agency in 2011; consolidate the authority and its brand, preserving both filing names and reports.'
m.append(dict(canonical_id=ids[0],source_ids=ids,rationale=claim,sources=[dict(url='https://sanfranciscobayferry.com/our-history/',claim=claim)],reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()));mfile.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed:',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()),'merges',len(m))
