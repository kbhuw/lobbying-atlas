import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round3-90-draft.json'))
def fix(k,desc,website,url,claim,name=None):
 v=p[k];v.update(description=desc,website=website,status='sourced',review_outcome='partial',identity_evidence=claim)
 if name:v['name']=name
 v['sources'].append(dict(url=url,label='Primary identity and activity evidence',claim=claim))
fix('e790f78ba0a14e2b','Provides patient and staff communication systems for public healthcare facilities under the PatientPoint Government brand.','https://patientpointgov.com/','https://patientpointgov.com/terms-of-use/','Official terms identify the site operator as Actio Health, Inc., a Delaware corporation doing business as PatientPoint Government.','Actio Health (PatientPoint Government)')
fix('e79f84eff23e23aa','Provides customer-data management, identity matching, analytics, and marketing technology to help businesses reach and understand audiences.','https://www.acxiom.co.uk/','https://www.acxiom.co.uk/about-us/','Official Acxiom page describes data integration and marketing technology services. This group site supports business identity; the exact LLC ownership chain remains unconfirmed.')
fix('0805610b4f8279b3','Trade association representing medical-device, diagnostic, and digital-health companies and advocating on healthcare and innovation policy.','https://www.advamed.org/','https://www.advamed.org/','Official AdvaMed website identifies the Advanced Medical Technology Association and its medical-technology membership. The abbreviated filing name is retained.','Advanced Medical Technology Association (AdvaMed)')
for k,desc in {
'93053fe4455a6524':'Disclosed as a supply-chain services business. Specific products, customers, and the current official website have not been independently established.',
'3f30608ef8ddfbab':'Coalition disclosed in connection with U.S. nitrile-glove manufacturing. Its members, legal organization, and official website remain unconfirmed.',
'a3c63db490a21edc':'Ad hoc coalition disclosed in connection with Banco Espirito Santo. Its membership, legal identity, and current activities remain unconfirmed.',
'9e81748974129ac8':'Disclosed as a technology business. The exact company, products, ownership, and official website remain unconfirmed.'}.items():
 p[k].update(description=desc,website='',status='unresolved',review_outcome='unresolved',ownership='Unknown')
p['93053fe4455a6524']['sources']=[s for s in p['93053fe4455a6524']['sources'] if 'lda.gov/' in s['url']];p['93053fe4455a6524']['identity_evidence']='Filing names Actual Resources Solutions LLC. The singular Resource candidate is not securely linked and has been excluded.'
(r/'general-round3-90-draft.json').write_text(json.dumps(p,indent=2)+'\n');print('Seven identity/activity gaps repaired')
