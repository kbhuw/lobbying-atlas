import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'research33c_root.py').read_text());index={x['id']:i for i,x in enumerate(rows)}
for file in ['round33c-first10-evidence.json','round33c-last10-evidence.json']:
 for k,v in json.load(open(r/file)).items():
  i=index[k];name=v['name'];notes=v['notes'];own='Unknown';outcome=None;sources=v['sources'];desc=v['description'];web=v.get('website') or ''
  if i in [0,3,23,28]:own='Government body'
  if i in [1,2,6,20]:own='Subsidiary'
  if i in [21,26]:own='Publicly traded'
  if i in [24,25,29]:own='Nonprofit / tax-exempt'
  if i==0:name='Chatham Area Transit Authority'
  if i in [1,2]:
   name='Chattem, Inc. d/b/a Opella';outcome='partial';notes+=' The quoted percentages describe the Opella group transaction, not direct share ownership of Chattem Inc. Exact intermediate ownership chain remains unverified.'
  if i==3:name='Chautauqua County, New York'
  if i==4:outcome='partial';notes+=' ContinueCare is the associated hospital brand; exact current website legal operator remains partial.'
  if i==5:outcome='partial';desc='Organization whose self-described profile identifies a network of federally qualified health centers serving Missouri patients.';notes+=' Network description is self-reported on LinkedIn, not independently established by a government record.'
  if i==6:name='CHCI Asset Management, LC';outcome='partial';notes+=' Subsidiary source is historical; current exact legal ownership chain not independently refreshed. Parent ticker not assigned.'
  if i==8:name='Checkmate Government Relations on behalf of Okapi Global LLC';notes+=' Wildlife-trade activity is self-reported in the LDA client description.'
  if i==9:name='Checkmate Government Relations on behalf of T1 Energy';desc='Government-relations intermediary Checkmate Government Relations representing T1 Energy, a solar manufacturing and energy business.';notes+=' Ownership left unknown for the composite filing; public listing pertains only to represented T1 Energy.'
  if i==21:name='Cheniere';own='Unknown';notes='LDA client 72170 identifies only CHENIERE, Texas, described as a liquefied natural gas company. This supports the group identity but not a particular legal subsidiary or the listed issuer. Parent investor sources are context only; public-company ownership is not assigned to the abbreviated client.';outcome='partial'
  if i==23:name='Chesapeake Bay Commission'
  if i==24:name='Chesapeake Bay Foundation'
  if i==26:
   sources=[dict(s,claim=s['claim'].replace('NYSE under ticker CPK','NYSE: CPK')) for s in sources]
  if i==27:name='Saint Louis Chess Club';own='Nonprofit / tax-exempt';notes='Missouri official tourism page identifies a 501(c)(3) educational organization. Current website uses Saint Louis Chess Club; the longer original filing name is preserved.'
  add(i,name,desc,web,kind=v['kind'],own=own,sources=[(s['url'],s['claim']) for s in sources],notes=notes,outcome=outcome,featured=i in [1,7,21,24,26,27])
assert len(p)==30
(r/'general-round33c-root-draft.json').write_text(json.dumps(p,indent=2)+'\n');print('30 drafts assembled')
(r/'check_general33c.py').write_text((r/'check_general33b.py').read_text().replace('33b','33c'))
s=(r/'build_general33b.py').read_text().replace('33b','33c').replace('general-round33-b-input','general-round33-c-input');start=s.index('hold=');end=s.index('\n',start);s=s[:start]+"hold={rows[i]['id'] for i in [1,2,4,6,8,9,16,17,20,21]}"+s[end:];(r/'build_general33c.py').write_text(s)
