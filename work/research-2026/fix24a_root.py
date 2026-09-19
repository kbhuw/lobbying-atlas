import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round24-a-researched.json'));i={v['id']:v for v in json.load(open(r/'general-round24-a-input.json'))}
fixes={
'119bf73034cd1790':('https://www.blueearthdiagnostics.com/about','Molecular imaging company developing PET radiopharmaceuticals to diagnose disease and guide treatment.','Subsidiary of private or public company','The current company About page identifies Blue Earth Diagnostics as a subsidiary of Bracco Imaging and describes its molecular-imaging products.'),
'4ddd45e0e0b04dcd':('https://blueforcegear.com/about_us/','Manufactures weapon slings, lightweight load-carrying equipment, and tactical gear for military, law-enforcement, and civilian users.','Unknown','The official About page identifies Blue Force Gear and its weapon slings and load-carrying equipment.'),
'592bf2be4df99c45':('https://www.bluestarnbr.com/about-1','Develops domestic production of nitrile-butadiene rubber used to manufacture medical gloves.','Unknown','The company About page describes its goal of domestic NBR production for medical gloves.'),
'6bba8616a65759de':('https://blueskyinfrastructure.com/about-blue-sky-infrastructure/','Develops infrastructure to capture, transport, and permanently store industrial carbon dioxide underground.','Private company','The official company page identifies the Houston CO2 infrastructure business as a Blackstone portfolio company.')}
for k,(u,d,o,c) in fixes.items():
 v=p[k];v.update(website=u,description=d,kind='Business',ownership=o,review_outcome='partial',identity_evidence=c,notes='Official operating website established; exact legal ownership details may remain unresolved.');v.setdefault('sources',[]).append(dict(url=u,label='Official company information',claim=c))
p['77aa8568273eef69']['website']='https://www.floridablue.com/'
p['77aa8568273eef69'].setdefault('sources',[]).append(dict(url='https://myfloridacfo.com/division/consumers/purchasingInsurance/small-group-market-carrier-list-2026',label='Florida Department of Financial Services 2026 carrier list',claim='Lists Blue Cross Blue Shield of Florida dba Florida Blue and its official website floridablue.com.'))
for k,v in p.items():
 v.setdefault('sources',[])
 for s in (i[k].get('profile') or {}).get('sources',[]):
  if s not in v['sources']:v['sources'].append(s)
 if v.get('ownership')=='Unknown':v['review_outcome']='partial'
(r/'general-round24-a-rootchecked.json').write_text(json.dumps(p,indent=2)+'\n')
