import json,datetime
from pathlib import Path
p=Path('work/research-2026');d=json.load(open(p/'reviewed.json')); inp=json.load(open(p/'featured65-input.json'));a=json.load(open(p/'featured65-first10.json'));assert {x['originalID'] for x in a}=={x['id'] for x in inp[:10]};out=[]
def update(i,u,e,**k):
 x=d[i];assert x['review_outcome']!='confirmed';x.update(review_outcome='confirmed',identity_evidence=e,notes=e,checked_at='2026-09-13',as_of='2026-09-13',website_status='verified',status='sourced',**k);x['sources']=[s for s in x.get('sources',[]) if s.get('label')=='Original lobbying disclosure']+[{'url':u,'label':'Primary identity evidence','claim':e}];out.append({'id':i,'url':u,'evidence':e,**k})
for x in a:
 i=x['originalID']
 if i=='f0b85e5f91744f02':continue # homepage brand alone does not prove Inc suffix
 k={z:x['proposed'][z] for z in ['kind','ownership','website']};update(i,x['exact_quotes'][0]['url'],x['evidence'],**k)
rows=[
('78e303f5e0ea4158','https://canoeprocurement.ca/wp-content/uploads/2023/11/Highland-Contract-051123-1.pdf','Company-signed 2023 Sourcewell proposal explicitly lists Highland Electric Fleets Inc., formerly Highland Electric Transportation Inc., website highlandfleets.com and 200 Cummings Center Suite 273D Beverly. This establishes the former-name bridge; project and operating subsidiaries remain distinct.','Unknown'),
('9a5161bec8f862b9','https://hifglobal.com/media/news-description/2026/07/01/leadership-transition-at-hif-emea','Official HIF Global announcement expands HIF as Highly Innovative Fuels and describes renewable fuels, matching the filed unsuffixed name and activity. This confirms brand identity, not a legal rename or ownership structure.','Unknown'),
('990af5fc10d62ba4','https://www.tampaairport.com/business/airport-administration','Official Tampa airport administration page explicitly identifies Hillsborough County Aviation Authority as responsible for daily operations of Tampa International Airport and three general aviation airports. Original authority name and airport parenthetical match.','Unknown'),
('2585ede17238100a','https://www.hillpointe.com/hillpointe-llc-raises-750-million/','Official March 5, 2025 announcement explicitly names Hillpointe LLC and its workforce-housing development and investment-management activities. Identity confirmed; fundraising does not establish private ownership classification.','Unknown'),
('5c794b84369547cb','https://investors.hgv.com/overview/','Official investor overview identifies Hilton Grand Vacations Inc., NYSE:HGV, and its timeshare business. It is kept distinct from Hilton Worldwide Holdings Inc.','Public company (NYSE: HGV)'),
('b9adfa78ff7460a9','https://syrairport.org/about-us/','Official airport About page names Syracuse Regional Airport Authority as a New York public benefit corporation operating Syracuse Hancock International Airport. The original OBO filing explicitly identifies this authority; Hill East Group LLC remains the intermediary. Website and description concern the represented authority, not the lobbying firm.','Public benefit corporation (represented authority)')]
for i,u,e,o in rows:update(i,u,e,ownership=o)
d['b9adfa78ff7460a9']['website']='https://syrairport.org/'
d['9a5161bec8f862b9']['description']='HIF Global develops renewable synthetic fuels; HIF stands for Highly Innovative Fuels. The filing uses the expanded brand name.'
d['78e303f5e0ea4158']['description']='Former name of Highland Electric Fleets, a business providing electric school buses, charging infrastructure and fleet operations services.'
(p/'featured65-rest-decisions.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
for f,indent,nl in [(p/'reviewed.json',2,True),(Path('lobbying-map/research/reviewed-2026.json'),None,False),(Path('outputs/2026-research-trial/profiles.json'),2,True)]:f.write_text(json.dumps(d,ensure_ascii=False,indent=indent)+ ('\n' if nl else ''))
mf=Path('lobbying-map/research/verified-entity-merges.json');m=json.load(open(mf));ids=['8261ddfa47e9ca00','78e303f5e0ea4158'];assert not set(ids)&{i for x in m for i in x['source_ids']};e=rows[0][2];m.append({'canonical_id':ids[0],'source_ids':ids,'rationale':e,'sources':[{'url':rows[0][1],'claim':e}],'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});mf.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n');print('Additional confirmations',len(out),'total wave',len(out)+9)
