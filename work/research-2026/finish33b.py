import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'research33b_root.py').read_text());index={x['id']:i for i,x in enumerate(rows)}
add(17,'Charter Brokerage','Provides customs brokerage, duty drawback recovery and international trade services to importers and exporters.','https://charterbrokerage.net/',kind='Customs brokerage company',own='Subsidiary',sources=[('https://charterbrokerage.net/customs-broker/','Official company profile describes customs brokerage and duty drawback recovery services.'),('https://www.berkshirehathaway.com/news/dec1214.pdf','Berkshire Hathaway announced its acquisition of Charter Brokerage in December 2014.'),('https://www.berkshirehathaway.com/2023ar/202310-k.pdf','2023 subsidiary exhibit includes Charter Brokerage Holdings Corp.')],notes='Historical Berkshire acquisition is established; latest exact direct ownership chain is not. Charter Brokerage Services remains a separate filing label pending legal-entity equivalence evidence.',outcome='partial')
add(18,'Charter Brokerage Services','Federal lobbying client represented by Jones Walker on trade and tax matters; the same name appears among Duty Drawback Coalition members.','',kind='Trade services client',sources=[('https://downloads.regulations.gov/USTR-2018-0035-0159/attachment_1.pdf','Appendix A of Jones Walker 2018 USTR submission lists Charter Brokerage Services LLC as a Duty Drawback Coalition member.')],notes='Likely related to the Charter Brokerage customs-services business, but exact legal equivalence and current ownership are not established. Kept separate; website and logo withheld.',outcome='partial')
for file in ['round33b-first10-evidence.json','round33b-last10-evidence.json']:
 for k,v in json.load(open(r/file)).items():
  i=index[k];name=v['name'];desc=v['description'];web=v.get('website') or '';notes=v['notes'];sources=v['sources'];kind=v['kind'].replace('Public ','');own='Unknown';outcome=None
  if i in [1,9]:own='Not applicable'
  if i in [2,7,21]:own='Subsidiary'
  if i==5:own='Private company';name='Chapter (Memoir, Inc.)'
  if i==20:own='Publicly traded';desc=desc.removeprefix('Public ');desc=desc[0].upper()+desc[1:]
  if i in [25,29]:own='Nonprofit / tax-exempt'
  if i==0: name='Changent';desc='National organization supporting Child First and Nurse-Family Partnership programs for children and families.'
  if i==2:outcome='partial';notes+=' Ownership evidence includes historical government records; exact current direct chain not independently verified.'
  if i==4:outcome='partial';notes+=' Exact legal-name equivalence with the Group brand remains uncertain.'
  if i==6:name='Character.ai (Character Technologies, Inc.)'
  if i==7:
   name='ChargePoint, Inc.';sources=[s for s in sources if 'stock-information' not in s['url']];notes='ChargePoint Inc is the operating subsidiary of ChargePoint Holdings Inc. The parent issuer ticker is not assigned to this client. Latest filing reports termination with no activity.'
  if i==8:
   sources=[s for s in sources if 'govchime.com' not in s['url']];notes='Official website describes tactical power systems. Current ownership not established; exact legal name is preserved from the LDA filing.'
  if i==9:outcome='unresolved'
  if i==25:name='CharterCARE Health of Rhode Island'
  if i==26:name='ChartSpan'
  if i==27:name='Chartwell Strategy Group on behalf of EFC and MEFA'
  if i==28:name='Chartwell Strategy Group on behalf of Hyundai Motor Company';notes+=' Ownership is left unknown for this composite filing label; Hyundai public-issuer evidence applies to the represented company only.'
  if i==29:name='CHAS Health'
  add(i,name,desc,web,kind=kind,own=own,sources=[(s['url'],s['claim']) for s in sources],notes=notes,outcome=outcome,featured=i in [1,3,5,6,7,20])
assert len(p)==30
(r/'general-round33b-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
(r/'check_general33b.py').write_text((r/'check_general33a.py').read_text().replace('33a','33b'))
s=(r/'build_general33a.py').read_text().replace('33a','33b');start=s.index('hold=');end=s.index('\n',start);s=s[:start]+"hold={rows[i]['id'] for i in [4,7,11,13,18,21,24,27,28]}"+s[end:];s=s.replace("# Hold parent", "rows=json.load(open(r/'general-round33-b-input.json'))\n# Hold parent")
(r/'build_general33b.py').write_text(s)
print('30 drafts assembled')
