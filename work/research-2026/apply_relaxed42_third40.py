import json,re,datetime
from pathlib import Path
p=Path('work/research-2026'); master=p/'reviewed.json';d=json.loads(master.read_text());c=json.loads((p/'relaxed-address-candidates42.json').read_text());a=json.loads((p/'relaxed-address42-agent-third40.json').read_text())
accept={72,76,78,84,88,89,90,94,95,97,99,101,106,109}; backup={};audit=[];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for i,r in enumerate(a,70):
 assert r['id']==c[i]['id'];m=c[i]['matches'][0];reg=m['registration'];rec={'id':r['id'],'index':i,'decision':'hold','agent_evidence':r,'registration':reg}
 if i not in accept:
  rec['reason']='Exact legal counterparty, conflicting entity scope, or missing source wording needs further evidence.';audit.append(rec);continue
 old=d[r['id']];assert old['review_outcome']!='confirmed';backup[r['id']]=dict(old)
 url=r['url'];cache=json.loads(Path(r['cache']).read_text());pg=next(x for x in cache['pages'] if x['url']==url);txt=re.sub(r'\s+',' ',pg['text']);quote=r['address_quote']
 if i==84:quote='150 South Front Street, Suite 220 Columbus, OH 43215'
 assert re.sub(r'\s+',' ',quote).lower() in txt.lower(),(i,'address')
 assert re.sub(r'\s+',' ',r['legal_name_quote']).lower() in txt.lower(),(i,'name')
 claim=f"Official organization name and street/city corroborate the filed client {reg['client_name']}; registration {reg['archive']} member {reg['member']}. Website address: {quote}. Suite differences retained where present. This confirms organization identity, not a particular ownership category."
 old['review_outcome']='confirmed';old['website_status']='verified';old['status']='sourced';old['checked_at']=now;old['identity_evidence']=claim
 old['sources'] += [{'url':reg['source_url'],'label':'Original registration archive '+reg['member'],'claim':f"Filed client {reg['client_name']}; address {reg['address']}, {reg['city']}, {reg['state']}; reported activity: {reg['description']}."},{'url':url,'label':'Official organization identity and address','claim':claim}]
 if i==99:
  old['description']='Huntsville, Alabama aerospace company developing defense systems, autonomous aircraft and engineering technology.'
  old['notes']='Official site identifies Cummings Aerospace as a Native American woman-owned small business, with headquarters in Huntsville. Exact legal ownership structure is not established.'
 rec.update(decision='confirm',official_url=url,address_quote=quote,legal_name_quote=r['legal_name_quote']);audit.append(rec)
(p/'relaxed42-third40-before.json').write_text(json.dumps(backup,indent=2,ensure_ascii=False)+'\n');(p/'relaxed42-third40-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
master.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(d,ensure_ascii=False));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');print('Confirmed',len(backup),'held',len(audit)-len(backup))
