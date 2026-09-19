import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
assert not (r/'featured91-before.json').exists()
rows=json.load(open(r/'featured91-first10.json'))+json.load(open(r/'featured91-middle10.json'))
names=['Eli Lilly and Company (via Tiber Creek Health Strategies)','TickPick, LLC','TidalHealth','Tiffany & Co.','TikTok Inc.','Tin Can Untechnologies, Inc.',"Tito’s Handmade Vodka / Fifth Generation, Inc.",'TNC (US) Holdings, Inc.','Tom James Company','Tools for Humanity Corporation','TOOTRiS, LLC','Top Aces Corp.','Topsoe A/S','Topsoe, Inc.','Torch Technologies, Inc.','Toshiba America, Inc.','Total Wine & More','TotalEnergies EP Mozambique Area 1','TotalEnergies Washington Office','TOTE Group']
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','website']};f.update(name=names[idx],ownership='Unknown',review_outcome='confirmed',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[src(d['official_url'],d['exact_official_excerpt'])]
 if idx==0:
  f.update(kind='Represented-client filing label',ownership='Not applicable');f['notes']='The 2026 federal filing expressly names Tiber Creek acting on behalf of Eli Lilly. The entry represents that disclosed relationship, not ownership between the organizations.';s=[src('https://lda.gov/filings/public/filing/eae4f114-691e-4a0c-ba03-6bf6a376cee9/print/',f['notes'])]
 if idx==2:
  f['ownership']='Nonprofit';f['notes']='Confirmed at healthcare-system scope. The original 2026 filing says FKA Nanticoke, Peninsula Health; official history describes formerly separate organizations now within TidalHealth. This is not evidence that all affiliate legal entities merged or changed legal names.';s += [src('https://www.tidalhealth.org/about-us/combined-care-system','Official history identifies the former regional system and Nanticoke hospital among the healthcare organizations now within TidalHealth.'),src('https://lda.gov/filings/public/filing/77480d3e-342f-419c-8463-75b70bf0e8a1/print/','2026 filing names TidalHealth with a filed historical reference to Nanticoke and Peninsula Health.'),src(d['sources'][-1]['url'],'Audited financial statements describe TidalHealth and its charitable affiliates as tax-exempt organizations.')]
 if idx==3:
  f.update(ownership='Subsidiary',description='Tiffany & Co. makes and sells jewelry, watches and luxury accessories. It is part of LVMH.');s=[src('https://www.lvmh.com/our-group/history','LVMH records its completed acquisition of Tiffany in 2021.'),src('https://www.lvmh.com/static/lettre-aux-actionnaires-juillet-2026/montres-et-joaillerie.html','July 2026 shareholder materials continue to include Tiffany within the group.')];f['notes']='LVMH acquisition and current group materials support subsidiary status. Preserve the filed Tiffany & Co. name without selecting a different operating subsidiary.'
 if idx==4:
  f['description']='TikTok Inc. is a legal entity associated with the TikTok video platform. It is distinct from TikTok USDS Joint Venture LLC.';f['notes']='The official August 2024 privacy policy identifies TikTok Inc. by exact name and US address. Its historical operator role is not treated as the current US service arrangement. The 2026 announcement names a separate USDS joint venture; its ownership percentages are not assigned to TikTok Inc.';s.append(src('https://www.tiktok.com/legal/page/us/privacy-policy/en?appLaunch=app','Official policy dated August 2024 names TikTok Inc. as the platform provider and gives its Culver City address. Historical identity evidence.'))
 if idx==6:
  f['description']='Fifth Generation, Inc. distills and bottles Tito’s Handmade Vodka in Austin, Texas.';f['notes']='Official purchasing terms identify Fifth Generation, Inc. as Titos. This verifies the company and brand relationship; the reversed DBA wording in the filing is preserved as filed, not endorsed as a legal statement.';s.append(src('https://www.titosvodka.com/distillery-tcs','Official purchasing terms identify Fifth Generation, Inc. as Titos.'))
 if idx==7:
  f.update(review_outcome='partial',website_status='partial');f['notes']='The exact holding entity appears in historical Nielsen records. Its current operational status and the filed former-name relationship remain unresolved; current ownership is unknown.'
 if idx in [8,12,16]:f['ownership']='Private company'
 if idx==11:f['notes']='Official contact directory names the exact US corporation and its Mesa address. Private ownership claims about the broader Top Aces group are not assigned to this entity without a direct bridge.'
 if idx==13:f['notes']='Official contact directory identifies the exact Inc. entity at multiple US locations. Identity and operating brand confirmed; direct corporate ownership left unknown.'
 if idx==14:
  f.update(ownership='Employee-owned',website='https://www.torchtechnologies.com/');s=[src(f['website'],'Official company site names Torch Technologies, Inc., describes its technical-services business, and states it is 100 percent employee-owned.')];f['notes']=s[0]['claim']
 if idx==15:
  f.update(ownership='Subsidiary',website='https://toshiba.com/tai/about-us/',description='Toshiba America, Inc. is Toshiba Corporation’s US holding company for businesses serving commercial, energy and industrial markets.');s=[src(f['website'],'Official about page identifies Toshiba America, Inc. as a Toshiba Corporation subsidiary and holding company for three US operating companies.')];f['notes']=s[0]['claim']
 if idx==16:
  s=[src('https://www.totalwine.com/site/binaries/content/assets/pdfs/weddings/0326_twm_weddings_booklet_web.pdf','Official 2026 publication describes Total Wine and More as still family-owned and its wine, beer and spirits retail business.')];f['notes']=s[0]['claim']
 if idx==17:
  f.update(ownership='Subsidiary',website='https://totalenergies.com/',description='TotalEnergies EP Mozambique Area 1 is the TotalEnergies subsidiary operating the Mozambique LNG development.');s=[src('https://totalenergies.com/newsroom/totalenergies-publishes-jcrufins-report-human-rights-cabo-delgado-together/?lang=eng','Official TotalEnergies publication names TotalEnergies EP Mozambique Area 1 Limitada as a wholly owned subsidiary and Mozambique LNG operator.')];f['notes']='Confirmed from the official parent publication. Project participation is distinct from ownership of the subsidiary. Removed a proposed non-resolving Mozambique website.'
 if idx==18:
  f.update(kind='Regional representative office',ownership='Not applicable');s=[src('https://jobs.totalenergies.com/en_US/careers/JobDetail/Government-Affairs-Specialist/70669?jobId=70669','Official careers posting describes the TotalEnergies Washington DC office and its government and public affairs work.')];f['notes']='Confirmed at representative-office scope. Retain the filed former name as reported history; no separately incorporated Washington entity or legal rename is asserted.'
 if idx==19:
  f.update(review_outcome='partial',website_status='partial');s=[src('https://totegroup.com/about/','Official site describes TOTE Group as TOTE, LLC, in the Saltchuk family of businesses.')];f['notes']='The group website explicitly uses TOTE, LLC, whereas the filing says TOTE Group, LLC. Brand and activity identified, but an exact legal-entity bridge is still needed. No merge or ownership transfer based only on the brand.'
 f['identity_evidence']=f['notes'];p[i].update(f)
 # Replace claims for URLs reviewed here; retain other historical evidence.
 byurl={x['url']:x for x in p[i].get('sources',[])}
 for x in s:byurl[x['url']]=x
 if idx==17:byurl={u:x for u,x in byurl.items() if 'corporate.totalenergies.mz' not in u}
 p[i]['sources']=list(byurl.values());dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes']))
logos=json.load(open(r/'featured91-logo-candidates.json'))['candidates']
for d in logos:
 if d['id'] in ['832c4afd1cd30207','32d8c0e7969809aa','d7dbdaefc5b3f9eb']:
  p[d['id']].update(logo_url=d['asset_url'].replace('http:','https:'),logo_source_url=d['source_page'],logo_kind='logo',logo_status='official_site_asset',logo_background='light')
(r/'featured91-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured91-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()));print('Status changes',[(i,b.get('status'),p[i]['status']) for i,b in before.items() if b.get('status')!=p[i]['status']])
