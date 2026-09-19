import pathlib,json
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round35-b-input.json'));p=json.load(open(r/'general-round35b-root-draft.json'));c=json.load(open(r/'round35b-last-critical-corrections.json'))
for k,z in c.items():
 v=p[k];v.update(name=z['name'],description=z['corrected_description'],kind=z['corrected_kind'],ownership=z['corrected_ownership'],website=z['website'],notes=z['notes'],identity_evidence='Exact filing identity compared with cited primary legal and organization evidence. '+z['notes'],review_outcome='partial');v['sources']=[v['sources'][0]]+[dict(url=x['url'],label='Primary organization evidence',claim=x['claim']) for x in z['sources']]
def patch(i,desc=None,web=None,own=None,kind=None,source=None,notes=None):
 v=p[rows[i]['id']]
 for field,val in [('description',desc),('website',web),('ownership',own),('kind',kind),('notes',notes)]:
  if val is not None:v[field]=val
 if source:v['sources'].append(dict(url=source[0],label='Primary organization evidence',claim=source[1]))
 v['review_outcome']='partial'
patch(135,'Client reporting products intended to keep homes, offices and cars cleaner. Exact independently verified product range remains unresolved.',web='',own='Unknown',notes='Filing describes cleaner home/office/car environments; no support for the draft waste-recycling claim. Official domain and ownership remain unverified.')
patch(136,'Identity-verification business offering biometric identity checks and airport security membership services.',web='https://www.clearme.com/',own='Unknown',source=('https://ir.clearme.com/','Clear Secure investor site describes CLEAR biometric identity-verification services and identifies Clear Secure Inc.'),notes='CLEAR brand fits the security-screening filing. The abbreviated filing does not establish which group legal entity lobbied; public parent ticker not assigned without that link.')
p[rows[136]['id']]['name']='CLEAR (security-screening filing)'
patch(139,'Develops negative-pressure wound therapy devices and dressings, including the PREVENT Kit.',own='Unknown',kind='Medical-device company',source=('https://www.accessdata.fda.gov/cdrh_docs/pdf23/K232379.pdf','FDA 510(k) summary identifies Clear Choice Therapeutics Inc in Raleigh, North Carolina and describes its PREVENT wound-therapy kit.'),notes='Medical-device developer, not a metabolic-drug company. Current ownership unknown.')
patch(148,'Manufactures paperboard for packaging applications.',source=('https://www.clearwaterpaper.com/','Official company website describes paperboard manufacturing.'),notes='The company sold its tissue business in 2024; older descriptions of an ongoing tissue segment are not adopted.')
patch(169,'Provides weather forecasting and precipitation monitoring using radar observations, numerical modeling and computing.',own='Unknown',source=('https://climavision.com/wp-content/uploads/2023/09/Climavision-SP-RaaS-TV-2023-FINAL.pdf','Official product sheet describes Climavision weather-radar services.'),notes='Not described as a satellite-only forecasting business; current equity ownership unknown.')
patch(170,'Climavision-associated operating client reporting weather-technology services.',own='Unknown',notes='Exact legal connection of the Operating LLC to the branded company remains only partially established; no unsupported subsidiary chain assigned.')
for i in [172,173]:
 patch(i,'Metropolitan Transit Authority of Harris County, operating public transit services in the Houston region.',web='https://www.ridemetro.org/',own='Government body',kind='Public transit authority',source=('https://www.ridemetro.org/about','Official METRO profile identifies the public transit authority serving the Houston region.'),notes='Cline Strategic Consulting is the named lobbying intermediary, not the owner of the transit authority.')
 p[rows[i]['id']]['name']='Houston METRO (via Cline Strategic Consulting)'
patch(143,web='',notes='Exact Action Fund legal identity remains distinct and unresolved; similar ClearPath Action branding is not treated as proof of identity.')
for i in [137,144,145,161,162,163,164,174,176,177,188,195]:
 patch(i,own='Unknown');p[rows[i]['id']]['notes']+=' Sources establish business activity but not current equity ownership.'
for i in [97,133]:patch(i,own='Unknown')
for i in [100,101,102]:
 p[rows[i]['id']]['description']='Provides healthcare payment analytics, cost-management and network services.';p[rows[i]['id']]['review_outcome']='confirmed'
tickers={111:('https://ir.qorvo.com/static-files/70d94020-c63d-4be3-8f31-80d3b2471492','July 2026 issuer filing identifies Qorvo as Nasdaq: QRVO; proposed Skyworks merger is not treated as already completed.'),114:('https://www.sec.gov/Archives/edgar/data/855658/000143774926025657/lscc20260704_10q.htm','July 2026 Form 10-Q identifies Lattice Semiconductor shares as Nasdaq: LSCC.'),115:('https://www.lightpath.com/investors','Official investor page identifies LightPath Technologies as Nasdaq: LPTH.'),116:('https://www.marvell.com/company/newsroom/marvell-completes-acquisition-of-celestial-ai.html','February 2026 acquisition-completion announcement identifies Marvell Technology as NASDAQ: MRVL.'),141:('https://www.clearmindmedicine.com/investors','Official investor page identifies Clearmind Medicine shares as Nasdaq: CMND.')}
for i,s in tickers.items():patch(i,source=s)
patch(112,own='Subsidiary',source=('https://www.marvell.com/company/newsroom/marvell-completes-acquisition-of-celestial-ai.html','Marvell confirms completion of the Celestial AI acquisition on February 2, 2026.'))
# Keep useful activity descriptions for unresolved records rather than replacing them with a generic error.
for i,row in enumerate(rows):
 v=p[row['id']]
 if 'Exact identity not independently resolved' in v['description'] or 'exact legal entity and current business website' in v['description']:
  d=row.get('profile',{}).get('description','')
  if d:v['description']='Lobbying client reporting the following activity: '+d.rstrip('.')+'.';v['review_outcome']='unresolved';v['ownership']='Unknown';v['website']=''
(r/'general-round35b-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
