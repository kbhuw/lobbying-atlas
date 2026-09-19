import json,pathlib,copy,collections
root=pathlib.Path(__file__).resolve().parents[2];base=root/'work/research-2026/transport-recovery43';path=root/'work/research-2026/reviewed.json';p=json.loads(path.read_text());m=json.loads((base/'matches.json').read_text());holds={31:'Filed Radiant Industries Inc differs from official Radiant Inc; no continuity link.',34:'Rocket Companies Inc does not establish Rocket Limited Partnership.',40:'Stephens group page does not identify Shared Services LLC.',41:'Superior Essex group page does not identify exact International Inc entity.',51:'PS operating brand does not establish Private Suite LAX LLC.',58:'Exact Saltchuk Resources Inc legal identity not established by cached group pages.'};decisions=[];backup={}
for i in range(31,62):
 x=m[i];id=x['id'];profile=p[id];backup[id]=copy.deepcopy(profile);a=x['matches'][0];r=a['registration'];proof=f"Official organization name, activity and address corroborate the registration: {r['client_name']}, {r['address']}, {r['city']}, {r['state']}. Source: {r['archive']} / {r['member']}.";decision={'id':id,'decision':'hold' if i in holds else 'confirm','evidence':holds.get(i,proof),'url':a['page_url']};decisions.append(decision)
 if i in holds:continue
 assert profile['review_outcome']=='partial'
 profile.update(status='sourced',review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12');old=profile.get('identity_evidence','');profile['identity_evidence']=(old if isinstance(old,str) else json.dumps(old))+' '+proof
 profile['sources'] += [{'url':a['page_url'],'label':'Official identity and registration-address corroboration','claim':proof},{'url':r['source_url'],'label':'House registration archive: '+r['member'],'claim':proof}]

(base/'local31-before.json').write_text(json.dumps(backup,indent=2,ensure_ascii=False));(base/'local31-decisions.json').write_text(json.dumps(decisions,indent=2,ensure_ascii=False))
for f,pretty in [(path,True),(root/'lobbying-map/research/reviewed-2026.json',False),(root/'outputs/2026-research-trial/profiles.json',True)]:f.write_text(json.dumps(p,indent=2 if pretty else None,ensure_ascii=False))
print(collections.Counter(d['decision'] for d in decisions))
