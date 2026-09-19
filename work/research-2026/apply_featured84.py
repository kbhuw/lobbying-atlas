import json,pathlib,datetime
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
rows=json.load(open(r/'featured84-first10.json'))+json.load(open(r/'featured84-middle10.json'))
names=['Shield AI','Sibanye-Stillwater','Hewlett Packard Enterprise (via Sidley Austin)','Hewlett Packard Enterprise (via Sidley Austin)','Sierra Nevada Company','Sierra Space','SIG Sauer, Inc.','Smith & Nephew, Inc.','SWIFT','Solo Brands','Sony Music Entertainment (formerly Sony BMG)','South32 Limited','Southwest Airlines','Space Exploration Technologies','SpaceX','Spellbinders Paper Arts LLC','SSA Marine','Stack AV Co.','STACK Infrastructure, Inc.',"Stampin’ Up!"]
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','website']};f.update(name=names[idx],ownership='Unknown',review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced',website_status='verified');s=[src(d['official_url'],d['exact_official_excerpt'])]
 for x in d.get('sources',[]):
  s.append(src(x['url'],x.get('excerpt',d['evidence'])))
 if idx in [1,9,11,12]:f['ownership']='Public company'
 if idx in [2,3]:f.update(review_outcome='confirmed',ownership='Not applicable',kind='Represented-client filing label',description='Sidley Austin LLP acting on behalf of Hewlett Packard Enterprise, the enterprise-computing company. The directory retains both the intermediary and represented client from the disclosure.')
 if idx==0:f['notes']='Official policy identifies Shield AI, Inc. A March 2025 release describes venture backing; this dated financing evidence does not by itself establish current ownership status.';f['identity_evidence']=f['notes']
 if idx==4:f['ownership']='Private company'
 if idx==5:f['notes']='Official current terms identify Sierra Space Corporation. SNC described it as a subsidiary when launched in 2021; current control following later financing is not established here.';f['identity_evidence']=f['notes']
 if idx==7:f['description']='U.S. medical-device business Smith & Nephew, Inc., operating under the Smith+Nephew brand in orthopaedics, sports medicine and wound care. The Inc. entity is distinct from the listed plc.'
 if idx==8:f['ownership']='Cooperative'
 if idx==9:s.append(src('https://investors.solobrands.com/stock-info/default.aspx','Current issuer stock-information page identifies Solo Brands, Inc.'))
 if idx==10:f['ownership']='Subsidiary';f['description']='Recorded-music business producing, marketing and distributing music worldwide. Sony’s October 2008 announcement documents Sony BMG becoming Sony Music Entertainment after Sony bought Bertelsmann’s stake.'
 if idx==11:s=[src('https://announcements.asx.com.au/asxpdf/20260212/pdf/06w70ddhsww33m.pdf','Issuer February 2026 exchange announcement identifies South32 Limited, incorporation details and ASX/LSE/JSE listings.')];f['identity_evidence']=f['notes']=s[0]['claim']
 if idx==13:f.update(review_outcome='partial',website_status='partial');f['notes']='Official SpaceX privacy policy identifies Space Exploration Technologies Corp. The grouped Inc. suffix remains an unresolved reporting variant; no legal continuity or duplicate merge is asserted for that variant.';f['identity_evidence']=f['notes']
 if idx==15:f['website']='https://spellbinders.com/'
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes']))
(r/'featured84-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured84-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
mfile=pathlib.Path('lobbying-map/research/verified-entity-merges.json');m=json.load(open(mfile));ids=['18a1e48c8236858a','8766861c0a5b4b76'];assert not any(set(ids)&set(x['source_ids']) for x in m)
claim='Both original source labels explicitly name Sidley Austin LLP on behalf of Hewlett Packard Enterprise. Consolidate the two spellings of this represented-client label while preserving all reports and both parties. This is not a merge into standalone Sidley Austin or an HPE affiliate.'
m.append(dict(canonical_id=ids[0],source_ids=ids,rationale=claim,sources=[dict(url=u,claim=claim) for u in ['https://lda.gov/filings/public/filing/f003ee58-4000-42be-9e3d-1af5bb0b90cd/print/','https://lda.gov/filings/public/filing/0cfa0991-6970-4829-b31f-5b9d6f9232f5/print/']],reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()));mfile.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()),'merges',len(m))
