import json,pathlib,gzip,re
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round37-input.json'));e={};p={}
for part in ['first25','second25','third25','root25']:e.update(json.load(open(r/f'round37-{part}-evidence.json')))
for part in ['first25','second25','third25','root-two','root-type','final-identity']:
 f=r/f'round37-{part}-corrections.json'
 if f.exists():
  for k,v in json.load(open(f)).items():
   old=e[k];src=old['sources'];old.update(v);old['sources']=v.get('sources',src)
exec((r/'filing_evidence.py').read_text());s=(r/'research30c_root.py').read_text();helper=s[s.index('def add('):s.index("add(0,'Carbon")].replace("filing=json.load(gzip.open('lobbying-map/public/data/reports/'+row['id'][:2]+'.json.gz','rt'))[row['id']][0]","filing,filing_member=latest_filing(row)");exec(helper)
for i,row in enumerate(rows):
 v=e[row['id']];own=v['ownership'];notes=v.get('notes','');out=v.get('review_outcome','partial')
 if i<25:
  notes+=' '+own
  own={0:'Public company',1:'Public company',3:'Nonprofit / tax-exempt',4:'Private company',6:'Nonprofit / tax-exempt',7:'Not applicable',8:'Nonprofit / tax-exempt',9:'Not applicable',12:'Government body',14:'Government body',15:'Nonprofit / tax-exempt',16:'Nonprofit / tax-exempt',17:'Government body',19:'Government body',20:'Government body',21:'Government body',22:'Subsidiary',23:'Subsidiary',24:'Private company'}.get(i,'Unknown')
 if own=='Unknown' and out=='confirmed':out='partial'
 name=v['name'];name=re.sub(r'\b(For|Of|And|TO|ON|IN|BY|The)\b',lambda m:m[0].lower(),name)
 src=[(s['url'],s['claim']) for s in v['sources'] if s['url'] not in ['https://lda.gov/','https://lda.gov/api/v1/clients/','https://www.sec.gov/ixviewer/doc/action?doc=','https://www.cfc.gov/']]
 add(i,name,v['description'],v.get('website',''),kind=v['kind'],own=own,sources=src,notes=notes,outcome=out,featured=i in [0,1,4,6,7,12,22,23,31,35,37,40,46,47,57,64,65,85,87,89,90])
def patch(i,**kw):p[rows[i]['id']].update(kw)
patch(0,name='Colgate-Palmolive Company');patch(1,name='Colgate-Palmolive Company');patch(14,name='City of College Park, Georgia');patch(21,name='Colorado Springs Utilities');patch(36,name='Color Of Change')
patch(4,review_outcome='partial')
patch(55,review_outcome='unresolved',kind='Informal coalition')
patch(62,review_outcome='unresolved')
for i in [48,66,68,74]:
 patch(i,ownership='Unknown',review_outcome='partial')
patch(32,ownership='Unknown',review_outcome='partial')
patch(38,name='Colosseum Rare Metals, Inc.',ownership='Subsidiary',review_outcome='partial',description='U.S. mining subsidiary of Dateline Resources developing the Colosseum gold and rare-earth project in California.',notes='Filing former-name parenthetical retained as provenance; Dateline Resources is its parent, not simply its former name. Parent stock ticker is not assigned to this subsidiary.')
p[rows[38]['id']]['sources']=[p[rows[38]['id']]['sources'][0],dict(url='https://cdn-api.markitdigital.com/apiman-gateway/ASX/asx-research/1.0/file/2924-02943033-2A1594349%26v%3D7bc42bd11d853ed5e8c28f2ffcd6a069ee5cd6b4',label='Issuer announcement',claim='May 5, 2025 Dateline announcement explicitly identifies Colosseum Rare Metals Inc as its wholly owned US subsidiary.')]
patch(34,website='https://www.yourcommunityhospital.com/')
patch(41,name='Columbia Basin Development League',description='Nonprofit advocating completion and maintenance of the Columbia Basin irrigation and water infrastructure project.',website='https://cbdl.org/',ownership='Nonprofit / tax-exempt',kind='Water infrastructure nonprofit',review_outcome='partial',notes='Abbreviated client label matched by Washington location, water infrastructure activity and Capitol Path Consulting representation.')
p[rows[41]['id']]['sources']+= [dict(url='https://cbdl.org/about/league-staff/',label='Official staff',claim='League lists John Culton of Capitol Path Consulting for federal government affairs, matching the disclosed registrant.'),dict(url='https://cbdl.org/about/the-league/',label='Official profile',claim='League identifies its nonprofit status and water infrastructure advocacy.')]
patch(42,website='',ownership='Unknown',kind='Irrigation advocacy client',review_outcome='unresolved',description='Lobbying client identified as Columbia Basin Project, with Washington State Water Resources Association in its former-name field.',notes='Exact legal organization unresolved. Do not identify this advocacy client as the federal Bureau of Reclamation project.')
p[rows[42]['id']]['sources']=[p[rows[42]['id']]['sources'][0],dict(url='https://lobbyingdisclosure.house.gov/lookup.asp?reg_id=40766',label='House client listing',claim='Water Strategies lists this exact client label.')]
# Local union evidence cannot establish the national union tax classification.
for i in [89,90]:
 patch(i,ownership='Not applicable',notes='Member-representative labor union; corporate stock ownership does not apply. National tax classification not inferred from a local union return.')
 p[rows[i]['id']]['sources']=[x for x in p[rows[i]['id']]['sources'] if '420807546' not in x['url']]
patch(82,review_outcome='unresolved',website='')
for i in [2,5,10,11,13,18]:
 if p[rows[i]['id']]['kind']=='Unknown':p[rows[i]['id']]['kind']={2:'Software company',5:'Student loan provider',10:'Professional association',11:'Professional association',13:'Scientific association',18:'Lobbying firm'}[i]
for k,v in json.load(open(r/'round37-logo-fixes.json')).items():
 p[k]['website']=v['website'];p[k]['sources']+=v['sources']
# Exact holding company identity, not the unrelated Cornelia institution.
p[rows[95]['id']]['sources']=[z for z in p[rows[95]['id']]['sources'] if 'enforcement20090923b' not in z['url']]
p[rows[95]['id']]['sources'].append(dict(url='https://www.ffiec.gov/npw/Institution/Profile/1081873?dt=20120101',label='Federal Reserve institution record',claim='FFIEC identifies Community Bankshares Inc at 201 Broad Street, LaGrange, as a bank holding company.'))
# Current official domain redirects to the parent project page.
patch(88,website='https://caturus.com/operations/',review_outcome='partial')
# Preserve historic group legal evidence, without treating an old issuer as current ownership.
p[rows[99]['id']]['sources'].append(dict(url='https://www.ccfi.com/wp-content/uploads/2020/03/CCF-Holdings-December-31-2019-Financial-Statements-1.pdf',label='Group financial statements',claim='Group 2019 financial statements identify Community Choice Financial Holdings LLC as a guarantor.'))
(r/'general-round37-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
