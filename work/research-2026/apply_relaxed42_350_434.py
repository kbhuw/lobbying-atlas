import json,re,datetime
from pathlib import Path
p=Path('work/research-2026'); master=p/'reviewed.json';d=json.loads(master.read_text());c=json.loads((p/'relaxed-address-candidates42.json').read_text());a=json.loads((p/'relaxed-address42-agent-350-434.json').read_text())
accept={353,355,359,360,368,373,380,387,388,389,391,392,395,398,400,403,407,409,410,415,416,419,423,424,427,431}; backup={};audit=[];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for r in a:
 i=r['original_index']
 assert r['id']==c[i]['id'];m=c[i]['matches'][0];reg=m['registration'];rec={'id':r['id'],'index':i,'decision':'hold','agent_evidence':r,'registration':reg}
 if i not in accept:
  rec['reason']='Exact legal counterparty, conflicting entity scope, or missing source wording needs further evidence.';audit.append(rec);continue
 old=d[r['id']];assert old['review_outcome']!='confirmed';backup[r['id']]=dict(old)
 url=r.get('address_url',r['url']);cache=json.loads(Path(r['cache']).read_text());pg=next(x for x in cache['pages'] if x['url']==url);txt=re.sub(r'\s+',' ',pg['text']);quote=r['address_quote']
 if i==84:quote='150 South Front Street, Suite 220 Columbus, OH 43215'
 assert re.sub(r'\s+',' ',quote).lower() in txt.lower(),(i,'address')
 legalurl=r.get('legal_name_url',r['url']);legaltxt=next(x['text'] for x in cache['pages'] if x['url']==legalurl)
 assert re.sub(r'\s+',' ',r['legal_name_quote']).lower() in re.sub(r'\s+',' ',legaltxt).lower(),(i,'name')
 if legalurl!=url:old['sources']=old['sources']+[{'url':legalurl,'label':'Official organization name','claim':'Official page identifies '+r['legal_name_quote']+'.'}]
 claim=f"Official organization name and street/city corroborate the filed client {reg['client_name']}; registration {reg['archive']} member {reg['member']}. Website address: {quote}. Suite differences retained where present. This confirms organization identity, not a particular ownership category."
 old['review_outcome']='confirmed';old['website_status']='verified';old['status']='sourced';old['checked_at']=now;old['identity_evidence']=claim
 old['sources'] += [{'url':reg['source_url'],'label':'Original registration archive '+reg['member'],'claim':f"Filed client {reg['client_name']}; address {reg['address']}, {reg['city']}, {reg['state']}; reported activity: {reg['description']}."},{'url':url,'label':'Official organization identity and address','claim':claim}]
 if i==99:
  old['description']='Huntsville, Alabama aerospace company developing defense systems, autonomous aircraft and engineering technology.'
  old['notes']='Official site identifies Cummings Aerospace as a Native American woman-owned small business, with headquarters in Huntsville. Exact legal ownership structure is not established.'
 rec.update(decision='confirm',official_url=url,address_quote=quote,legal_name_quote=r['legal_name_quote']);audit.append(rec)
(p/'relaxed42-350-434-before.json').write_text(json.dumps(backup,indent=2,ensure_ascii=False)+'\n');(p/'relaxed42-350-434-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
master.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(d,ensure_ascii=False));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');print('Confirmed',len(backup),'held',len(audit)-len(backup))
