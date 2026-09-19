import json,datetime,collections
from pathlib import Path
w=Path('work/research-2026');p=json.load(open(w/'reviewed.json'));rs=json.load(open(w/'irs-followup-address-reviewed.json'));extras=[('89c27f01572cb340',3,'https://waihawarriors.org/contact','Official contact page states wAIHA Warriors is an IRS-recognized 501(c)(3) charitable organization.'),('351b147fee71e4ab',3,'https://barksdaleforward.org/about-barksdale-forward/','Official About page identifies Barksdale Forward as a 501(c)(3) nonprofit supporting Barksdale Air Force Base and its missions.'),('dd62b7d04ec334c7',6,'https://www.greetingcard.org/about-the-gca/','Official membership page explicitly identifies Greeting Card Association as a 501(c)(6) organization.'),('820a47cb9cc98985',4,'https://www.languagepolicy.org/our-story','Official history distinguishes NCLIS, a 501(c)(4) advocacy organization, from its sister JNCL, a 501(c)(3).')];ids=[r['id'] for r in rs]+[r[0] for r in extras];b=w/'irs-contact-followup-before.json'
if not b.exists():b.write_text(json.dumps({k:p[k] for k in ids},indent=2)+'\n')
for x in rs:
 k=x['id'];r=p[k];e=x['irs'];ein=e['EIN'];sub=int(e['SUBSECTION']);r.update(ownership='Nonprofit',legal_form=f'501(c)({sub}) nonprofit',review_outcome='confirmed',checked_at='2026-09-09',notes=f'IRS August 11, 2026 data identifies {e["NAME"]}, EIN {ein[:2]}-{ein[2:]}, under section 501(c)({sub}). Its official Contact page corroborates the organization name and street address in {e["CITY"]}, {e["STATE"]}.')
 if k=='7d774f1096cfaa7d':r['notes']+=' This is the EB-5 investor alliance, separate from the American Immigration Lawyers Association.'
 sources=[{'url':x['source_url'],'label':'IRS exempt organizations data — August 11, 2026','claim':f'Exact original CSV row: {e["NAME"]}; EIN {ein}; address {e["STREET"]}, {e["CITY"]} {e["STATE"]}; status {e["STATUS"]}; subsection {e["SUBSECTION"]}.'},{'url':x['resolved_url'],'label':'Official organization address','claim':'Official organization name and street address corroborate the IRS identity; punctuation and postal abbreviations differ.'}]
 for s in sources:
  if s not in r['sources']:r['sources'].append(s)
for k,sub,url,claim in extras:
 r=p[k];r.update(ownership='Nonprofit',legal_form=f'501(c)({sub}) nonprofit',checked_at='2026-09-09',notes=claim)
 if k=='351b147fee71e4ab':r['notes']+=' Original filing context remains qualified; tax classification does not resolve that separate issue.'
 else:r['review_outcome']='confirmed'
 s={'url':url,'label':'Official tax-status statement','claim':claim}
 if s not in r['sources']:r['sources'].append(s)
for path,c in [(w/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:path.write_text(json.dumps(p,ensure_ascii=False,**({'separators':(',',':')} if c else {'indent':2}))+'\n')
f=w/'publication.json';pub=json.load(open(f));pub={k:v for k,v in pub.items() if not k.startswith('pending_')};pub.update(local_changes_pending=True,pending_source_pushed=False,pending_change_summary='15 nonprofit classifications supported by official Contact/About pages and IRS records');f.write_text(json.dumps(pub,indent=2)+'\n');f=w/'full-corpus-coverage-audit.json';a=json.load(open(f));a.update(as_of=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication=pub,publication_stage='local_changes_pending',local_changes_pending=True)
for key,field in [('outcomes','review_outcome'),('websites','website_status'),('logos','logo_status'),('ownership','ownership')]:a[key]=dict(collections.Counter(v.get(field,'Unknown') for v in p.values()))
f.write_text(json.dumps(a,indent=2)+'\n');print(a['outcomes'])
