import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'))
rows={
'de18c106fae2b481':('https://www.sec.gov/Archives/edgar/data/1520504/000129281426002559/R15.htm','The 2025 related-party note in SEC accession 0001292814-26-002559 explicitly states that CleanJoule changed its name to Cyclokinetics, Inc. on February 23, 2026. This exact passage was visible in the indexed SEC body reviewed September 14, 2026, resolving the earlier unverified rename; direct download still returned an SEC access page. The current company website independently describes advanced propellants for aerospace and defense. The investor’s related-party status and historical share purchase do not establish current controlling ownership.'),
'b721d4d2c9e42a6b':('https://www.currenthydro.com/about','The official About page identifies Current Hydro and its run-of-river hydropower development work. Its project pages and May 2026 environmental-assessment announcement describe proposed projects progressing toward licensing and construction. These are not treated as completed operating plants. Direct official About body and indexed project bodies reviewed September 14, 2026; ownership of the company remains unknown.'),
'59cb62a13036bd4f':('https://www.cyclopsdefense.com/','The indexed official website identifies Cyclops Defense as a manufacturer, systems integrator and defense/security services business, describing unmanned systems, surveillance, communications and maintenance capabilities. This corroborates the operating identity. Its certifications, network size and performance claims are not independently verified here. The existing privately-held label comes from the company’s own public profile, not an audited ownership register. Official indexed body reviewed September 14, 2026; direct site returned a JavaScript shell.')
}
b=r/'featured328-before.json';assert not b.exists();b.write_text(json.dumps({i:p[i] for i in rows},indent=2,ensure_ascii=False)+'\n')
for i,(u,n) in rows.items():
 p[i].update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-14',notes=n,identity_evidence=n)
 p[i]['sources'].append({'url':u,'label':'Primary organization evidence reviewed September 14, 2026','claim':n})
p['de18c106fae2b481'].update(legal_form='Corporation',logo_background='dark')
p['b721d4d2c9e42a6b'].update(description='Developer of run-of-river hydropower projects at existing dams. Its portfolio includes proposed projects undergoing design, licensing and environmental review.',kind='Hydropower developer',logo_background='dark')
p['59cb62a13036bd4f']['website']='https://www.cyclopsdefense.com/'
(r/'featured328-decisions.json').write_text(json.dumps({i:p[i] for i in rows},indent=2,ensure_ascii=False)+'\n');(r/'reviewed.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
print('Three identities confirmed, project-stage description corrected, two logo backgrounds fixed.')
