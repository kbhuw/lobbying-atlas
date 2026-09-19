import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'))
chosen={275:['cfc0286aa36ba9f2','4a1108b4af5b5da8','cf45df967c27f5ec','3fa31f562c30ddd6','3ed96b006c65cf63','c2a4b43f09f3024a','81e4d64e66ebc894'],276:['12a40c9a5c2f60d2','4d1d3261bc841f0d','8e84fc2ebe29cf97','645ca1eb8fc41812'],277:['3a4026dd615a583c','00b9fa281428bcec','e34c8f1e833cfa48']};ids=sum(chosen.values(),[]);f=r/'featured279-before.json';assert not f.exists();f.write_text(json.dumps({i:p[i] for i in ids},indent=2,ensure_ascii=False)+'\n')
for n,selected in chosen.items():
 b=json.load(open(r/f'identity{n}-batch.json'))
 for x in b['records']:
  i=x['id']
  if i not in selected:continue
  q=p[i];q.update(description=x['description'],review_outcome='confirmed',checked_at='2026-09-14')
  note=x['recommendation']
  if note.startswith('Confirm '):note='The evidence supports '+note[8:]
  q['notes']=note+' Reviewed September 14, 2026; existing official-page caches were captured September 8 where indicated. Ownership has not been inferred from a legal suffix or brand.';q['identity_evidence']=q['notes']
  for s in x['sources']:
   if s.get('http_status') in [0,403] and 'full-body' not in s.get('retrieval_ref',''):continue
   if s.get('retrieval_method')=='web search result':continue
   q['sources'].append({'url':s['url'],'label':'Original registration evidence' if 'Registrations_XML' in s['url'] else 'Official organization evidence','claim':s['excerpt']})
# Strengthened exact legal names and current domains.
p['cf45df967c27f5ec'].update(website='https://ykkamericas.com/',website_status='verified',legal_form='Corporation')
p['3fa31f562c30ddd6'].update(website='https://www.ysginc.com/',website_status='verified',legal_form='Corporation')
p['3fa31f562c30ddd6']['notes']='The current official site names Yorktown Systems Group, Inc. and gives 350 Voyager Way, Suite 110, Huntsville, matching the registered training and mission-support business. The stale yorktownsystems.com domain was replaced. Ownership remains unknown; a LinkedIn search classification was not used as verified ownership.'
p['81e4d64e66ebc894'].update(website_status='verified',legal_form='LLC');p['81e4d64e66ebc894']['notes']='The official About page describes Zebra Recovery’s disaster and emergency services and explicitly names Zebra Recovery, LLC in its footer. This establishes the exact filed operating entity; the homepage access restriction does not prevent verification from the About page.'
p['c2a4b43f09f3024a']['notes']='The original registration names Zanskar Geothermal & Minerals and describes geothermal development. The official site describes the same distinctive geothermal business. Another filing includes Inc.; omission of that suffix is not itself evidence of a separate entity, but no legal merger is performed in this pass. Ownership remains unknown.'
p['3ed96b006c65cf63'].update(ownership='Subsidiary',legal_form='LLC');p['3ed96b006c65cf63']['notes']='Zai Lab Limited’s 2025 Form 10-K explicitly lists Zai Lab (US) LLC with 100% ownership and describes its U.S. business development, R&D, legal, compliance and communications functions. This establishes the exact subsidiary as reported for 2025; it is retained separately from the public parent. The prior investor-domain retrieval failure remains recorded.'
p['4d1d3261bc841f0d'].update(ownership='Nonprofit/tax-exempt',website_status='verified')
p['3a4026dd615a583c'].update(name='Zions Bancorporation, N.A.',website='https://zionsbancorp.com/about-us/company-info/default.aspx',website_status='verified',ownership='Publicly traded',legal_form='National bank')
p['00b9fa281428bcec'].update(website='https://zone5tech.com/',website_status='verified');p['00b9fa281428bcec']['notes']='The substantive operating website is zone5tech.com, which identifies Zone 5 Technologies and its unmanned-aircraft and counter-UAS products. The old zone5.tech launching-soon page was replaced. The filed name and San Luis Obispo location are retained; acquisition completion and ownership were not established in this pass.'
p['e34c8f1e833cfa48'].update(website='https://www.zipline.com/',website_status='verified',legal_form='Corporation')
for i in ids:p[i]['identity_evidence']=p[i]['notes']
for i,u,src in [('cf45df967c27f5ec','https://ykkamericas.com/wp-content/uploads/2026/06/new_ykk_logo_R_WB.png','https://ykkamericas.com/terms-of-use/'),('3fa31f562c30ddd6','https://www.ysginc.com/wp-content/themes/ysg/assets/images/logo.svg','https://www.ysginc.com/')]:
 p[i].update(logo_url=u,logo_kind='logo',logo_status='official_site_asset',logo_source_url=src);p[i]['sources'].append({'url':src,'label':'Official branding','claim':'Logo linked by the official site; retrieved and visually checked September 14, 2026.'})
p['cfc0286aa36ba9f2']['name']='DisposeRx, Inc. (represented by YC Consulting)';p['4a1108b4af5b5da8']['name']='Genentech, Inc. (represented by YC Consulting)'
(r/'featured279-decisions.json').write_text(json.dumps({i:p[i] for i in ids},indent=2,ensure_ascii=False)+'\n');(r/'reviewed.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');print('Saved',len(ids),'profiles with reviewed evidence and two official logos.')
