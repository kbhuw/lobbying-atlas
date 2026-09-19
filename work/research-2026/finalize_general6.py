import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round6-90-draft.json'));ev=json.load(open(r/'general6-public-evidence.json'))
for k,e in ev.items():
 v=p[k]
 for s in e['sources']:v['sources'].append(dict(url=s['url'],label=s['label'],claim=s['claims']+' '+e['claim']))
 if k=='8002d7e31b84a6f5':v.update(ownership='Unknown',review_outcome='partial');v['notes']+=' The NYSE: AB listing applies to AllianceBernstein Holding L.P.; the filing’s shortened name does not by itself distinguish that issuer from the operating partnership.'
 if k=='316284b0a1f8c7fe':v['notes']+=' The filed name is the historical Allegheny Technologies name; current company branding is ATI.'
(r/'general-round6-90-draft.json').write_text(json.dumps(p,indent=2)+'\n')
s=(r/'build_general5.py').read_text().replace('general-round5','general-round6');start=s.index('hold=');end=s.index('\nfor k,v',start);s=s[:start]+"hold={'78a1614d1c961b95','6d9a189ac5c80304','8ae14d5fcc44aade','5969daadb5543011','8c7a46fde006d718','9fd9e854b17e4de4','fb1ade9ad95abd4f','ec78a0a25b0d8b39','e4b647b42ca664c5'}"+s[end:];(r/'build_general6.py').write_text(s)
