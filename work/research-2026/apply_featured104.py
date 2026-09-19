import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));rows=json.load(open(r/'featured104-first10.json'))+json.load(open(r/'featured104-middle10.json'));before={};dec=[];assert not (r/'featured104-before.json').exists()
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
benef=['Google Client Services LLC','ID.me, LLC','NASCAR','National Hockey League','United Parcel Service'];firms=['JGB & Associates, LLC','DiNino Associates, LLC','DiNino Associates, LLC','JGB & Associates, LLC','JGB & Associates, LLC']
for k,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f=dict(name=before[i]['name'],description=d['description'],kind=d['kind'],ownership=d['ownership'],review_outcome=d['decision'],notes=d['evidence'],website=d['website'],website_status='verified' if d['website'] else 'unresolved',status='sourced',checked_at='2026-09-13',as_of='2026-09-13');s=[]
 if k<5:
  f['name']=benef[k]+' (via Cornerstone Government Affairs)';f['description']+=' This record names Cornerstone acting on its behalf, with '+firms[k]+' filing the report.'
  for v in d['sources']:
   s.append(src(v['url'],('Original2026report identifies '+firms[k]+' as registrant and Cornerstone Government Affairs obo '+benef[k]+' as client.') if 'lda.gov' in v['url'] else d['description']))
  if k==0:f['website_status']='partial';f['description']='This client record names Google Client Services LLC, represented through Cornerstone Government Affairs, with JGB & Associates filing the report. The exact LLC’s connection to Google’s corporate structure remains unverified.'
  if k==1:
   f['review_outcome']='confirmed';f['notes']='Original2026report establishes DiNino Associates as registrant and Cornerstone obo ID.me LLC as client. ID.me’s November2025employee privacy policy explicitly names ID.me LLC and its current help center repeats the LLC legal name. This resolves the identity gap left by older Inc. terms; current ownership remains Unknown.';s.append(src('https://network.id.me/privacy-policy/','November2025employee privacy policy specifically names ID.me LLC; revision history says Update LLC.'))
 else:
  s=[src(d['official_url'],d['evidence'])]
  if k==6:s.append(src('https://www.td.com/content/dam/tdcom/canada/about-td/pdf/acquisition-history/2022/final-joint-cowen-deal-close-24-02-2023.pdf','TD and Cowen jointly announced completed acquisition March1,2023; parts of combined business continued as TD Cowen.'));f['name']='Cowen Group (now part of TD)'
  if k==9:
   s.extend([src('https://lda.gov/filings/public/filing/9d465767-6039-4652-af57-ff549bbf6d1a/print/','OriginalLD1 names exact Culture Organics LLC in Rye NH and alternative-plastic manufacturing.'),src('https://products.bpiworld.org/companies/culture-organics-llc','BPI product directory identifies exact company at matching address and lists resin product. Its New York state label conflicts with SEC/LDA New Hampshire; not adopted.')])
 f['identity_evidence']=f['notes'];p[i].update(f);byurl={x['url']:x for x in p[i].get('sources',[])}
 for v in s:byurl[v['url']]=v
 p[i]['sources']=list(byurl.values());dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes'],sources=s))
(r/'featured104-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured104-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()));print('Status changes',[(i,b.get('status'),p[i]['status']) for i,b in before.items() if b.get('status')!=p[i]['status']])
