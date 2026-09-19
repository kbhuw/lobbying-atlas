import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));ids={x['id'] for x in json.load(open(r/'featured61-input.json'))[:20]};(r/'featured61-agents-before.json').write_text(json.dumps({i:p[i] for i in ids},indent=2)+'\n');dec=[]
def apply(i,patch,ev,urls):
 assert i in ids;p[i].update(patch);p[i].update(review_outcome='confirmed',website_status='verified',identity_evidence=ev,notes=ev,checked_at='2026-09-13',as_of='2026-09-13',status='sourced')
 for u in urls:
  if u not in [s['url'] for s in p[i]['sources']]:p[i]['sources'].append(dict(url=u,label='Primary organization evidence',claim=ev))
 dec.append(dict(id=i,decision='confirmed',evidence=ev,urls=urls))
for x in json.load(open(r/'featured61-first10.json')):
 i=x['originalID'];assert i in ids
 if x['decision']!='confirm':dec.append(dict(id=i,decision='hold',evidence=x['evidence']));continue
 apply(i,x['proposed'],x['evidence'],[s['url'] for s in x['exact_quotes']])
for x in json.load(open(r/'featured61-middle10.json')):
 i=x['id'];assert i in ids;patch={k:x[k] for k in ['description','website','kind']};patch['ownership']='Unknown';urls=[u for u in x['source_urls'] if 'lda.gov' not in u];ev='Original filing aliases compared with primary organization evidence. '+x['exact_official_excerpt']
 if i in ['2055ef915e24e37b','d03467c52eefcac1']:dec.append(dict(id=i,decision='hold',evidence='Parent/group or Canadian legal name does not resolve the filed client scope.'));continue
 if i=='420134e702061157':urls=['https://privacy.gsk.com/en-au/privacy-notice/candidate/'];ev='Official GSK candidate privacy notice explicitly names GlaxoSmithKline LLC as a data controller. Exact original LLC name confirmed; no public-parent ownership transfer.'
 if i=='a79602a5e5695d7f':urls=['https://glytec.com/wp-content/uploads/2025/02/Glytec-Command-Center-01-2025-web.pdf'];ev='Official 2025 Command Center product sheet explicitly names Glytec LLC and describes diabetes and insulin-management software; exact filed LLC matches. Current ownership unverified.'
 if i=='5b0bf3ebec9f1444':urls+=['https://www.gle-us.com/about-us/'];ev='Official About page names Global Laser Enrichment LLC. Current homepage states Silex Systems owns51% and Cameco49%. Exact filed LLC and enrichment activity match.';patch['ownership']='Joint venture: Silex Systems 51%; Cameco 49%'
 if i=='b22384766967a36b':urls=['https://globalmusicrights.com/privacypolicy'];ev='Official privacy policy explicitly names Global Music Rights LLC as website provider; original exact LLC identity and music licensing business match.'
 if i=='314a72cdce92f706':urls=['https://www.glydways.com/terms-and-conditions/'];ev='Official March26,2026 terms explicitly identify Glydways Inc. as website provider, matching exact filed corporation.'
 if i in ['c5cee807ded2248c','12c9a309af42a0dd']:urls=['https://www.gnc.com/learn/newsroom/gnc-fully-repays-152-million-second-lien-credit-facility-advancing-financial-flexibility.html'];ev='Official July21,2026 newsroom names GNC Holdings LLC and health/wellness activity. Original legal name matches; Doucet OBO intermediary wording remains intact where filed.'
 apply(i,patch,ev,urls)
(r/'featured61-agents-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f,c in [(r/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:f.write_text(json.dumps(p,ensure_ascii=False,indent=None if c else 2)+('' if c else '\n'))
print(sum(x['decision']=='confirmed' for x in dec),'confirmations')
