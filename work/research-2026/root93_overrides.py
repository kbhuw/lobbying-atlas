import json,pathlib
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round93-input.json'));p={}
for part in 'bcd':p.update(json.load(open(r/f'round93-{part}-evidence.json')))
assert set(p)=={x['id'] for x in rows}
def v(i):return p[rows[i]['id']]
# Root verified source-specific corrections; never infer ownership from legal suffix alone.
v(0).update(ownership='Unknown',review_outcome='partial',notes='The official practice website establishes its pain-management work. A Form D for a similarly named holding entity does not establish current ownership of this exact lobbying client.')
v(0)['sources']=[s for s in v(0)['sources'] if 'sec.gov' not in s['url']]
for i in [4,11]:v(i)['description']=v(i)['description'].replace('nonprofit, ','').replace('nonprofit ','')
# Tour IRS evidence was incorrectly attached to Treasury Employees Union.
tour=[s for s in v(16)['sources'] if 'NATIONAL TOUR ASSOCIATION' in s['claim']]
v(15).update(ownership='Nonprofit / tax-exempt',review_outcome='confirmed',notes='IRS exact National Tour Association Inc., EIN 311049903, Lexington KY, subsection06, status01.')
v(15)['sources']+=tour
v(16).update(ownership='Unknown',review_outcome='partial',notes='National union identified by its official website; no chapter-specific IRS exemption has been substituted for the national organization.')
v(16)['sources']=[s for s in v(16)['sources'] if 'irs.gov' not in s['url']]
# Independently read IRS rows and original disclosure metadata.
irs={x['EIN']:x for x in json.load(open(r/'round93-root-irs-rows.json'))}
for i,ein,desc in [(2,'394707869','Social welfare organization advocating for STEM education, as reported in its lobbying registration.'),(82,'921746571','Biomedical-research advocacy and education organization, as reported in its lobbying registrations.')]:
 x=irs[ein];v(i).update(description=desc,ownership='Nonprofit / tax-exempt',review_outcome='partial',notes=f"IRS record {x['NAME']}, EIN {ein}, {x['CITY']} {x['STATE']}, subsection {x['SUBSECTION']}, status {x['STATUS']}; matches disclosed name and location. Current official website remains unverified.",sources=[{'url':'https://www.irs.gov/pub/irs-soi/'+x['file'],'claim':f"IRS identifies {x['NAME']}, EIN {ein}, {x['CITY']} {x['STATE']}, subsection {x['SUBSECTION']}, status {x['STATUS']}."}]+rows[i]['profile']['sources'])
v(2)['name']='National STEM Talent Initiative';v(82)['name']='NCATS Alliance'
v(5).update(name='National Stripper Well Association',website='https://nswa.us/',ownership='Nonprofit / tax-exempt',review_outcome='confirmed',description='Trade association representing owners and operators of marginal oil and natural-gas wells in federal legislative and regulatory policy.',notes='The filing uses plural Wells; the official association uses singular Well. Official address matches IRS EIN522328209, Ada OK. Original filing name is retained as an alias.',sources=[{'url':'https://nswa.us/','claim':'The National Stripper Well Association describes advocacy for marginal oil and gas wells and lists 2313 N. Broadway, Ada OK.'},{'url':'https://www.irs.gov/pub/irs-soi/eo3.csv','claim':'IRS identifies NATIONAL STRIPPER WELL ASSOCIATION, EIN522328209, 2313 N Broadway Ave, Ada OK, subsection06, status01.'}])
v(46).update(ownership='Unknown',review_outcome='partial')
v(47).update(name='Advance CTE (National Association of State Directors of Career Technical Education)',notes='The official privacy policy explicitly establishes the legal name and Advance CTE DBA. This is distinct from ACTE.',sources=[{'url':'https://careertech.org/','claim':'Advance CTE supports state career and technical education directors through policy, leadership resources and professional development.'},{'url':'https://careertech.org/privacy-policy/','claim':'The privacy notice identifies National Association of State Directors of Career Technical Education doing business as Advance CTE.'}])
for i in [61,62,63,64]:
 v(i).update(ownership='Unknown',review_outcome='partial')
 if i==61:v(i)['notes']='Public benefit corporation is a legal form; the cited source does not establish whether it is privately held.'
 else:v(i)['notes']+=' Tribal ownership is established; the current ownership taxonomy lacks a dedicated tribal-enterprise category, so it is not labeled privately owned.'
v(80)['description']='The lobbying client describes itself as a nonprofit. Its specific programs and exact current organizational identity remain unverified.'
for i in [81,84,87,88,92,97]:v(i)['description']='The lobbying client reports: '+rows[i]['profile']['description'].strip().rstrip('.')+'. Its exact current organizational identity and website remain unverified.'
v(83)['name']='National Coordinating Committee for Multiemployer Plans (NCCMP)'
v(86)['name']='NCTA — The Internet & Television Association'
v(89)['name']='Nebius Group N.V.';v(94)['name']='NeedleSmart'
for i in [33,38,39,40,41,57,76,85,86,89]:v(i)['featured']=True
for x in p.values():
 if x['ownership']=='Unknown' and x['review_outcome']=='confirmed':x['review_outcome']='partial'
(r/'round93-root-incremental-evidence.json').write_text(json.dumps(p,indent=2)+'\n')
