import json,datetime,collections
from pathlib import Path
w=Path('work/research-2026');p=json.loads((w/'reviewed.json').read_text());rs=json.loads((w/'irs-ownership-followup-decisions.json').read_text());b=w/'irs-ownership-followup-before.json'
if not b.exists():b.write_text(json.dumps({r['id']:p[r['id']] for r in rs},indent=2)+'\n')
for r in rs:
 k=r['id'];v=p[k];ein=r['ein'];sub=int(r['subsection']);match='Official website publishes or links its matching EIN.' if r.get('ein_matches') else 'Official website explicitly describes nonprofit status and gives the same city and street address as the IRS record.'
 note=f'IRS August 11, 2026 data lists {r["irs_name"]}, EIN {ein[:2]}-{ein[2:]}, under section 501(c)({sub}). {match}'
 if k=='b14ce3619852eee0':note+=' The website describes registrations in several countries; continuity with the exact lobbying client remains qualified.'
 v.update(ownership='Nonprofit',legal_form=f'501(c)({sub}) nonprofit',checked_at='2026-09-09',notes=note)
 if k!='b14ce3619852eee0':v['review_outcome']='confirmed'
 sources=[{'url':r['irs_record']['source_url'],'label':'IRS exempt organizations data — August 11, 2026','claim':f'Exact EIN {ein}; name {r["irs_name"]}; status 01; subsection {r["subsection"]}; address {r["irs_record"]["row"]["STREET"]}, {r["city"]} {r["state"]}.'},{'url':r['resolved_url'],'label':'Official identity and nonprofit evidence','claim':match}]
 for s in sources:
  if s not in v['sources']:v['sources'].append(s)
p['6766b15bfca08b05']['description']='Buckner International is a Christian nonprofit serving vulnerable children, families and older adults in the United States and internationally.'
for path,c in [(w/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:path.write_text(json.dumps(p,ensure_ascii=False,**({'separators':(',',':')} if c else {'indent':2}))+'\n')
f=w/'publication.json';pub=json.loads(f.read_text());pub={k:v for k,v in pub.items() if not k.startswith('pending_')};pub.update(local_changes_pending=True,pending_source_pushed=False,pending_change_summary='11 sourced nonprofit tax classifications plus earlier saved corrections awaiting publication');f.write_text(json.dumps(pub,indent=2)+'\n');f=w/'full-corpus-coverage-audit.json';a=json.loads(f.read_text());a.update(as_of=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication=pub,publication_stage='local_changes_pending',local_changes_pending=True)
for key,field in [('outcomes','review_outcome'),('websites','website_status'),('logos','logo_status'),('ownership','ownership')]:a[key]=dict(collections.Counter(v.get(field,'Unknown') for v in p.values()))
f.write_text(json.dumps(a,indent=2)+'\n');print(a['outcomes'])
