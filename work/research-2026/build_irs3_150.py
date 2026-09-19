import json,pathlib,re,urllib.parse,collections
r=pathlib.Path('work/research-2026')
def read(f):return json.load(open(r/f))
def keyed(d):return {v['id']:v for v in d} if isinstance(d,list) else d
p={**keyed(read('irs-round3-b-researched.json')),**keyed(read('irs-round3-c-correct-researched.json'))}
inputs={x['id']:x for l in 'bc' for x in read(f'irs-round3-{l}-correct-input.json')}
assert set(p)==set(inputs)
fixes=keyed(read('irs-round3-c-specific-corrections.json')['records'])
bf=r/'irs-round3-b-specific-facts.json'
if bf.exists():
 d=read(bf.name);fixes.update(keyed(d.get('records',d)))
audit={**read('irs-round3-b-branding-audit.json'),**keyed(read('irs-round3-c-branding-audit.json')['records'])}
out={}
for k,v in p.items():
 v=v.copy();f=fixes.get(k,{})
 for field in ['name','description','website','identity_evidence']:
  if f.get(field):v[field]=f[field]
 ss=v.get('sources',[])+f.get('sources',[]);t=inputs[k]['tax_return']
 ss.append({'url':t['source_url'],'label':'Organization Form 990','claim':'Filed organization '+t.get('organization_name','')+'; EIN '+t['ein']+'. Mission and filed website reviewed; reflects return reporting period.'})
 o={field:v.get(field,'') for field in ['name','description','kind','website','identity_evidence']}
 o.update(ownership='Nonprofit / tax-exempt',status='sourced',review_outcome='partial',website_status='filed' if o['website'] else 'unresolved',checked_at='2026-09-05',as_of='2026-09-05',featured=False,legal_form='',logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved',notes='Individual review of tax-return activity, IRS identity, House disclosure and official website where available. Original filing names remain searchable; related legal entities are kept separate. Tax information reflects its reporting period.',sources=[])
 for s in ss:
  if not s.get('url'):continue
  u=urllib.parse.urlsplit(s['url']);url=urllib.parse.urlunsplit((u.scheme.lower(),u.netloc.lower(),u.path,u.query,u.fragment))
  claim=s.get('claim',s.get('claims',s.get('excerpt','')))
  if claim:o['sources'].append({'url':url,'label':s.get('label','Organization evidence'),'claim':claim})
 cp=r/'website-cache'/f'{k}.json';c=json.load(open(cp)) if cp.exists() else {}
 def norm(u):
  q=urllib.parse.urlsplit(u);return(q.hostname or '',q.path.rstrip('/'))
 if o['website'] and norm(c.get('requested_url',''))==norm(o['website']) and c.get('http_status')==200 and len(c.get('text',''))>150:
  o.update(website=c.get('final_url',o['website']),website_status='verified',review_outcome='confirmed')
  a=audit.get(k,{})
  if a.get('status',a.get('decision'))=='keep' and c.get('logo_http_status')==200:
   candidate=a.get('replacement_candidate_url') or a.get('replacement_candidate') or a.get('logo_url') or c.get('logo_url','')
   if candidate==c.get('logo_url'):
    for field in ['logo_url','logo_kind','logo_source_url']:o[field]=c.get(field,'')
    o['logo_status']='official_site_asset'
  o['sources'].append({'url':o['website'],'label':'Official organization website','claim':'Page identity and activities reviewed against IRS and House organization evidence on 2026-09-05.'})
 if not o['identity_evidence']:o['identity_evidence']='IRS EIN '+t['ein']+' reviewed with House disclosure identity and tax-return activity; historical aliases or parent identities are not inferred.'
 o['name']=re.sub(r'\b(Of|For|The|And|ON|IN|AT)\b',lambda m:m[0].lower(),o['name'])
 for a,b in {'international':'International','independent':'Independent','institute':'Institute','internet':'Internet','infirmary':'Infirmary','inc.':'Inc.','NEW':'New','LAW':'Law','BAR':'Bar'}.items():o['name']=re.sub(r'\b'+re.escape(a)+r'\b',b,o['name'])
 if o['name']:o['name']=o['name'][0].upper()+o['name'][1:]
 assert o['sources'] and len(o['description'])>25;out[k]=o
for k,n in {'b2ad0a1c8de31e97':'HIV and Hepatitis Policy Institute','cb7cf65536feffc2':'Hazelden Betty Ford Foundation','68ef5e16d4ba0f59':'Hire Heroes USA','eb9aa24ee970c3a6':'I AM ALS','8881739e1b8877a1':'InspiriTec','c6be42a9cb956dae':'KC2026','c4a58742cdc223ce':'MRIGlobal','ed260bdbac8367dd':'MultiCare Health System','81585b04b170a991':'NY CREATES','c6002f2ef60ba7ea':'NEW Health Programs Association','8653fb52c441fd75':'Nicklaus Children’s Health System','925dc5346f5c0226':'Marion Health','9e75f4faceacb775':'League of American Bicyclists'}.items():out[k]['name']=n
out['87653e15f7ab37ea']['description']='Education association representing education research and service organizations and advocating for the use of research evidence in K–12 policy and practice.'
out['871d63d7f40eca4d']['description']='Nonprofit health system in Osage Beach, Missouri, serving the Lake of the Ozarks region through a hospital, clinics, pharmacies, rehabilitation, and hospice services.'
for k in ['cb7cf65536feffc2','2fe8840f88df0ad3','59a6aab065297411','9d354046279f15b2','731a910d142879c8','efe7bfed9c6e775e']:out[k]['featured']=True
for k in ['dcaa806d13023aa0','80b9ff03d95b9d74','a6c95bf0a472f309','ba8aeee6eac76de7']:
 out[k].update(logo_url='',logo_kind='',logo_source_url='',logo_status='unresolved',review_outcome='partial')
 out[k]['notes']+=' Website branding presents a wider or differently named organization; exact branding relationship remains unconfirmed.'
for v in out.values():
 v['name']=v['name'].replace("Women'S","Women's").replace(' inc.',' Inc.').replace(' officers ',' Officers ')
assert len(out)==150
(r/'irs-round3-rootchecked-draft.json').write_text(json.dumps(out,indent=2)+'\n')
print(len(out),collections.Counter(x['review_outcome'] for x in out.values()))
