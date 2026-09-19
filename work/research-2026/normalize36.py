import json,pathlib,gzip,re
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round36-input.json'));e={};p={}
for part in ['first25','second25','third25','root25']:e.update(json.load(open(r/f'round36-{part}-evidence.json')))
e.update(json.load(open(r/'round36-second25-corrections.json')))
exec((r/'filing_evidence.py').read_text());s=(r/'research30c_root.py').read_text();helper=s[s.index('def add('):s.index("add(0,'Carbon")].replace("filing=json.load(gzip.open('lobbying-map/public/data/reports/'+row['id'][:2]+'.json.gz','rt'))[row['id']][0]","filing,filing_member=latest_filing(row)");exec(helper)
for i,row in enumerate(rows):
 v=e[row['id']];own=v['ownership'];notes=v.get('notes','');out=v.get('review_outcome','partial');src=[(s['url'],s['claim']) for s in v['sources'] if s['url'] not in ['https://lda.gov/','https://tsdr.uspto.gov/']]
 if own not in ['Government body','Nonprofit / tax-exempt','Public company','Subsidiary','Private company','Not applicable','Unknown']:
  notes+=' '+own;own='Unknown'
 if i in [2,6,11,22,23]:own='Nonprofit / tax-exempt'
 if i in [3,4,5,7,9,10,12,15,18,19,20]:own='Not applicable';out='partial'
 if own=='Unknown' and out=='confirmed':out='partial'
 name=v['name'];name=re.sub(r'\b(For|Of|And|TO|ON|IN|BY|The)\b',lambda m:m[0].lower(),name);name=name.replace('PET Care','Pet Care').replace('GAS','Gas').replace('TAX','Tax').replace('USE','Use').replace('NEW England','New England').replace('FLU','Flu')
 if out=='unresolved':
  profile=row.get('profile') or {};d=profile.get('description')
  if d:v['description']='Lobbying client reporting the following activity: '+d.strip().rstrip('.')+'.'
  src += [(s['url'],s['claim']) for s in profile.get('sources',[])]
 add(i,name,v['description'],v['website'],kind=v['kind'],own=own,sources=src,notes=notes,outcome=out,featured=i in [59,66,67,69,75,81,84,85,89,90,91,92,95,96,97])
def patch(i,web=None,desc=None,name=None,own=None,source=None,out='partial',notes=None):
 v=p[rows[i]['id']]
 for k,z in [('website',web),('description',desc),('name',name),('ownership',own),('notes',notes)]:
  if z is not None:v[k]=z
 v['review_outcome']=out
 if source:v['sources'].append(dict(url=source[0],label='Primary organization evidence',claim=source[1]))
patch(0,desc='Coal-industry organization identified by CEDAR as a co-founder based in Pikeville, Kentucky.',source=('https://www.cedarinc.org/','CEDAR identifies Coal Operators and Associates of Pikeville, Kentucky as a founding partner.'),notes='Historical identity evidence established; current operating scope, ownership and official website remain unknown.')
patch(20,web='https://renewgsptoday.com/',source=('https://renewgsptoday.com/about/','Official campaign site says it is operated by the Coalition for GSP.'))
patch(21,name='4As Health (formerly Coalition for Healthcare Communication)',web='https://4ashealth.org/',own='Subsidiary',source=('https://www.aaaa.org/blog/4as-rebrands-coalition-for-healthcare-communication-to-4as-health-as-part-of-next-chapter-strategy/','June 2026 4As announcement confirms its subsidiary CHC now operates as 4As Health.'),out='confirmed')
patch(40,web='https://www.epscorideacoalition.org/',desc='Coalition advocating federal support for EPSCoR and IDeA research programs and research capacity across member jurisdictions.',source=('https://www.epscorideacoalition.org/','Official coalition website describes EPSCoR/IDeA congressional advocacy.'))
patch(41,web='https://thecfainc.com/',source=('https://thecfainc.com/','Official site identifies the Coalition of Franchisee Associations and its member-association mission.'))
patch(43,out='unresolved',notes='Exact filing name retained. No direct legal record or official website was verified; generic USPTO search page is not proof.')
patch(84,web='https://cognition.com/')
patch(94,web='https://www.coienergy.com/')
patch(99,web='https://coleridge.us/',out='confirmed')
patch(97,notes='Both the 2017 coin-counting registration and the anomalous 2025 law-firm description list Bellevue, Washington. Official Coinstar identity and headquarters match; the law-firm description is treated as an apparent filing error.',out='confirmed')
# A direct group-branded page does not prove ownership of an exact subsidiary.
for i in [70,74,86,90]:p[rows[i]['id']]['review_outcome']='partial'
# Same coalition spelling variant; identical field treatment.
p[rows[7]['id']]['ownership']=p[rows[58]['id']]['ownership'];p[rows[7]['id']]['sources']+=p[rows[58]['id']]['sources'][1:]
(r/'general-round36-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
s=(r/'check_general35b_final.py').read_text().replace('general-round35b-root-draft','general-round36-root-draft');(r/'check_general36_final.py').write_text(s)
