import json,copy,datetime
from pathlib import Path
P=Path('work/research-2026'); master=P/'reviewed.json'; d=json.loads(master.read_text()); inp=json.loads((P/'featured64-input.json').read_text()); by={x['id']:x for x in inp}; before={i:copy.deepcopy(d[i]) for i in by}; changes=[]
def apply(i,url,evidence,**kw):
 p=d[i]; assert p['review_outcome']!='confirmed'; p.update(review_outcome='confirmed',status='sourced',website_status='verified',checked_at='2026-09-13',as_of='2026-09-13',identity_evidence=evidence,notes=evidence,**kw)
 p['sources']=[s for s in p.get('sources',[]) if s.get('label')=='Original lobbying disclosure']+[{'url':url,'label':'Official organization evidence','claim':evidence}]
 changes.append({'id':i,'url':url,'evidence':evidence,**kw})
a=json.loads((P/'featured64-first10.json').read_text()); assert {x['originalID'] for x in a}=={x['id'] for x in inp[:10]}
for x in a:
 i=x['originalID']
 if x['decision']!='confirm' or i=='c12b9af25189a4ce':continue
 prop=x['proposed']; ev=x['evidence']; own='Unknown'
 if i in ['372062a0285dd453','f463363702487e81','da13725d36943bcc']: ev+=' Trade-association activity is supported; tax-exempt status was not established by this page.'
 if i=='da13725d36943bcc': ev='Official HINJ page spells out HealthCare Institute of New Jersey and describes its life-sciences trade-association activity. No tax-exempt status or corporate ownership is inferred.'
 apply(i,x['exact_quotes'][0]['url'],ev,name=prop['name'],website=prop['website'],kind=prop['kind'],ownership=own)
d['3310a587be14dcab']['description']='Operates online marketplaces that help consumers use health and wellness benefits, including FSA and HSA funds. This filing covers the Health-E Commerce group including subsidiaries.'
b=json.loads((P/'featured64-middle10.json').read_text());assert {x['id'] for x in b}=={x['id'] for x in inp[10:20]}
for x in b:
 if x['decision']!='confirm':continue
 ev=x['exact_official_excerpt']+' Original filed name and activity match; ownership remains unverified.'
 url=next(u for u in x['source_urls'] if 'lda.gov' not in u)
 apply(x['id'],url,ev,description=x['description'],website=x['website'],kind=x['kind'],ownership='Unknown')
rows=[
('34e6967be7d23e26','https://helixdefense.com/our-vision/','Official site identifies Helix Defense and counter-drone munitions technology, matching the unsuffixed filed brand and activity. Legal form and ownership are not established.','Unknown'),
('5874979f74167ad6','https://www.hemophiliafed.org/our-story/','Official organization history identifies Hemophilia Federation of America, incorporated in 1994, and its bleeding-disorders education and advocacy mission. Identity confirmed; no newly verified tax-exemption determination is claimed.','Unknown'),
('bdc99f6c0cbc29a4','https://henrymeds.com/legal/terms-of-service/','Official terms dated August 6, 2026 identify Adonis Health Inc. doing business as Henry Meds. The platform coordinates access to providers and pharmacies; it does not itself practice medicine or fill prescriptions. The original filing description is retained as reported, not treated as the platform business model. Ownership remains unverified.','Unknown'),
('f814f8e2473e7d43','https://www.hermeus.com/s/purchasingterms.pdf','Official purchasing terms define Hermeus as Hermeus Corporation, unless a contracting instrument specifies an affiliate. The original filings expressly name Hermeus Corporation/Corp.; identity confirmed without extending the match to all affiliates.','Unknown'),
('69661814f1d08e88','https://hevenaerotech.com/heven-aerotech-a-new-identity-for-a-growing-mission/','Official September 30, 2025 announcement bridges Heven Drones to Heven AeroTech and describes unmanned systems, matching the filed brand and activity. Ownership remains unverified.','Unknown'),
('b31f50a91621ff4f','https://investors.hpe.com/stock','Official investor page identifies Hewlett Packard Enterprise, its enterprise technology business and NYSE stock ticker HPE. Original unsuffixed filing names this issuer, not HP Inc.','Public company (NYSE: HPE)'),
('5575927c07ddfad1','https://investors.hpe.com/stock','Original label is Hewlett Packard Enterprise with the acronym HPE in parentheses. Official investor page explicitly bridges this name and acronym and identifies the NYSE-listed issuer. No subsidiary qualifier appears in the original label.','Public company (NYSE: HPE)')]
for i,u,e,o in rows:apply(i,u,e,ownership=o)
d['bdc99f6c0cbc29a4']['description']='Henry Meds is a telehealth platform operated by Adonis Health Inc. It coordinates access to healthcare providers, pharmacies and laboratory services; the platform itself does not practice medicine or fill prescriptions.'
d['bdc99f6c0cbc29a4']['kind']='Telehealth platform'
d['9c7b88e930d1fbe8']['legal_form']='Limited liability company'
d['dc11452008337635']['legal_form']='Corporation'
d['f814f8e2473e7d43']['legal_form']='Corporation'
# Acquisition does not prove the filed FKA represents a legal rename.
h=d['c12b9af25189a4ce'];h['notes']='The official 2019 acquisition announcement establishes that WageWorks became a HealthEquity subsidiary, not that HealthEquity was formerly WageWorks. Preserve the filed FKA wording as reported; exact represented-entity continuity remains unresolved.';h['identity_evidence']=h['notes']
(P/'featured64-before.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n');(P/'featured64-root-decisions.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False)+'\n')
for path,indent,nl in [(master,2,True),(Path('lobbying-map/research/reviewed-2026.json'),None,False),(Path('outputs/2026-research-trial/profiles.json'),2,True)]:path.write_text(json.dumps(d,indent=indent,ensure_ascii=False)+ ('\n' if nl else ''))
mfile=Path('lobbying-map/research/verified-entity-merges.json'); merges=json.loads(mfile.read_text());used={i for m in merges for i in m['source_ids']};ids=['b31f50a91621ff4f','5575927c07ddfad1'];assert not used.intersection(ids)
merges.append({'canonical_id':ids[0],'source_ids':ids,'rationale':'Same original organization name; second label adds only the official HPE acronym in parentheses. Official investor page explicitly bridges name and acronym. Preserve all original filings; HP Inc. remains distinct.','sources':[{'url':'https://investors.hpe.com/stock','claim':'Official issuer name and HPE acronym/ticker.'}],'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});mfile.write_text(json.dumps(merges,indent=2,ensure_ascii=False)+'\n')
print('Confirmed',len(changes),'merge groups',len(merges))
