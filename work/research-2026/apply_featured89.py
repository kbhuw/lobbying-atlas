import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
assert not (r/'featured89-before.json').exists()
rows=json.load(open(r/'featured89-first10.json'))+json.load(open(r/'featured89-middle10.json'))
names=['The GEO Group (reported client history)','The Hartford Insurance Group (formerly Hartford Financial Services Group)','The Henry Ford','The Hertz Corporation','The Home Depot','Institute of Electrical and Electronics Engineers (IEEE)','Reflection AI (via The Livingston Group)','The Lubrizol Corporation','Sevita (formerly The MENTOR Network)','The MITRE Corporation','The Mosaic Company','The North American Coal Corporation','Northwestern Mutual Life Insurance Company','The Nuclear Company','Delek US (via The Picard Group)','President and Trustees of Williams College','The Rainey Center Freedom Project','Regents of the University of Michigan','Nova Minerals (via The Roosevelt Group)','Serco Inc. (via The Roosevelt Group)']
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
obo={6:('The Livingston Group','Reflection AI, Inc.','67ff6eca-c504-4d84-b4bc-eba51757ddb2'),14:('The Picard Group, LLC','Delek US Holdings, Inc.','3cb0161a-b3dd-4554-9f57-6243dec6ed35'),18:('The Roosevelt Group','Nova Minerals Limited','b04f6a52-6d3a-4562-9791-d23694f37115'),19:('The Roosevelt Group','Serco Inc.','3ce578dd-d7c0-470e-813c-8c3b46376290')}
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','website']};f.update(name=names[idx],ownership='Unknown',review_outcome='confirmed',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[src(d['official_url'],d['exact_official_excerpt'])]
 for x in d.get('sources',[]):
  if x.get('excerpt'):s.append(src(x['url'],x['excerpt']))
 if idx in [0,1,4,10]:f['ownership']='Public company'
 if idx in [3,7]:f['ownership']='Subsidiary'
 if idx in [2,5,9,15]:f['ownership']='Nonprofit'
 if idx==17:f['ownership']='Government body'
 if idx==12:
  f.update(ownership='Cooperative',legal_form='Mutual insurance company');s.append(src('https://www.northwesternmutual.com/life-and-money/what-is-a-mutual-insurance-company/','Northwestern Mutual explains that it is a mutual insurance company owned by policyholders, without shareholders.'))
 if idx==0:
  s=[src('https://lda.gov/filings/public/filing/ebff56f8-a5dd-489f-af0f-f2aec95b3326/print/','Original registration identifies The GEO Group, Inc. at its Boca Raton address, providing correctional and detention management services.'),src('https://lda.gov/filings/public/filing/2619142d-8788-4541-ae01-02582fc5d527/print/','2026 report retains GEO client name with a parenthetical former Capitol Counsel on-behalf-of label.'),src('https://investors.geogroup.com/static-files/1f07849f-9af5-4d49-9b1d-484eda283140','2025 annual report identifies The GEO Group, Inc., NYSE GEO.')];f['notes']=f['identity_evidence']='Registration and 2026 report establish GEO as the represented company. The Capitol Counsel parenthetical records client-label history, not a corporate rename of Capitol Counsel into GEO.'
 if idx==1:s=[src('https://www.sec.gov/Archives/edgar/data/874766/000087476625000016/hig-20250206.htm','February 6, 2025 SEC 8-K documents the legal name change from The Hartford Financial Services Group, Inc. to The Hartford Insurance Group, Inc.')]
 if idx==2:s.append(src('https://www.thehenryford.org/about-thf/impact-partners','The Henry Ford explicitly identifies itself as a registered 501(c)(3) nonprofit organization.'))
 if idx==4:s=[src('https://ir.homedepot.com/investor-resources/investor-documents','Current official investor page identifies The Home Depot, Inc., its home improvement retail business and NYSE HD listing.')]
 if idx==11:
  f.update(review_outcome='partial',ownership='Unknown',website_status='partial');f['notes']=f['identity_evidence']='Historical exact corporation is established, but current NACCO disclosures distinguish NACCO Natural Resources Corporation from North American Coal, LLC. Current legal-name continuity is under review; do not substitute the LLC for the filed corporation.';s.append(src('https://www.sec.gov/Archives/edgar/data/789933/000078993321000061/ex101-pncxnorthamericancoa.htm','2021 credit agreement directly names The North American Coal Corporation, a Delaware corporation.'))
 if idx in obo:
  who,client,reg=obo[idx];f.update(ownership='Not applicable',kind='Represented-client filing label',description=f'{who} acting on behalf of {client}. '+({6:'Reflection AI develops artificial-intelligence systems.',14:'Delek operates refining and logistics businesses.',18:'Nova Minerals develops mineral projects in Alaska.',19:'Serco provides government services and engineering.'}[idx]));s.append(src(f'https://lda.gov/filings/public/filing/{reg}/print/',f'Original registration expressly identifies {who} on behalf of {client}.'));f['notes']=f['identity_evidence']='Original federal registration verifies the represented-client label. Preserve the intermediary and represented company separately; no corporate ownership relationship is implied.'
 if idx==18:s=[x for x in s if 'ThinkEquity' not in x['url']];s.append(src('https://www.sec.gov/Archives/edgar/data/1852551/000149315226003702/ex99-1.htm','January 2026 issuer release identifies Nova Minerals Limited and the Estelle gold and critical minerals project in Alaska.'))
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes']))
x=next(x for x in json.load(open(r/'featured89-logo-candidates.json'))['candidates'] if x['id']=='7db99db9facbfdea');p[x['id']].update(logo_url=x['asset_url'],logo_source_url=x['source_page'],logo_kind='logo',logo_status='official_site_asset',logo_background='light');p[x['id']]['sources'].append(src(x['source_page'],x['evidence']))
(r/'featured89-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured89-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()));print('Status changes',[(i,b.get('status'),p[i]['status']) for i,b in before.items() if b.get('status')!=p[i]['status']])
