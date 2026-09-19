import json,pathlib,copy
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));a={x['id']:x for x in json.load(open(r/'sbir-domain-candidates215.json'))};sel=json.load(open(r/'sbir216-selected.json'));skip={'0727872fc471ff78','01e060b95b89fe96','1f30b4f1d25f1996'};assert not (r/'featured216-before.json').exists();before={};dec=[]
names={'3df0151c698ebd50':'Seatrec Incorporated (via Jones Walker LLP)','9eb5eaa6909a4cdc':"Motiv Space Systems (via O’Brien, Gentry and Scott)",'adfa22ff032656c7':'HawkEye 360 (via Prasam / The Potomac Advocates)','9b1a48a82742a574':'Airloom Energy (via SBIR Advisors)','c7ade7da17fb2796':'Circle Optics Inc. (via SBIR Advisors)','6160b169209a0815':'Saltenna LLC (via SBIR Advisors)','1aa95def82bf10e3':'Sequoia Holdings (via SBIR Advisors)','846d355168b4131a':'SafeTraces (via The Livingston Group)','1cf176054341a40d':'Q-Net Security, Inc. (via The Roosevelt Group)','ce95af30fd55a3c9':'American Lithium Energy (via Thorn Run Partners)','cf69136208f9d5da':'Dayton T. Brown (via Thorn Run Partners)'}
for i in sel:
 if i in skip:continue
 v=p[i];x=a[i]['records'][0];before[i]=copy.deepcopy(v)
 n=f"The represented organization is corroborated by the SBIR record for {x['Company']} (UEI {x['UEI']}) and its explicit link to {x['Company Website']}. The intermediary relationship is retained as reported in the original lobbying label; the intermediary is not treated as an owner. Original filing IDs remain separate."
 v.update(review_outcome='confirmed',status='sourced',identity_evidence=n,notes=n,checked_at='2026-09-13');v['sources'].append(dict(url='https://data.www.sbir.gov/mod_awarddatapublic_no_abstract/award_data_no_abstract.csv',label='Federal identity evidence for represented client: '+x['UEI'],claim=n))
 if i in names:v['name']=names[i]
 dec.append(dict(id=i,decision='confirmed_represented_identity',record=x,previous_name=before[i]['name'],previous_notes=before[i]['notes'],name=v['name'],notes=n))
assert len(dec)==21
for k,v in [('before',before),('decisions',dec)]: (r/f'featured216-{k}.json').write_text(json.dumps(v,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
f=pathlib.Path('lobbying-map/research/publication-metadata.json');m=json.load(open(f));n=sum(v['status']=='unresolved' for v in before.values());m['counts']['unresolved']-=n;m['counts']['sourced']+=n;f.write_text(json.dumps(m,indent=2)+'\n');print('21 identities saved; renamed',len(names),'status updates',n)
