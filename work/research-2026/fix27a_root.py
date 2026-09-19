import json,pathlib,gzip,copy,re
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round27-a-root-draft.json'));rows=json.load(open(r/'general-round27-a-input.json'));c=json.load(open(r/'general-round27-c-researched.json'))
for k,v in p.items():
 o=v['ownership'];v['notes']=v.get('notes','');v['ownership']='Government body' if o=='public local government' else 'Subsidiary / affiliated entity' if o.startswith('subsidiary') else 'Private company' if o.startswith('wholly owned') else 'Unknown'
 if v['ownership']=='Unknown':v['review_outcome']='partial'
 if not v.get('identity_evidence'):v['identity_evidence']='Official organization description and original filing reviewed; remaining uncertainties are noted.'
 if not v.get('sources'):
  f=json.load(gzip.open(f'lobbying-map/public/data/reports/{k[:2]}.json.gz','rt'))[k][0]
  v['sources']=[dict(url=f"https://lda.gov/filings/public/filing/{f['id']}/print/",label='Original disclosure',claim='Identifies the client under this disclosed name.')]
 if ' OBO ' in v['name']:v['name']=v['name'].split(' OBO ')[1]+' (via Brownstein)'
 v['description']=v['description'].split(' (represented client')[0]
def fix(k,url,claim,**kw):
 v=p[k];v.update(kw);v['identity_evidence']=claim;v['sources'].append(dict(url=url,label='Primary identity or ownership evidence',claim=claim));return v
fix('b00181240a3e42d7','https://investors.palantir.com/files/2026%20Q1%20PLTR%2010-Q.pdf','Palantir’s 2026 quarterly report identifies its Nasdaq listing, NASDAQ: PLTR.',ownership='Publicly traded',review_outcome='confirmed',website='https://www.palantir.com/',featured=True)
fix('7a3dc71ef2821667','https://www.brunswick.com/investors/','Issuer investor page identifies Brunswick Corporation as NYSE: BC.',ownership='Publicly traded',review_outcome='confirmed')
for k in ['cb70170f2739d82f','f06b8575bbf3c324']:fix(k,'https://www.bruno.com/ca/about','Bruno identifies its exact legal name and family ownership.',ownership='Private company',review_outcome='confirmed',description='Manufactures stairlifts, wheelchair and scooter lifts, platform lifts, and home elevators.')
fix('806585cc5e7c2ac4','https://www.brownsville-pub.com/about/the-value-of-public-power/','BPUB identifies itself as a municipally owned utility governed by a city-appointed board.',ownership='Government body',kind='Government',review_outcome='confirmed')
for k in ['ca1ebe3b2a885ba2','cbba497255b3109d','3eac0739a74848f9']:
 v=p[k];base=copy.deepcopy(c['b1b45bef1722fdd5']);base.update(id=k,name='Business Software Alliance',sources=v['sources']+base['sources']);p[k]=base
fix('0e0068bd676b6d64','https://lapaz.gov/381/Sanitary-Sewer-Systems','La Paz County identifies Buckskin Sanitary District as the sewer-service provider between the CRIT reservation and Parker Dam.',website='https://www.buckskinsanitarydistrict.org/',kind='Government',ownership='Government body',review_outcome='confirmed',description='Public sanitary district providing sewer collection and wastewater treatment near Parker, Arizona.')
v=p['6bcb8417affc7d17'];v['sources']=[s for s in v['sources'] if 'bostonscientific.com' not in s['url']]
fix('6bcb8417affc7d17','https://serb.com/accreditations/','SERB identifies BTG International Inc. as a SERB Pharmaceuticals company and gives its Pennsylvania address.',website='https://serb.com/',ownership='Subsidiary / affiliated entity',review_outcome='confirmed',description='SERB pharmaceutical business supplying specialty medicines, including emergency treatments and antidotes.',notes='Older Boston Scientific ownership sources are superseded; group website.')
p['723c0b5bb032b778'].update(kind='Individual',ownership='Not applicable',description='Individual lobbying client who reports being a real-estate executive. The exact business affiliation remains unverified.',review_outcome='partial')
p['9efd7471a9486627'].update(kind='Business',description='Lobbying client reporting that it imports and distributes organic sugar. Ownership and official website remain unverified.',review_outcome='partial')
p['a273dffa3ca72683'].update(description='Lobbying client recorded as Bside Capital. Its precise business identity, ownership, and official website remain unverified.',review_outcome='unresolved')
p['7c1a7c2eb3c3803f']['name']='ArcelorMittal Liberia (via Bryan Cave Leighton Paisner)'
p['53a147f99eced163']['description']='Provides workplace and asset-management software for managing offices, facilities, equipment, and maintenance.'
(r/'general-round27-a-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
