import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
assert not (r/'featured87-before.json').exists()
rows=json.load(open(r/'featured87-first10.json'))+json.load(open(r/'featured87-middle10.json'))
names=['Teamworks','Technosylva','TechUnited:NJ','TekniPlex','TELACU Industries','Teleperformance Group, Inc.','Telephone and Data Systems, Inc.','TelevisaUnivision, Inc.','Telix Pharmaceuticals US','Telix Pharmaceuticals, Inc.','Telnyx','Tempus AI (formerly Tempus Labs)','Tenable, Inc.','Tencent America LLC','Tenet Business Services Corporation','Tenet Healthcare','Tenstorrent, Inc.','Teradata Government Systems LLC','Terawatt Infrastructure','Terra-Gen Power']
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','website']};f.update(name=names[idx],ownership='Unknown',review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[src(d['official_url'],d['exact_official_excerpt'])]
 for x in d.get('sources',[]):
  if x.get('excerpt'):s.append(src(x['url'],x['excerpt']))
 if idx in [5,8,12,14,17]:f['ownership']='Subsidiary'
 if idx in [6,11,15]:f['ownership']='Public company'
 if idx in [4,9,19]:f['website_status']='partial'
 if idx==0:f['description']='Provides software for collegiate and professional sports teams to manage athletes, staff and daily operations.'
 if idx==2:f.update(description='New Jersey technology community connecting entrepreneurs, companies, investors, policymakers and students.',kind='Technology membership organization');f['notes']+=' Tax-exempt status has not been independently established.'
 if idx==11:f['website']='https://www.tempus.com/'
 if idx==12:s=[src('https://www.sec.gov/Archives/edgar/data/1660280/000166028026000005/tenb-20251231.htm','2025 Form 10-K records the wholly owned subsidiary renamed Tenable, Inc. in 2017; public issuer is Tenable Holdings, Inc.')];f['notes']=f['identity_evidence']=s[0]['claim']
 if idx==13:
  f.update(review_outcome='confirmed',website='https://multimedia.tencent.com/',description='U.S. Tencent technology business identified as the developer and operator of the Tencent Media Lab website.',ownership='Unknown');s=[src('https://multimedia.tencent.com/en/privacy/','Official February 2021 Media Lab privacy policy names Tencent America LLC as website developer and data controller at 2747 Park Blvd, Palo Alto, CA 94306. Exact current ownership is not established by this policy.')];f['notes']=f['identity_evidence']=s[0]['claim']
 if idx==16:s=[src('https://tenstorrent.com/newsroom/rapidus-and-tenstorrent-partner-to-accelerate-development-of-ai-edge-device-domain-based-on-2nm-logi','Official November 2023 announcement identifies Tenstorrent Inc. and its AI computer and semiconductor development activity.')]
 if idx==19:
  s.append(src('https://lei.bloomberg.com/leis/view/5493005QIRJCOJYARG32','LEI issuer records Terra-Gen Power LLC as the previous legal name of TERRA-GEN, LLC, Delaware registration 5772950, renamed March 12, 2025. The source filing has not yet been linked to that registration number.'))
  f['notes']=f['identity_evidence']='Terra-Gen renewable-energy brand is established. A current LEI record documents a Terra-Gen Power LLC rename, but the filing-to-registration bridge remains unverified; do not assign the group parent ownership or merge records.'
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes']))
logos=json.load(open(r/'featured87-logo-candidates.json'))['candidates']
for x in logos:
 if x['id'] not in ['985c2ff6975a8a24','008c1276e32ab651','5990ba760f287172']:continue
 p[x['id']].update(logo_url=x['asset_url'],logo_source_url=x['source_page'],logo_kind='logo',logo_status='official_site_asset',logo_background='light')
 p[x['id']]['sources'].append(src(x['source_page'],x['evidence']))
(r/'featured87-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured87-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()));print('Status changes',[(i,b.get('status'),p[i]['status']) for i,b in before.items() if b.get('status')!=p[i]['status']])
