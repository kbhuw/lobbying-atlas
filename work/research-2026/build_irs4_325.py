import json,pathlib,re,urllib.parse,collections
r=pathlib.Path('work/research-2026')
def read(f):return json.load(open(r/f))
def keyed(d):
 if isinstance(d,dict) and 'records' in d:d=d['records']
 return {x['id']:x for x in d} if isinstance(d,list) else d
p={**keyed(read('irs-round4-a-researched.json')),**keyed(read('irs-round4-b-researched.json')),**read('irs-round4-c-root-rewrite.json'),**keyed(read('irs-round5-last25-researched.json'))}
inputs={x['id']:x for l in 'abc' for x in read(f'irs-round4-{l}-input.json')};inputs.update({x['id']:x for x in read('irs-round5-last25-input.json')})
fixes={};audits={}
for l in 'abc':fixes.update(keyed(read(f'irs-round4-{l}-specific-corrections.json')));audits.update(keyed(read(f'irs-round4-{l}-branding-audit.json')))
for f,target in [('irs-round5-specific-corrections.json',fixes),('irs-round5-branding-audit.json',audits)]:
 if (r/f).exists():target.update(keyed(read(f)))
for l in 'abc':
 for k,a in keyed(read(f'irs-round4-{l}-logo-repairs.json')).items():
  choice=a.get('new_url') or a.get('logo_url') or ''
  decision=a.get('status',a.get('decision'))
  audits[k]={'decision':'keep' if decision in ['keep','replace'] and choice else 'hold','logo_url':choice}
out={}
for k,v in p.items():
 v=v.copy();fix=fixes.get(k,{})
 for field in ['name','description','website','identity_evidence','kind']:
  if fix.get(field):v[field]=fix[field]
 ss=v.get('sources',[])+fix.get('sources',[]);support=fix.get('supporting_source',{})
 if support.get('url'):ss.append({'url':support['url'],'label':'Official identity evidence','claim':support.get('excerpt','')})
 t=inputs[k]['tax_return'];ss.append({'url':t['source_url'],'label':'Organization Form 990','claim':'Filed EIN '+t['ein']+'. Mission and website reviewed; reflects the return reporting period.'})
 o={field:v.get(field,'') for field in ['name','description','kind','website','identity_evidence']}
 o.update(ownership='Nonprofit / tax-exempt',status='sourced',review_outcome='partial',website_status='filed' if o['website'] else 'unresolved',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved',notes='Individual review of IRS identity, tax-return activity, House disclosure and organization website where available. Original filing names remain searchable. Related legal entities remain separate; tax information reflects its reporting period.',sources=[])
 if k=='ab79082827d5e29e':
  ss=[s for s in ss if 'irs.gov' not in s.get('url','').lower() and 'propublica.org' not in s.get('url','').lower()];ss.append({'url':'https://www.carpenters.org/','label':'Union official website','claim':'Identifies the United Brotherhood of Carpenters and Joiners of America and describes worker representation and training.'});o.update(description='Labor union representing carpenters and related construction workers through collective bargaining, training, and worker advocacy.',website='https://www.carpenters.org/',kind='Labor union',ownership='Not applicable',identity_evidence='House disclosures identify the national union. The automatically joined EIN 52-6799457 belongs to an industry training alliance and was rejected. Official union website independently supports identity.');o['notes']+=' Rejected the automatic tax-return join to International Standards and Training Alliance; its mission and EIN are not assigned to the union.'
 if k=='55e9b71e150fcb1d':
  o.update(name='Innovative Payments Association',website='https://www.ipa.org/',identity_evidence='House testimony identifies IPA as formerly NBPCA; current organization website is ipa.org.');ss.append({'url':'https://www.govinfo.gov/content/pkg/CHRG-116hhrg42795/pdf/CHRG-116hhrg42795.pdf','label':'Association congressional testimony','claim':'IPA testimony explicitly states formerly NBPCA on page 120.'})
 if k=='7e8060a02bb9b594':
  ss=[s for s in ss if 'propublica.org' not in s.get('url','')];o['notes']+=' The fetched tax return names Northeast Consumers Electric Systems; its exact legal relationship remains unconfirmed and the return is not used as proof of this association identity.'
 if k=='9d6b171bf7aec95e':
  o.update(name='Steel Tank Institute / Steel Plate Fabricators Association',description='Trade association representing fabricators of steel storage tanks, water pipes, pressure vessels, and related steel-plate products.',website='https://stispfa.org/');ss.append({'url':'https://members.stispfa.org/','label':'Official association directory','claim':'Identifies Steel Tank Institute/Steel Plate Fabricators Association and its steel fabrication membership.'})
 for s in ss:
  if not s.get('url'):continue
  u=urllib.parse.urlsplit(s['url']);url=urllib.parse.urlunsplit((u.scheme.lower(),u.netloc.lower(),u.path,u.query,u.fragment));claim=s.get('claim',s.get('claims',s.get('excerpt','')))
  if claim:o['sources'].append({'url':url,'label':s.get('label','Organization evidence'),'claim':claim})
 cp=r/'website-cache'/f'{k}.json';c=json.load(open(cp)) if cp.exists() else {}
 def norm(u):
  q=urllib.parse.urlsplit(u);return(q.hostname or '',q.path.rstrip('/'))
 if o['website'] and norm(c.get('requested_url',''))==norm(o['website']) and c.get('http_status')==200 and len(c.get('text',''))>150:
  o.update(website=c.get('final_url',o['website']),website_status='verified',review_outcome='confirmed')
  a=audits.get(k,{})
  if a.get('status',a.get('decision'))=='keep' and c.get('logo_http_status')==200:
   candidate=a.get('replacement_candidate_url') or a.get('replacement_candidate') or a.get('logo_url') or c.get('logo_url','')
   if candidate==c.get('logo_url'):
    for field in ['logo_url','logo_kind','logo_source_url']:o[field]=c.get(field,'')
    o['logo_status']='official_site_asset'
  o['sources'].append({'url':o['website'] if o['website'].startswith('https://') else c['requested_url'],'label':'Official organization website','claim':'Page identity and activities checked against the disclosed organization on 2026-09-05.'})
 if k=='7e8060a02bb9b594':o['review_outcome']='partial'
 if k=='cb1832e51c4d80ad':o.update(review_outcome='partial',website='',website_status='unresolved',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved');o['notes']+=' Seattle nonprofit; current programs and official website unresolved. No match to the Toronto arts organization is asserted.'
 if not o['identity_evidence']:o['identity_evidence']='IRS EIN '+t['ein']+' reviewed with House disclosure and tax-return activity; aliases and parent identity are not inferred.'
 o['name']=re.sub(r'\b(Of|For|The|And|ON|IN|AT|TO)\b',lambda m:m[0].lower(),o['name'])
 for a,b in {'international':'International','institute':'Institute','internet':'Internet','industry':'Industry','inc.':'Inc.','NEW':'New','LAW':'Law','BAR':'Bar','ART':'Art','OUR':'Our','ONE':'One','OIL':'Oil','GAS':'Gas','WAY':'Way','TAX':'Tax'}.items():o['name']=re.sub(r'\b'+re.escape(a)+r'\b',b,o['name'])
 o['name']=o['name'].replace("Children'S","Children’s").replace("America'S","America’s").replace(' inc.',' Inc.')
 o['name']=o['name'][0].upper()+o['name'][1:]
 assert o['sources'] and len(o['description'])>25,(k,o['description']);out[k]=o
names={'cfe0835915f18fde':'NMDP','74b30fa4fea2bd57':'NatureServe','8c0026741eb4f46d':'NCTA – The Internet & Television Association','f13696488bd16265':'NextOp','988b029271c316af':'NumbersUSA Action','d4db71eecc1adeea':'PATH','a39f20af2278bf3b':'PKD Foundation','c2d066a6bd84872c':'ReFED','75881ff6fbdeef22':'SAM Action','dfc7c211aaf9e229':'SCAN Health Plan','77c43aa5a725f6bc':'SEMI','86d35d246cf46a2e':'SNAC International','d837664d2f0969e2':'SourceAmerica','68c76011e5d2edfe':'StoryCorps','912af2bedb709a52':'TruMerit','a5252f786da1475e':'UCAN','8e15851d1e31f065':'URAC','6ee0e062adca7af1':'UsAgainstAlzheimer’s','e60196c0f600afb5':'WellSpan Health','87c320bb87910f70':'Wellstar Health System','da18c2d9a1be8bb8':'XR Association','93ec3b27c1d5c54b':'YMCA of Greater Cleveland','746e82ce5918a311':'YWCA Clark County','bb2e5493498552da':'ZERO TO THREE'}
for k,n in names.items():out[k]['name']=n
for k in ['98fd08285a4b2ef7','6afdab3684d92477','bd25d5c4e949fedf','f5ff5511bc322955','b6dc9112ff32b65d','baf3cdce0816212d','3e53227fa4b0619c','561e90c73e2ac200','6945f14d42065556','5131ee0bfede7fd1','d5c828ff213e8908','a9fda42d550dae93','b36b4c80d1268598','8a9ed020e9fb3fe0']:out[k]['featured']=True
assert set(out)==set(inputs) and len(out)==325
(r/'irs-round4-325-root-draft.json').write_text(json.dumps(out,indent=2)+'\n');print(len(out),collections.Counter(x['review_outcome'] for x in out.values()))
