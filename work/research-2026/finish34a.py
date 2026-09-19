import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'research34a_root.py').read_text());index={x['id']:i for i,x in enumerate(rows)}
for file in ['round34a-first10-evidence.json','round34a-last10-evidence.json']:
 for k,v in json.load(open(r/file)).items():
  i=index[k];name=v['name'];notes=v['notes'];own='Unknown';outcome=None
  if i in [1,8]:own='Subsidiary'
  if i==3:own='Government body'
  if i==7:own='Government body';outcome='partial';notes+=' Government ownership describes the garden property; nonprofit operation belongs to the Chicago Horticultural Society. These roles are not interchangeable.'
  if i in [20,21,23,26,27,28,29]:own='Nonprofit / tax-exempt'
  if i==0:own='Subsidiary';outcome='partial';notes+=' Filing uses Company LP while the parent source names Company LLC. The brand is the Chevron/Phillips joint venture; exact LP-to-LLC legal relationship and direct ownership percentages are unverified. Ownership left unknown for the exact filing label.'
  if i==1:name='Chevron U.S.A. Inc.';notes+=' Parent issuer ticker is not assigned to this operating subsidiary.'
  if i==2:name='Chey Institute for Advanced Studies'
  if i==4:own='Private company';outcome='partial';notes='Leonard Green lists CHG Healthcare Services as a current buyout investment. Current full investor ownership percentages and the precise legal entity behind the shortened filing name remain unverified.'
  if i==5:outcome='unresolved';notes+=' Business description is self-reported in lobbying disclosures; external identity not independently established.'
  if i==6:outcome='partial';notes+=' Filing spelling Advisors differs from official legal Advisers; exact equivalence remains partial.'
  if i==9:name='Chickasaw Inkana Foundation on behalf of the Chickasaw Nation';notes+=' Composite label retains foundation and tribal government roles; ownership left unknown for the combined entry.'
  if i==21:name='Children and Screens: Institute of Digital Media and Child Development'
  if i==22:name="Children’s Cancer Cause";own='Nonprofit / tax-exempt';notes='Current name Children’s Cancer Cause; official audited financial statement identifies 501(c)(3) status. Original filing variant preserved.'
  if i==23:name="Children’s Healthcare of Atlanta"
  if i in [24,25]:name="Children’s Hospital Association";outcome='partial'
  if i==26:name="Children’s Hospital Association of Texas"
  if i==27:name="Boston Children’s Hospital"
  if i==28:name="Children’s of Alabama"
  if i==29:name="Children’s Hospital of The King’s Daughters"
  sources=list(v['sources'])
  if i==4:sources.append(dict(url='https://www.leonardgreen.com/portfolio/',claim='Investor Leonard Green lists CHG Healthcare Services as a current buyout investment.'))
  if i==22:sources.append(dict(url='https://www.childrenscancercause.org/s/CCC-Financial-Statements-6-30-24.pdf',claim='Official audited financial statement identifies The Children’s Cancer Cause Inc as a 501(c)(3) tax-exempt nonprofit.'))
  if i==0:
   notes='EPA identifies the LP as a wholly owned subsidiary of Chevron Phillips Chemical Company LLC. The joint-venture shareholders hold the LLC, not direct stakes asserted here in the LP. Historical relationship established; latest intermediate ownership details remain partial.'
   sources.append(dict(url='https://www.epa.gov/enforcement/chevron-phillips-chemical-company-clean-lp-air-act-settlement',claim='EPA identifies Chevron Phillips Chemical Company LP as wholly owned by Chevron Phillips Chemical Company LLC.'))
  add(i,name,v['description'],v.get('website') or '',kind=v['kind'],own=own,sources=[(s['url'],s['claim']) for s in sources],notes=notes,outcome=outcome,featured=i in [0,1,7,20,23,27])
assert len(p)==30
(r/'general-round34a-root-draft.json').write_text(json.dumps(p,indent=2)+'\n');print('30 drafts assembled')
(r/'check_general34a.py').write_text((r/'check_general33c.py').read_text().replace('33c','34a'))
s=(r/'build_general33c.py').read_text().replace('33c','34a').replace('general-round33-c-input','general-round34-a-input');start=s.index('hold=');end=s.index('\n',start);s=s[:start]+"hold={rows[i]['id'] for i in [0,1,6,9,11,12]}"+s[end:];(r/'build_general34a.py').write_text(s)
