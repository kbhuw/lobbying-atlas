import json,pathlib,gzip,re
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round34-b-input.json'));e=json.load(open(r/'round34b-working-evidence.json'));p={}
s=(r/'research30c_root.py').read_text();helper=s[s.index('def add('):s.index("add(0,'Carbon")];exec((r/'filing_evidence.py').read_text());helper=helper.replace("filing=json.load(gzip.open('lobbying-map/public/data/reports/'+row['id'][:2]+'.json.gz','rt'))[row['id']][0]","filing,filing_member=latest_filing(row)");exec(helper)
# Only retain claims actually supported by the primary documents.
for i in [72,75]:
 v=json.load(open(r/'round34b-citi-citadel-corrections.json'))[rows[i]['id']];e[rows[i]['id']].update(v);e[rows[i]['id']].update(ownership='Unknown',review_outcome='partial',notes='Investment-management business is distinct from Citadel Securities. Exact ownership chain is not established by the cited identity page.')
v=e[rows[79]['id']];v.update(website='https://www.citigroup.com/global/about-us',ownership='Subsidiary',review_outcome='partial',notes='Historical SEC subsidiary list names the exact Washington corporation; a 2026 Citi privacy notice still lists it among Citi entities. Current immediate ownership chain not established. The 2025 significant-subsidiary list does not name this entity and was rejected as proof.',sources=[dict(url='https://www.sec.gov/Archives/edgar/data/831001/000104746906002377/a2167745zex-21_01.htm',claim='Historical SEC subsidiary list names Citigroup Washington Inc. in the District of Columbia.'),dict(url='https://www.citigroup.com/rcs/citigpa/storage/public/Citi-Non-Employee-Supplier-Online-Privacy-Notice.pdf',claim='2026 Citi non-employee privacy notice lists Citigroup Washington Inc. among Citi entities.')])
e[rows[82]['id']]['sources'].append(dict(url='https://ccrkba.org/wp-content/uploads/2026/03/CCRKBA-2024-IRS-FORM-990.pdf',claim='Organization publishes its 2024 IRS Form 990 in its official financial-information section.'))
e[rows[25]['id']]['sources'].append(dict(url='https://www.sec.gov/Archives/edgar/data/1386570/000162828025013681/cdxc-20250317.htm',claim='Company rename announcement changes the former ChromaDex issuer to Niagen Bioscience and its listing to NASDAQ: NAGE.'))
e[rows[33]['id']].update(description='Chubb-group insurance holding-company label in federal disclosures, associated with the Chubb INA holding-company business.',notes='Current filings identify Chubb INA Holdings LLC; the singular Holding Company Inc. spelling is a disclosed variant whose exact legal-name equivalence remains partial.')
# Preserve useful descriptions without claiming the branded site proves a corporate merger.
e[rows[30]['id']].update(description='Financial holding-company client associated with the NewDay USA residential mortgage business.',notes='NewDay leadership page names the same executive for NewDay USA and Chrysalis Holdings. The original filing supplies the d.b.a. label; the page alone does not establish the precise corporate ownership chain.',review_outcome='partial')
e[rows[39]['id']]['description']='Religious communal organization identified in a New York tax opinion as sharing a common treasury and communal income.'
e[rows[69]['id']].update(kind='Textile-circularity organization',description='Advocates for textile reuse, recycling and circular-economy policies under the American Circular Textiles brand.')
names={0:"Children’s National Medical Center",1:"Children’s Tumor Foundation",2:'CHILD USA',3:"Children’s Hospital Colorado",18:'ChristianaCare',19:'Christians United for Israel Action Fund',23:'CHRISTUS Health',25:'Niagen Bioscience (formerly ChromaDex)',26:'Chromalloy Gas Turbine, LLC',28:'Chronic Disease Day / Chronic Disease Alliance',31:'CHS Inc.',32:'CHSPSC, LLC',36:'Chugach Alaska Corporation',40:'Church of Scientology International',44:'CIBanco',46:'CIEBA — Committee on Investment of Employee Benefit Assets',47:'CIEE — Council on International Educational Exchange',51:'Cigar Rights of America',54:'Cigna Corporate Services, LLC and affiliates',55:'Cigna Corporation and subsidiaries',57:'Altafiber (Cincinnati Bell Inc.) and subsidiaries',58:"Cincinnati Children’s Hospital Medical Center",69:'American Circular Textiles (Circular Services Group II, LLC)',71:'CTIA — The Wireless Association',78:'CITGO Petroleum Corporation',79:'Citigroup Washington Inc.'}
for i,row in enumerate(rows):
 v=e[row['id']];own=v.get('ownership','Unknown');originalown=own
 if own.startswith('Public ('):own='Publicly traded'
 elif own=='Public' or own=='Public/locally governed':own='Government body'
 elif 'subsidiary' in own.lower():own='Subsidiary'
 elif own.startswith('Nonprofit') or own.startswith('501(d)') or 'Related affiliate of Christians' in own:own='Nonprofit / tax-exempt'
 elif own.startswith('Privately') or own in ['Family owned']:own='Private company'
 elif 'Cooperative' in own:own='Cooperative'
 elif 'Alaska Native shareholders' in own:own='Alaska Native corporation'
 elif own=='Industry consortium':own='Not applicable'
 elif own.startswith('Private Citadel'):own='Unknown'
 notes=re.sub(r' Latest filing:.*','',v.get('notes',''))
 if originalown!=own and originalown not in ['Nonprofit','Public','Public/locally governed']:notes+=' Ownership detail: '+originalown+'.'
 sources=[(s['url'],s['claim']) for s in v.get('sources',[]) if s['url']!='https://lda.gov/api/v1/clients/']
 assert sources,row['id']
 outcome=v.get('review_outcome')
 if own=='Unknown':outcome='partial' if outcome!='unresolved' else outcome
 add(i,names.get(i,v['name']),v['description'],v.get('website') or '',kind=v.get('kind','Organization'),own=own,sources=sources,notes=notes,outcome=outcome,featured=i in [5,10,20,25,53,60,67,72,78,84])
 assert len(p[row['id']]['description'])>25
(r/'general-round34b-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
print(len(p),'normalized drafts')
