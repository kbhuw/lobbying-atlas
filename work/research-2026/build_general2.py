import json,pathlib,re,urllib.parse,collections
r=pathlib.Path('work/research-2026')
def read(n):return json.load(open(r/n))
def keyed(d):
 if isinstance(d,dict):
  for t in ['records','profiles','corrections']:
   if t in d:d=d[t];break
 return {v['id']:v for v in d} if isinstance(d,list) else d
p=read('general-round2-90-draft.json');p.update(keyed(read('general-round2-c-specific-corrections.json')))
for f in ['general-round2-a-extra-corrections.json','general-round2-b-ownership-corrections.json','general-round2-b-identity-corrections.json']:
 for k,fix in keyed(read(f)).items():
  v=p[k];ss=v.get('sources',[])+fix.get('sources',[])
  if fix.get('source'):ss.append(fix['source'])
  for field in ['name','description','kind','ownership','website','review_outcome','identity_evidence','notes']:
   if field in fix:v[field]=fix[field]
  if fix.get('status') in ['partial','unresolved']:v['review_outcome']=fix['status']
  if fix.get('identity_note'):v['identity_evidence']=fix['identity_note']
  if fix.get('evidence_excerpt') and fix.get('website'):ss.append(dict(url=fix['website'],claim=fix['evidence_excerpt'],label='Official page evidence'))
  v['sources']=ss

def add(k,url,claim):p[k]['sources'].append(dict(url=url,label='Primary organization evidence',claim=claim))
p['6cfb28d395b2c1ce']['ownership']='Publicly traded';add('6cfb28d395b2c1ce','https://www.acadiahealthcare.com/investors/','NASDAQ: ACHC. Official 2026 investor page identifies the behavioral-health company and its listing.')
for k in ['1437ae0ab2adbc84','26afccd998b9fde7']:
 p[k]['legal_form']='Public benefit corporation';p[k]['ownership']='Private company';add(k,'https://industryinsights.act.org/2024/05/act-completes-formation-partnership-nexus','ACT announced completed formation of ACT Education Corp., a Delaware public benefit corporation, and closed its partnership with private equity firm Nexus in May 2024. Public benefit describes its legal form, not a stock exchange listing.')
 p[k]['description']='Provides the ACT college-admissions test, workforce-readiness credentials, and related education assessments. ACT Education Corp. became a public benefit corporation in 2024.'
for k,t in [('5e3c36f67d1eb334','NYSE: ACN'),('079798d2de7b5323','NYSE: ACH'),('71640d9d5058a166','NYSE: ACH'),('47b81cb9ef8b1897','NASDAQ: ARAY'),('62852ee869cfbc8d','NYSE AMERICAN: ACU')]:
 p[k]['ownership']='Publicly traded'
 for s in reversed(p[k]['sources']):
  if any(w in s['claim'].upper() for w in ['TICKER','SYMBOL','NASDAQ:']):s['claim']=t+'. '+s['claim'];break
# Generic names without a demonstrated legal-entity match must not inherit a convenient website.
for k in ['51020b75a1b716c6','cdc4bc5e15575c69','693b72a5457be5c4']:
 v=p[k];v.update(website='',ownership='Unknown',kind='Unknown',review_outcome='unresolved');v['sources']=[s for s in v['sources'] if 'lda.gov' in s['url'] or 'house.gov' in s['url']];v['description']='Disclosed as '+v['name']+'. The exact organization, current activities, and official website remain unconfirmed.'
# Achieve finance group is supported by California consumer-finance filing and current primary brand disclosures.
k='4228cb17ea6c1892';v=p[k];v.update(name='Achieve',description='Digital personal-finance group offering personal loans, home-equity loans, and debt-relief services. The brand covers several affiliated businesses.',kind='Consumer financial services',ownership='Unknown',website='https://www.achieve.com/',review_outcome='partial',identity_evidence='LDA client 72212 reports California consumer financial services. Current Achieve site matches that activity and location, but the exact affiliate behind the short disclosed name remains unresolved.');v['sources']=[s for s in v['sources'] if 'lda.gov/' in s['url']];add(k,'https://www.achieve.com/about/achieve-and-freedom-debt-relief','Achieve describes its financial-services brands and affiliates and identifies Freedom Debt Relief in San Mateo, California.')
k='7f044f25fa2a2f11';p[k].update(name='ACCUS (Automobile Competition Committee for the United States)',description='Umbrella organization for U.S. motor-racing sanctioning bodies, representing the United States within the FIA and coordinating international motorsport matters.',website='https://accusfia.us/',kind='Motorsport association',ownership='Unknown',review_outcome='partial',identity_evidence='GAO lists ACCUS as an Ogilvy lobbying client; current FIA and ACCUS sources identify the U.S. motorsport organization. Historical legal-name continuity remains partially checked.')
add(k,'https://www.gao.gov/pdf/product/653471','GAO lobbying-disclosure audit lists Ogilvy Government Relations representing ACCUS.')
add(k,'https://accusfia.us/','Official ACCUS site identifies the Automobile Competition Committee for the United States and its FIA role and motorsport members.')
k='75ad69d7586c3d7e';p[k].update(description='Lobbying client disclosed only as ACP, with an advocacy description and New York location. Its full organization name and official website remain unresolved.',website='',kind='Unknown',ownership='Unknown',review_outcome='unresolved',identity_evidence='LDA client 72839 does not establish a link to either the physician association or Associated Church Press. Both guessed matches excluded.');p[k]['sources']=[s for s in p[k]['sources'] if 'lda.gov/' in s['url']]
k='287540bfab4b90d9';p[k]['ownership']='Unknown';add(k,'https://eqtgroup.com/news/eqt-to-acquire-a-majority-stake-in-acronis-a-leading-cybersecurity-and-data-protection-platform-for-managed-service-providers-and-corporate-it-departments-2024-08-07','EQT announced a proposed majority acquisition in August 2024, pending approvals. This announcement alone does not establish completion or current ownership; the unsupported public-company classification was removed.')
k='4f7721a782641411';p[k]['description']='Provides aircraft avionics, pilot training and simulators, and flight-data analysis. Formed from the former L3Harris Commercial Aviation Solutions business.';p[k]['ownership']='Portfolio company of TJC';add(k,'https://acronaviation.com/about-us/','Official company history identifies sale of L3Harris Commercial Aviation Solutions to TJC to create Acron Aviation.')
audits={}
for f in ['general-round2-a-branding-root-audit.json','general-round2-b-branding-audit.json','general-round2-c-branding-audit.json']:audits.update(keyed(read(f)))
for k,v in p.items():
 v.pop('id',None);v.update(status='unresolved' if v['review_outcome']=='unresolved' else 'sourced',as_of='2026-09-05',checked_at='2026-09-05',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved')
 v.setdefault('featured',False);v.setdefault('legal_form','');v.setdefault('notes','Individual review with original filing names retained.')
 if v['ownership']=='Nonprofit':v['ownership']='Nonprofit / tax-exempt'
 if v['ownership']=='Privately held':v['ownership']='Private company'
 c=read(f'website-cache/{k}.json') if (r/f'website-cache/{k}.json').exists() else {}
 def norm(u):
  a=urllib.parse.urlsplit(u or '');return a.hostname,a.path.rstrip('/')
 same=v.get('website') and norm(v['website']) in [norm(c.get('requested_url')),norm(c.get('final_url'))]
 v['website_status']='partial' if v.get('website') else 'unresolved'
 if v['review_outcome']=='unresolved':v['website']='';v['website_status']='unresolved'
 elif same and c.get('http_status')==200 and len(c.get('text',''))>150:
  v['website_status']='verified';a=audits.get(k,{})
  if a.get('decision')=='keep' and a.get('logo_url')==c.get('logo_url') and c.get('logo_http_status')==200 and c.get('logo_url','').startswith('https://'):
   for f in ['logo_url','logo_kind','logo_source_url']:v[f]=c[f]
   v['logo_status']='official_site_asset'
 elif v['review_outcome']=='confirmed':v['review_outcome']='partial'
 v['sources']=[dict(url=s['url'],claim=s['claim'],label=s.get('label','Organization evidence')) for s in v['sources']]
 if k=='51020b75a1b716c6' and not v['sources']:v['sources']=[dict(url='https://www.accessservices.org/about/',label='Unconfirmed candidate excluded',claim='This page identifies an Eastern Pennsylvania nonprofit. A link to the disclosed Access Services entity has not been established, so its identity, ownership, website, and logo are not assigned.')]
 assert v['sources'] and v['identity_evidence'] and len(v['description'])>25,k
 assert all(s['url'].startswith('https://') and s['claim'] for s in v['sources']),k
 if ' OBO ' in v['name'] or ' ON Behalf Of ' in v['name']:v['name']=v['name'].replace(' OBO ',' representing ').replace(' ON Behalf Of ',' representing ')
assert len(p)==90
(r/'general-round2-90-rootchecked.json').write_text(json.dumps(p,indent=2)+'\n');print(collections.Counter(v['review_outcome'] for v in p.values()),'logos',sum(bool(v['logo_url']) for v in p.values()))
