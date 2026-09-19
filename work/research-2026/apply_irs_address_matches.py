import json,datetime,collections
from pathlib import Path
w=Path('work/research-2026');p=json.loads((w/'reviewed.json').read_text());rs=json.loads((w/'irs-address-reviewed-decisions.json').read_text());b=w/'irs-address-before.json'
if not b.exists():b.write_text(json.dumps({r['id']:p[r['id']] for r in rs},indent=2)+'\n')
qualifications={
'dee91f8b5e872db6':'This is the South Carolina university; the Indiana institution remains separate. Its logo remains unverified.',
'68194f4a3810fe90':'Any disclosed intermediary and represented principal remain explicit in the original filings.',
'b17734615a10f676':'Separate from the American Society of Nephrology.',
'30685d7c7a1ae0b1':'Separate from affiliated state associations and industry councils.',
'991c345fcb8b38d8':'The IRS record is Coalition of EPSCoR States; continuity with every EPSCoR/IDeA filing name remains qualified.',
'1abbdbca5e5a9036':'This is the Browns Mills, New Jersey hospital; the unrelated d-h.org match was excluded.',
'281fe763234a484e':'The website and IRS record use Newton, Iowa. The reported Raleigh, North Carolina filing location remains unexplained.',
'1e9a124dbd30cd30':'Tax classification establishes nonprofit status; it does not establish the institute’s complete governance or parent relationships.',
'a6861a88e734c2d7':'Tax status and website identity are corroborated; earlier missing original-filing context remains a separate research qualification.',
'291653b0fae37950':'USA Rice Federation is the legal umbrella organization commonly called USA Rice. Its member associations remain separate.'}
keep_partial={'991c345fcb8b38d8','281fe763234a484e','a6861a88e734c2d7'}
changed=0
for x in rs:
 k=x['id'];v=p[k];e=x['irs'];ein=e['EIN'];sub=int(e['SUBSECTION']);note=f'IRS August 11, 2026 records identify {e["NAME"]}, EIN {ein[:2]}-{ein[2:]}, as section 501(c)({sub}) tax-exempt. The official site corroborates its name and street address in {e["CITY"]}, {e["STATE"]}.'
 if k in qualifications:note+=' '+qualifications[k]
 v.update(ownership='Nonprofit',legal_form=f'501(c)({sub}) nonprofit',checked_at='2026-09-09',notes=note)
 if k not in keep_partial:
  changed+=v['review_outcome']!='confirmed';v['review_outcome']='confirmed'
 sources=[{'url':x['source_url'],'label':'IRS exempt organizations data — August 11, 2026','claim':f'Original CSV row: EIN {ein}; {e["NAME"]}; {e["STREET"]}, {e["CITY"]} {e["STATE"]} {e["ZIP"]}; status {e["STATUS"]}; subsection {e["SUBSECTION"]}.'},{'url':x['website'],'label':'Official organization address','claim':'Organization name and address corroborate the IRS identity. Reviewed page address excerpt: '+x['excerpts'][0]}]
 for s in sources:
  if s not in v['sources']:v['sources'].append(s)
for path,c in [(w/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:path.write_text(json.dumps(p,ensure_ascii=False,**({'separators':(',',':')} if c else {'indent':2}))+'\n')
f=w/'publication.json';pub=json.loads(f.read_text());pub={k:v for k,v in pub.items() if not k.startswith('pending_')};pub.update(local_changes_pending=True,pending_source_pushed=False,pending_change_summary='49 IRS classifications corroborated with official organization names and addresses');f.write_text(json.dumps(pub,indent=2)+'\n');f=w/'full-corpus-coverage-audit.json';a=json.loads(f.read_text());a.update(as_of=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication=pub,publication_stage='local_changes_pending',local_changes_pending=True)
for key,field in [('outcomes','review_outcome'),('websites','website_status'),('logos','logo_status'),('ownership','ownership')]:a[key]=dict(collections.Counter(v.get(field,'Unknown') for v in p.values()))
f.write_text(json.dumps(a,indent=2)+'\n');print({'newly_confirmed':changed,'outcomes':a['outcomes']})
