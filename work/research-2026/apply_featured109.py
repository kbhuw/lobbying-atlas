import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));rows=json.load(open(r/'featured109-first10.json'));before={};dec=[]
assert not (r/'featured109-before.json').exists()
notes=[
'The original 2026 report names Capitol Consulting Group LLC (DC) as registrant, Ferox Strategies as client intermediary, and the NFL as represented beneficiary. This entry describes that representation arrangement, not a separate NFL corporation.',
'The June 30, 2026 SEC 10-Q identifies exact Fervo Energy Company, a Delaware corporation, trading on Nasdaq as FRVO after its May 14, 2026 IPO.',
'The April 11, 2025 SEC Form D index identifies exact Find Solace, Inc., a Delaware corporation at 311 Fuller Street, Redwood City. Official Solace material describes patient advocacy and care coordination. Form D alone does not establish current private ownership.',
'The March 18, 2025 SEC Form D index identifies exact Flock Homes, Inc., a Delaware corporation in Denver. Its official site describes rental-property exchanges. Current ownership remains unknown.',
'The lobbying filing names Flora Food Group US, Inc. Official group material identifies Flora Food US Inc., without Group. Their legal equivalence has not been established; these records remain separate.',
'The official Delaware certificate filed October 14, 2024 explicitly changes Upfield US Inc. to Flora Food US Inc. This confirms the former-name continuity, but does not establish equivalence to the separately filed Flora Food Group US, Inc.',
'The April 17, 2026 SEC Form 4 footnote identifies exact Fluor Enterprises, Inc. as a wholly owned subsidiary of Fluor Corporation. The subsidiary does not inherit its parent’s public-company classification or NuScale’s stock ticker.',
'The April 14, 2026 SEC 8-K agreement identifies exact Foris DAX Markets, Inc. doing business as Crypto.com, separately from NADEx and Foris DAX FCM LLC. Another Crypto.com document naming Foris DAX Inc. is not proof about this Markets entity. Ownership remains unknown.',
'USDA FSIS indexed establishment material independently names Foster Poultry Farms, LLC in Farmerville and links the poultry operation. The direct page returned 403 during root review; the official indexed result corroborates the exact identity. Current ownership is not inferred from undated family-owned brand text.',
'The August 12, 2026 SEC-hosted Franklin Templeton letter expressly concerns its family of US registered open- and closed-end funds. This is a fund-family filing label, not the publicly traded Franklin Resources parent. The logo was obtained from the official website and visually checked.'
]
web=['https://www.nfl.com','https://fervoenergy.com','https://www.solace.health/','https://www.flockhomes.com/','https://www.florafoodgroup.com/','https://www.florafoodgroup.com/','https://www.fluor.com/','https://crypto.com','https://www.fosterfarms.com/','https://www.franklintempleton.com/']
for k,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));url=d['official_url'];desc=d['description']
 if k==0:
  url='https://lda.gov/filings/public/filing/3b2789d4-ea7a-45a0-887b-ceec20ea308f/print/';desc='Capitol Consulting Group reported lobbying for Ferox Strategies on behalf of the National Football League. Ferox is the intermediary; the NFL is the represented organization.'
 if k==4:desc='A Flora Food Group lobbying client associated with spreads and plant-based foods. Its exact relationship to the separately named Flora Food US Inc. remains unresolved.'
 if k==5:
  url='https://www.florafoodgroup.com/-/media/Project/Upfield/Corporate/Upfield-Corporate/Proof-of-name-change/US/20241014---FLORA-FOOD-US-INC.pdf?rev=cec1597243b144eda56040174b7a5132';desc='Flora Food US Inc., formerly Upfield US Inc., is a US company in the Flora food group, which sells spreads and plant-based food products.'
 if k==7:desc='Foris DAX Markets, Inc. is a financial-services company doing business as Crypto.com. This record refers to that named entity within the broader Crypto.com business.'
 if k==8:
  url='https://www.fsis.usda.gov/inspection/fsis-inspected-establishments/foster-poultry-farms-llc-13';desc='Foster Poultry Farms, LLC operates a poultry-processing business associated with the Foster Farms brand.'
 f=dict(description=desc,kind=d['kind'],ownership='Public company' if k==1 else 'Subsidiary' if k==6 else 'Unknown',review_outcome='partial' if k==4 else 'confirmed',notes=notes[k],identity_evidence=notes[k],website=web[k],website_status='partial' if k==4 else 'verified',status='sourced',checked_at='2026-09-13',as_of='2026-09-13')
 if k==9:f.update(kind='Investment fund family',logo_url='https://franklintempletonprod.widen.net/content/hrxzxi4q8b/webp/ft-global-logo-header.png',logo_source_url=web[k],logo_kind='logo',logo_status='official_site_asset',logo_background='light')
 p[i].update(f);sources={s['url']:s for s in p[i].get('sources',[]) if not (k==7 and 'entity_us.pdf' in s['url'])};sources[url]=dict(url=url,label='Primary identity evidence',claim=notes[k]);p[i]['sources']=list(sources.values());dec.append(dict(id=i,decision=f['review_outcome'],notes=notes[k],sources=[sources[url]]))
(r/'featured109-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured109-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()))
