import json,datetime
from pathlib import Path
r=Path('work/research-2026');p=json.loads((r/'reviewed.json').read_text()); before={};dec=[]
for group in ['first10','middle10']:
 for x in json.loads((r/f'featured56-{group}-verified.json').read_text()):
  if x['decision']=='hold':continue
  i=x.get('id',x.get('originalID')); before[i]=json.loads(json.dumps(p[i]));a=p[i];patch=x.get('final_patch',x.get('proposed',{})).copy();patch.pop('aliases',None)
  ev=x['evidence']
  if i=='5c1e688ba2a5848e':
   patch['name']='Draiver (DriverDO LLC)';ev='Original registration explicitly names DriverDO LLC doing business as DRAIVER at 7900 College Blvd, Overland Park. Current official terms corroborate DRAIVER and that address and describe its vehicle-delivery marketplace, but spell the operator DraiverDO LLC. Preserve the filed legal spelling and disclose the discrepancy; no legal rename is inferred.'
  a.update(patch);a.update(review_outcome='confirmed',identity_evidence=ev,notes=ev,checked_at='2026-09-13',as_of='2026-09-13',website_status='verified',status='sourced')
  urls=[q['url'] for q in x.get('exact_quotes',[])]+[v for k,v in x.items() if k.endswith('_url')]
  for u in dict.fromkeys(urls):
   if u not in [s['url'] for s in a['sources']]:a['sources'].append(dict(url=u,label='Primary identity evidence',claim=ev))
  dec.append(dict(id=i,evidence=ev,patch=patch))
(r/'featured56-agent-root-before.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n');(r/'featured56-agent-root-decisions.json').write_text(json.dumps(dec,indent=2,ensure_ascii=False)+'\n')
for f,c in [(r/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:f.write_text(json.dumps(p,ensure_ascii=False,indent=None if c else 2)+('' if c else '\n'))
f=Path('lobbying-map/research/verified-entity-merges.json');m=json.loads(f.read_text());(r/'featured56-merges-before.json').write_text(json.dumps(m,indent=2)+'\n')
for canonical,other,reason,url in [('56c42fcf045a5703','217951c4b81d06f9','US agreement explicitly defines doTERRA International LLC as dōTERRA; original 2023 registration 301448318.xml names the LLC in the brand address field, and 2019 registration 301041769.xml matches the agreement Pleasant Grove address. Preserve all original filings and aliases; foreign affiliates remain separate.','https://media.doterra.com/us/en/forms/wellness-advocate-terms-and-conditions.pdf'),('a141bba7062e902d','188e2a8ac78e238e','Both original labels explicitly identify DPWN Holdings (USA) Inc.; the second adds a formerly-known-as parenthetical. Current DHL entity list confirms the exact corporation. Preserve the historical parenthetical as reported rather than independently asserting its rename date.','https://group.dhl.com/content/dam/deutschepostdhl/de/media-center/responsibility/dhl-group-konzerndatenschutzrichtlinie-anhang-3-uebersicht-konzerngesellschaften.pdf')]:
 assert not any(other in a['source_ids'] or canonical in a['source_ids'] for a in m)
 m.append(dict(canonical_id=canonical,source_ids=[canonical,other],rationale=reason,sources=[dict(url=url,claim=reason)],reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
f.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n');print('Saved',len(dec),'additional confirmations and 2 merges')
