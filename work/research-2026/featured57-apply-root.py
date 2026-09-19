import json
from pathlib import Path
r=Path('work/research-2026');p=json.loads((r/'reviewed.json').read_text());before={};dec=[]
def apply(i,patch,ev,urls):
 before[i]=json.loads(json.dumps(p[i]));a=p[i];a.update(patch);a.update(review_outcome='confirmed',identity_evidence=ev,notes=ev,checked_at='2026-09-13',as_of='2026-09-13',website_status='verified',status='sourced')
 for u in dict.fromkeys(urls):
  if u not in [s['url'] for s in a['sources']]:a['sources'].append(dict(url=u,label='Primary identity evidence',claim=ev))
 dec.append(dict(id=i,patch=patch,evidence=ev,urls=urls))
for x in json.loads((r/'featured57-first10.json').read_text()):
 if x['decision']!='confirm' or x['originalID']=='44787b57fac62726':continue
 patch=x['proposed'];
 if x['originalID']=='89615a9fd3008b2a':patch['description']='Manufactures commercial printing equipment, advanced materials and chemicals.'
 apply(x['originalID'],patch,x['evidence'],[q['url'] for q in x['exact_quotes']])
original={x['id']:x for x in json.loads((r/'featured57-middle10.json').read_text())}
for x in json.loads((r/'featured57-middle10-verified.json').read_text()):
 if x['decision']=='hold':continue
 i=x['id'];patch=original[i]['proposed'].copy();patch.update(x['final_patch']);ev=x['evidence']
 if i in ['4277c6c367a7ba6f','0ec4e054d2b36668']:
  patch['ownership']='Unknown';ev+=' Ownership for this specific filed organization is not independently established; no public-parent status is transferred.'
 if i=='0ec4e054d2b36668':ev+=' The applicant policy dates to May 2018 and supports historical legal identity.'
 apply(i,patch,ev,[v for k,v in x.items() if k.endswith('_url')])
for x in json.loads((r/'featured57-last10-verified.json').read_text()):
 if x['id'] not in ['a61660bc0c740846','48f0a9d4babd377f','876ea335540426ab','2191dc2e76f30cdb']:continue
 patch={k:x[k] for k in ['name','description','website','kind']};patch['ownership']='Unknown'
 apply(x['id'],patch,x['exact_official_excerpt']+' Confirmed at the filed name scope; no legal continuity between distinct entities or current ownership is inferred.',x['source_urls'])
apply('cc02a88da2879c14',dict(ownership='Subsidiary of Duke Energy Corporation',legal_form='LLC'),'Duke Energy 2025 subsidiary exhibit names Duke Energy Business Services LLC (Delaware) among entities at least 50% owned as of December 31, 2025. Exact legal identity and dated parent relationship are established.',['https://www.sec.gov/Archives/edgar/data/20290/000132616026000014/duk-20251231x10kxexx21.htm'])
apply('9585c3603eb0b474',dict(description='Dubai-based airline operating international passenger and cargo flights.',kind='Airline',ownership='Unknown',logo_url='https://c.ekstatic.net/ecl/logos/emirates/emirates-logo-badge.svg',logo_source_url='https://www.emirates.com/',logo_kind='logo',logo_status='official_site_asset',logo_background='dark'),'Official Emirates About page identifies its Dubai hub and airline operations, matching the original Emirates Airline client and reported activity. Ownership remains unverified in this review. Official-site logo asset fetched and visually checked.',['https://www.emirates.com/english/about-us/'])
(r/'featured57-root-before.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n');(r/'featured57-root-decisions.json').write_text(json.dumps(dec,indent=2,ensure_ascii=False)+'\n')
for f,c in [(r/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:f.write_text(json.dumps(p,ensure_ascii=False,indent=None if c else 2)+('' if c else '\n'))
print('Saved',len(dec),'identity confirmations and Emirates logo')
