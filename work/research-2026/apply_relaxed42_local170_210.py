import json,datetime,re
from pathlib import Path
p=Path('work/research-2026');f=p/'reviewed.json';d=json.loads(f.read_text());cs=json.loads((p/'relaxed-address-candidates42.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat();before={};audit=[]
accept={170,176,178,180,185,188,197,199,202,204,207};agent_ids={r['id'] for r in json.loads((p/'legal-pages44/matches.json').read_text())}
for i in range(170,210):
 c=cs[i];r=c['matches'][0]['registration'];url=c['matches'][0]['page_url'];rec={'id':c['id'],'index':i,'decision':'hold','registration':r,'url':url}
 if c['id'] in agent_ids:rec['decision']='delegated_legal44';audit.append(rec);continue
 if i not in accept:rec['reason']='Exact counterparty, represented scope, or source quality needs further primary evidence.';audit.append(rec);continue
 cache=json.loads(Path(c['cache']).read_text());texts=' '.join(pg.get('text','') for pg in cache['pages']);assert texts
 old=d[c['id']];assert old['review_outcome']!='confirmed';before[c['id']]=dict(old)
 claim=f"Official organization name, activity and street/city match the filed client {r['client_name']} in {r['archive']} member {r['member']}. Address-suite changes are retained; ownership is a separate field."
 if i==188:claim+=' The original registration explicitly identifies Veteran Benefits Guide as the DBA of JoshCo Group, LLC.'
 if i==199:claim+=' Official homepage explicitly states Learning Care Group is now Learning Care.'
 old.update(review_outcome='confirmed',website_status='verified',status='sourced',checked_at=now,identity_evidence=claim)
 old['sources'] += [{'url':r['source_url'],'label':'Original registration archive '+r['member'],'claim':f"Client {r['client_name']}; address {r['address']}, {r['city']}, {r['state']}; reported activity: {r['description']}."},{'url':url,'label':'Official identity and address','claim':claim}]
 if i==197:old['sources'].append({'url':'https://lasermarktech.com/contact/','label':'Official legal name and office list','claim':'Contact page names Laser Marking Technologies, LLC across its offices and identifies the Caro headquarters.'})
 if i==185:old['description']='Municipal airport authority serving Jackson, Mississippi, with airport operations, business facilities and aviation services.'
 rec['decision']='confirm';rec['evidence']=claim;audit.append(rec)
(p/'relaxed42-local170-210-before.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n');(p/'relaxed42-local170-210-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
f.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(d,ensure_ascii=False));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');print('Confirmed',len(before))
