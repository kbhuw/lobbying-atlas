import json,pathlib,datetime
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
extra={
'c1092c4c705f0446':('https://group.softbank/en/segments/group','August 6, 2026 group-company list identifies SB Group US, Inc. as overseas investment management entity. Its own House registrant record 44445 reports DBA SoftBank Group US, Inc.; the external-firm filing uses the same DBA with Inc omitted from SB Group US.'),
'c28f97f206e45b52':('https://lobbyingdisclosure.house.gov/lookup.asp?reg_id=44445','Company self-registration identifies SB Group US, Inc. DBA SoftBank Group US, Inc.; independent official group list identifies SB Group US, Inc.'),
'17054b3b2ae59e20':('https://www.sandboxaq.com/legal/privacy-policy','August 1, 2026 official privacy notice explicitly identifies SB Technology, Inc. d/b/a SandboxAQ.'),
'652d29563c51f681':('https://selinc.com/company/privacy/','May 2026 official privacy policy identifies Schweitzer Engineering Laboratories, Inc. and affiliates.'),
'8cd337c3801f53b1':('https://investors.saic.com/sec-filings/sec-filing/10-k/0001571123-26-000029','Correct 2026 annual-report accession identifies Science Applications International Corp. The filing uses singular Application; the exact source-label bridge remains unresolved. Preliminary unverified SEC URL discarded.'),
'c290b6298e2f20b9':('https://www.seafarers.org/plans/','Official plans page expands AGLIW as Atlantic, Gulf, Lakes and Inland Waters, identifying this maritime union rather than the broader federation.'),
'1dcbede54a135f62':('https://www.seagate.com/legal/privacy/privacy-policy/','Official current privacy statement names Seagate Technology LLC and distinguishes parents, subsidiaries and affiliates; the filed LLC is not the listed Holdings plc.')}
rows=json.load(open(r/'featured82-first10.json'))+json.load(open(r/'featured82-middle10.json'));logos={x['id']:x for x in json.load(open(r/'featured82-logo-candidates.json')) if x['id'] in ['652d29563c51f681','4b9e00bf0586735c']}
names=['San Joaquin Regional Transit District','San Joaquin Valley Air Pollution Control District','San Juan Southern Paiute Tribe','San Luis & Delta-Mendota Water Authority','Sandoz Inc.','Sauk-Suiattle Indian Tribe','Sault Ste. Marie Tribe of Chippewa Indians','Savage Services Corporation','Savannah Airport Commission','Save the Manatee Club','SB Group US (reported DBA SoftBank Group US)','SB Group US, Inc. (reported DBA SoftBank Group US)','SandboxAQ (SB Technology, Inc.)','Schneider Electric','Schweitzer Engineering Laboratories','Science Application International Corporation','Science Corporation','Seafarers International Union — AGLIW','Seagate Technology LLC','SeatGeek']
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','ownership','website']};f.update(name=names[idx],review_outcome='confirmed',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[src(d['official_url'],d['exact_official_excerpt'])]
 if idx<10:
  for x in d.get('sources',[]):
   if x.get('excerpt'):s.append(src(x['url'],x['excerpt']))
 if i in extra:
  u,c=extra[i];s.append(src(u,c));f.update(notes=c,identity_evidence=c)
 if f['ownership'].startswith('Government body'):f['ownership']='Government body'
 if i=='b252ede97fc75396':f.update(ownership='Subsidiary',description='U.S. generic and biosimilar medicines company Sandoz Inc., a subsidiary of Sandoz Group AG. The Inc. entity is distinct from the listed parent.')
 if i=='6e094ee424afcb81':f['ownership']='Nonprofit'
 if i in ['c1092c4c705f0446','c28f97f206e45b52']:
  f['ownership']='Subsidiary';s.append(src('https://group.softbank/en/segments/group','Official August 2026 group list names SB Group US, Inc.; overseas investment management.'));s.append(src('https://lobbyingdisclosure.house.gov/lookup.asp?reg_id=44445','Company self-reported DBA preserved as reported legal-trade label, not a separately verified state DBA registration.'))
 if i=='4b5396be33b2652e':f['ownership']=before[i]['ownership']
 if i=='652d29563c51f681':f['ownership']='Employee-owned';s.append(src('https://selinc.com/company/about/','Official about page identifies 100% employee ownership through ESOP.'))
 if i=='8cd337c3801f53b1':f.update(review_outcome='partial',website_status='partial');s=[src(*extra[i])]
 if i=='c290b6298e2f20b9':f.update(ownership='Not applicable',description='Maritime labor union representing Atlantic, Gulf, Lakes and Inland Waters workers; part of the broader Seafarers International Union federation.')
 if i=='1dcbede54a135f62':
  f['ownership']='Subsidiary';s.append(src('https://www.sec.gov/Archives/edgar/data/1137789/000113778926000159/stx-20260703.htm','2026 annual report identifies Seagate Technology LLC among company subsidiaries in BIS settlement disclosure.'))
 if i in logos:
  x=logos[i];f.update(logo_url=x['asset_url'],logo_source_url=x['source_page'],logo_kind='logo',logo_status='official_site_asset',logo_background='dark' if i=='4b9e00bf0586735c' else 'light');s.append(src(x['source_page'],'Official standalone logo fetched and visually verified.'))
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes']))
(r/'featured82-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured82-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
mfile=pathlib.Path('lobbying-map/research/verified-entity-merges.json');m=json.load(open(mfile));ids=['c28f97f206e45b52','c1092c4c705f0446'];assert not any(set(ids)&set(x['source_ids']) for x in m)
claim='Self-filed House registrant44445 identifies SB Group US, Inc. DBA SoftBank Group US, Inc. External-firm client label omits Inc from SB Group US but retains the identical DBA; official corporate list identifies the U.S. entity. Consolidate naming variants, preserving source reports and self-reported DBA status.'
m.append(dict(canonical_id=ids[0],source_ids=ids,rationale=claim,sources=[dict(url='https://lobbyingdisclosure.house.gov/lookup.asp?reg_id=44445',claim=claim),dict(url='https://group.softbank/en/segments/group',claim='August2026 group list identifies SB Group US, Inc.'),dict(url='https://lda.gov/filings/public/filing/11ddae02-b0fc-480c-977d-1e6cbdcebd69/print/',claim='External-firm client label retains identical SoftBank Group US, Inc. DBA.')],reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()));mfile.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()),'merges',len(m))
