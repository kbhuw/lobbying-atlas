import json,pathlib,zipfile
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
assert not (r/'featured94-before.json').exists()
rows=json.load(open(r/'featured94-first10.json'))+json.load(open(r/'featured94-middle10.json'))
follow={x['id']:x for suffix in ['first','middle'] for x in json.load(open(r/f'featured94-root-followup-{suffix}.json'))}
names=['TSMC Arizona','TTI (filed as formerly Milwaukee Tool)','Tufts Medicine','Turion Space Corporation','Turo','Tuskegee University College of Veterinary Medicine','Tutor.com, Inc.','TWG Cadillac Formula 1 Team Holdings, LLC','Internet Infrastructure Coalition (via TwinLogic Strategies)','SAIC (via TwinLogic Strategies)','Clipboard Health (Twomagnets LLC)','Tycho AI Inc.','Type One Energy Group','U.S. Center for SafeSport','U.S. Bancorp (formerly filed as U.S. Bank)','UNICEF USA (U.S. Fund for UNICEF)','U.S. Sugar','UAW Retiree Medical Benefits Trust','UBS Americas Inc.','UC Health, LLC and affiliates']
kinds=['Semiconductor manufacturer','Power-tool group filing label','Healthcare system','Space technology company','Car-sharing marketplace','University veterinary college','Online tutoring company','Formula 1 team holding-company filing','Represented-client filing label','Represented-client filing label','Healthcare staffing marketplace','Autonomous navigation technology company','Fusion-energy company','Sports-safety organization','Bank holding company','Children’s humanitarian organization','Agricultural and food-processing company','Retiree medical-benefits trust','Financial-services subsidiary','Healthcare system']
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f=dict(name=names[idx],description=d['description'],kind=kinds[idx],ownership='Unknown',review_outcome='confirmed',notes='Identity and activity supported by official organization materials. Ownership remains unknown unless separately evidenced.',website=d['website'],website_status='verified',status='sourced',checked_at='2026-09-13',as_of='2026-09-13');s=[]
 if i in follow:
  e=follow[i];f['description']=e['proposed_fields']['description'];s=[src(e['official_url'],e['evidence'])]
 if idx==0:
  f.update(ownership='Subsidiary',website='https://www.tsmc.com/english/dedicatedFoundry');s=[src('https://investor.tsmc.com/english/credit-rating','Official investor credit-rating page identifies TSMC Arizona Corporation as wholly owned by TSMC.'),src('https://www.tsmc.com/english/dedicatedFoundry','Official manufacturing overview locates TSMC Arizona Corporation in Phoenix.')]
 if idx==1:
  f.update(review_outcome='partial',website='https://www.ttigroup.com/company',website_status='partial');f['notes']='Milwaukee is a TTI brand. The filed FKA wording does not establish a legal rename or identify which TTI subsidiary is the client.'
 if idx==2:f['ownership']='Nonprofit'
 if idx==3:
  f['description']='Turion Space builds satellites and software for space-domain awareness and satellite-fleet operations.';s=[src('https://starfire.turionspace.com/eula','Official StarfireOS agreement identifies Turion Space Corp. at 5 Technology Drive, Irvine, California.'),src('https://disclosurespreview.house.gov/data/LD/2025_Registrations_XML.zip','Registration 301730411.xml identifies Turion Space Corporation at the same 5 Technology Drive address and describes defense and space manufacturing.')];f['notes']='Official legal agreement and original registration match the exact street address and business; Corp. is an abbreviation of Corporation.'
 if idx==5:f['website']='https://www.tuskegee.edu/cvm';f['notes']='Exact university college confirmed at academic-unit scope; no separate corporate ownership inferred.'
 if idx==6:f['website']='https://www.tutor.com/';f['notes']='Official privacy policy identifies Tutor.com, Inc. and its subsidiaries. Other education companies named in shared terms are not merged.'
 if idx==7:
  f.update(review_outcome='partial',website_status='partial',description='Filed as a holding company associated with the Cadillac Formula 1 team. The exact Holdings, LLC entity still needs independent verification.');s=[src('https://www.cadillacf1team.com/privacy-policy','Team policy identifies TWG Cadillac Formula 1 Team LLC, which omits Holdings from this filing’s legal name.')];f['notes']='Do not substitute the operating team LLC for the separately named Holdings, LLC.'
 if idx in [8,9]:
  f['ownership']='Not applicable';f['notes']='Original 2026 report explicitly identifies the represented client and TwinLogic intermediary; this relationship is not corporate ownership.';s=[src(d['sources'][0]['url'],'Original 2026 report explicitly names TwinLogic acting on behalf of the represented organization.')]
  if idx==8:f['description']='TwinLogic Strategies acting on behalf of the Internet Infrastructure Coalition, an association representing internet infrastructure businesses.';s.append(src('https://i2coalition.com/','Official Internet Infrastructure Coalition website.'))
  else:f['description']='TwinLogic Strategies acting on behalf of Science Applications International Corporation (SAIC), a government technology and services contractor.';s.append(src('https://investors.saic.com/','Official SAIC investor website.'))
 if idx==10:
  f['website']='https://www.clipboardworks.com/';s=[src('https://www.clipboardworks.com/terms-of-service','June 2026 terms explicitly identify Twomagnets LLC doing business as Clipboard Health and separately name affiliate Clipboard Health LLC.')];f['notes']='Exact Twomagnets LLC DBA identity confirmed; the separate affiliate Clipboard Health LLC is not merged.'
 if idx==11:s=[src('https://tycho.ai/terms-of-use','Official terms explicitly identify Tycho AI Inc. and its website services.')]
 if idx in [12,16]:f['review_outcome']='partial';f['notes']=follow[i]['evidence']
 if idx==13:f['ownership']='Nonprofit'
 if idx==14:
  f['ownership']='Public company';s=[src('https://ir.usbank.com/shareholder-information/default.aspx','Current issuer shareholder page identifies U.S. Bancorp common stock as NYSE USB.'),src('https://ir.usbank.com/news-events/news/news-details/2026/U-S--Bancorp-Names-Brian-Mauney-Head-of-Investor-Relations/default.aspx','June 2026 issuer announcement identifies U.S. Bancorp as the parent company of U.S. Bank.')];f['notes']='Formerly filed as U.S. Bank records filing history, not a legal rename of the bank into its parent.'
 if idx==15:f['ownership']='Nonprofit';f['notes']='Official financial disclosures establish U.S. Fund for UNICEF doing business as UNICEF USA, a New York nonprofit, EIN 13-1760110.'
 if idx==17:
  f.update(ownership='Nonprofit',legal_form='Tax-exempt employee welfare benefit fund (501(c)(9) VEBA)');s=[src('https://www.uawtrust.org/AdminCenter/Library.Files/Media/501/SPD/SPD2023.pdf','Official plan description identifies the trust as a tax-exempt employee welfare benefit fund under 501(c)(9), a VEBA.'),src('https://www.uawtrust.org/AdminCenter/Library.Files/Media/501/UBR%20File%20Cabinet/Reference%20Guides/2024UBRresourceguide.pdf','Official guide identifies the UAW Retiree Medical Benefits Trust and eligible GM, Ford and Chrysler retirees.')];f['notes']='A retiree-benefit VEBA trust; do not describe it as a 501(c)(3) charity.'
 if idx==18:
  f.update(ownership='Subsidiary',description='UBS Americas Inc. is a legal entity within the UBS financial-services group.');s=[src('https://www.ubs.com/global/en/investor-relations/complementary-financial-information/disclosure-legal-entities.html','June 2026 official group legal-entity disclosure explicitly names UBS Americas Inc. separately from UBS Americas Holding LLC.')];f['notes']='Exact Inc. entity confirmed in group legal-entity disclosure; do not substitute UBS Americas Holding LLC or assign the parent’s public listing.'
 if idx==19:
  s=[src('https://www.uchealth.com/en/legal-and-compliance/privacy-policy','Official system policy explicitly covers UC Health, LLC and named Cincinnati healthcare affiliates.'),src('https://disclosurespreview.house.gov/data/LD/2024_Registrations_XML.zip','Registration 301604041.xml identifies UC Health LLC and affiliates at 3200 Burnet Avenue, Cincinnati, Ohio.')];f['notes']='Cincinnati system identity confirmed using exact legal name, affiliate scope and original registration location.'
 assert s
 f['identity_evidence']=f['notes'];p[i].update(f)
 bad={d['official_url']} if d['official_url'] not in {x['url'] for x in s} else set()
 byurl={x['url']:x for x in p[i].get('sources',[]) if x['url'] not in bad}
 for x in s:byurl[x['url']]=x
 p[i]['sources']=list(byurl.values());dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes'],sources=s))
logo=next(x for x in json.load(open(r/'featured94-logo-candidates.json'))['candidates'] if x['id']==rows[5]['id']);p[logo['id']].update(logo_url=logo['asset_url'],logo_source_url='https://www.tuskegee.edu/cvm',logo_kind='logo',logo_status='official_site_asset',logo_background='light')
z=zipfile.ZipFile('work/federal-directory/raw/2025_Registrations_XML.zip');(r/'featured94-turion-registration.xml').write_bytes(z.read('301730411.xml'))
(r/'featured94-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured94-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()));print('Status changes',[(i,b.get('status'),p[i]['status']) for i,b in before.items() if b.get('status')!=p[i]['status']])
