import json,re,datetime,collections,copy
from pathlib import Path
w=Path('work/research-2026');p=json.loads((w/'reviewed.json').read_text());before=copy.deepcopy(p)
for r in p.values():
 for f in ['notes','identity_evidence']:
  if not isinstance(r.get(f),str):continue
  s=r[f];s=re.sub(r'\ballowed ownership (?:categories|category|classes|class|classification|labels)\b','ownership status',s);s=s.replace('permitted ownership category','ownership status');r[f]=s
updates=[
('dd49828a1f18ed5e','Publicly traded','Nextpower’s official investor FAQ identifies it as formerly Nextracker and states that its shares trade on Nasdaq under NXT.','https://investors.nextpower.com/resources/investor-faqs/default.aspx'),
('041479e05df89b93','Joint venture','Mitsubishi Electric Trane HVAC US is a 50/50 joint venture of Mitsubishi Electric and Trane Technologies, established in 2018.','https://www.mitsubishicomfort.com/about-us'),
('d4abcd27d6a57663','Member-owned cooperative','Nex-Tech’s official history identifies Rural Telephone as a cooperative, records services to cooperative members, and links its current bylaws under the Rural Telephone d/b/a Nex-Tech name.','https://www.nex-tech.com/about/'),
('6be79bd02e8f3f98','Subsidiary','Yulista’s official careers page identifies Yulista Integrated Solutions LLC as wholly owned by Yulista Holding LLC. The group is owned by Calista Corporation, an Alaska Native Regional Corporation.','https://yulista.com/careers/')]
for k,own,claim,url in updates:
 r=p[k];r.update(ownership=own,review_outcome='confirmed',checked_at='2026-09-09',identity_evidence=claim,notes=claim);r['sources'].append({'url':url,'label':'Official ownership evidence','claim':claim})
changed={k:before[k] for k in p if before[k]!=p[k]};(w/'ownership-language-before.json').write_text(json.dumps(changed,indent=2)+'\n');(w/'ownership-language-decisions.json').write_text(json.dumps({'editorial_only_ids':[k for k in changed if k not in [u[0] for u in updates]],'primary_source_updates':updates},indent=2)+'\n')
for path,compact in [(w/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:path.write_text(json.dumps(p,ensure_ascii=False,**({'separators':(',',':')} if compact else {'indent':2}))+'\n')
pub=json.loads((w/'publication.json').read_text());pub={k:v for k,v in pub.items() if not k.startswith('pending_')};pub.update(local_changes_pending=True,pending_source_pushed=False,pending_change_summary='Ownership wording cleanup and four source-backed classifications, plus pending GSMS and subsidiary corrections');(w/'publication.json').write_text(json.dumps(pub,indent=2)+'\n');a=json.loads((w/'full-corpus-coverage-audit.json').read_text());a.update(as_of=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication=pub,publication_stage='local_changes_pending',local_changes_pending=True)
for key,field in [('outcomes','review_outcome'),('websites','website_status'),('logos','logo_status'),('ownership','ownership')]:a[key]=dict(collections.Counter(v.get(field,'Unknown') for v in p.values()))
(w/'full-corpus-coverage-audit.json').write_text(json.dumps(a,indent=2)+'\n');print('Updated profiles',len(changed),a['outcomes'])
