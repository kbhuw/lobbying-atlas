import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));b=json.load(open(r/'featured322-before.json'))
rows=json.load(open(r/'identity321-batch.json'))['records']
claims={
'efaf2eb93283a1ee':'The official 2022–25 strategic plan identifies Concrete Masonry & Hardscapes Association and the unification of ICPI and NCMA. It describes industry education, certification, technical research and advocacy. Operating identity confirmed; no separate tax classification inferred.',
'd5dbbd262ceee583':'The official Condista website identifies its Spanish-language television distribution business, US and international portfolios, advertising services and Doral, Florida office. This corroborates the operating identity; a separate legal-suffix identity and equity ownership are not asserted.',
'6a5bf393cdb9d7c0':'The official ConductorAI website describes its Conduit platform for agentic document search, policy-driven review, approvals and redaction. This confirms the operating software-business identity. Performance and accreditation marketing claims are not independently verified or repeated as established facts; equity ownership remains unknown.',
'91436b8fcf03db30':'The official Para la Naturaleza donation page explicitly gives Puerto Rico Conservation Trust as its legal charitable recipient and EIN 66-0288581. This establishes the organization behind the conservation activity while preserving the distinction between the trust and the Para la Naturaleza program brand.',
'16beb462924ef8fe':'The official Consumer Access to Repair website identifies the CAR Coalition as independent auto-parts makers, insurers, retailers and groups advocating repair choice and vehicle-data access. Operating coalition identity confirmed. Its policy arguments and proposed legislation are not presented as enacted law; separate incorporation and tax classification remain unknown.'}
for q in rows:
 i=q['id'];assert i not in b;b[i]=p[i].copy();n=claims[i]+' Official body reviewed September 14, 2026.'
 p[i].update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-14',description=q['description'],notes=n,identity_evidence=n)
 p[i]['sources']=p[i]['sources']+[{'url':q['sources'][0]['url'],'label':'Official organization body reviewed September 14, 2026','claim':n}]
p['6a5bf393cdb9d7c0']['description']='Software company whose Conduit platform searches documents and helps teams review, redact and approve them against complex policies.'
p['d5dbbd262ceee583']['logo_background']='dark'
(r/'featured322-before.json').write_text(json.dumps(b,indent=2,ensure_ascii=False)+'\n')
(r/'reviewed.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');(r/'featured322-decisions.json').write_text(json.dumps({i:p[i] for i in b},indent=2,ensure_ascii=False)+'\n')
print('Five more operating identities corroborated; white Condista logo contrast fixed.')
