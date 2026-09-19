import json,re,datetime
from pathlib import Path
p=Path('work/research-2026');f=p/'reviewed.json';d=json.loads(f.read_text());a=json.loads((p/'legal-pages44-reviewed.json').read_text());cs={r['id']:r for r in json.loads((p/'relaxed-address-candidates42.json').read_text())};before={};audit=[];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for r in a:
 id=r['id'];rec={'id':id,'decision':'hold'}
 if d[id]['review_outcome']=='confirmed':rec['decision']='already_confirmed';audit.append(rec);continue
 if id in ['12ee893e54bc5fb3','0d1635ad7190e2f1']:
  rec['reason']='Unbounded Inc/including match has no exact legal name evidence.' if id=='12ee893e54bc5fb3' else 'Office address appears under mixed Inc/GmbH labels; needs clearer entity address corroboration.';audit.append(rec);continue
 cache=json.loads((p/'legal-pages44'/f'{id}.json').read_text());url=r['official_url'];q=r['exact_legal_name_quote']
 if id=='623439e93690c392':url='https://www.humaneticsgroup.com/privacy-policy-gdpr';q='Humanetics Innovative Solutions Inc.'
 if id=='5c976cf5d3e5e663':q='Mikel Inc.'
 pg=next(x for x in cache['pages'] if x['url']==url);t=pg['text'];pat=r'(?<!\w)'+r'\W*'.join(map(re.escape,re.findall(r'\w+',q)))+r'(?!\w)';m=re.search(pat,t,re.I);assert m,(id,q)
 c=cs[id];reg=c['matches'][0]['registration'];addressurl=c['matches'][0]['page_url'];old=d[id];before[id]=dict(old)
 claim=f"Official source explicitly identifies {m.group(0)}. Corroborated against filed client {reg['client_name']} and street/city in {reg['archive']} member {reg['member']}. Ownership and parent relationships remain separately assessed."
 old.update(review_outcome='confirmed',website_status='verified',status='sourced',checked_at=now,identity_evidence=claim)
 old['sources'] += [{'url':reg['source_url'],'label':'Original registration archive '+reg['member'],'claim':f"Filed client {reg['client_name']}; address {reg['address']}, {reg['city']}, {reg['state']}; activity {reg['description']}."},{'url':url,'label':'Official legal entity identification','claim':claim},{'url':addressurl,'label':'Official organization address','claim':'Official website street and city corroborate the registration; suite differences retained.'}]
 rec.update(decision='confirm',official_url=url,legal_name_quote=m.group(0),context=t[max(0,m.start()-100):m.end()+250],registration=reg,address_url=addressurl);audit.append(rec)
(p/'legal44-before.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n');(p/'legal44-root-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');f.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(d,ensure_ascii=False));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');print('Confirmed',len(before))
