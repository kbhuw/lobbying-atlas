import json,pathlib,copy
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));a={x['id']:x for x in json.load(open(r/'sbir-domain-candidates215.json'))};sel=json.load(open(r/'sbir215-selected.json'));exclude={'c82c30dc33170b85','55da7836624ea5c4'};assert not (r/'featured215-before.json').exists();before={};dec=[]
for i in sel:
 if i in exclude:continue
 v=p[i];x=a[i];assert len(x['records'])==1;row=x['records'][0];before[i]=copy.deepcopy(v)
 n=f"Official SBIR award data explicitly links {row['Company']} (UEI {row['UEI']}) in {row['City']}, {row['State']}, to {row['Company Website']}, the same domain as the existing organization profile. This corroborates the legal name behind the disclosed operating label. Identity confirmed; ownership and current website-availability assessments remain separate."
 if i=='27d0143d732d61d0':n+=' This specifically establishes Ouraring Inc. at the Oura domain; it does not equate Ouraring Inc. with Oura Inc. or Oura Health Oy.'
 v.update(review_outcome='confirmed',status='sourced',checked_at='2026-09-13',identity_evidence=n,notes=n);v['sources'].append(dict(url='https://data.www.sbir.gov/mod_awarddatapublic_no_abstract/award_data_no_abstract.csv',label='SBIR exact legal-name/domain evidence: '+row['UEI'],claim=n));dec.append(dict(id=i,decision='confirmed_identity_only',record=row,previous_notes=before[i]['notes'],notes=n))
assert len(dec)==34
for k,v in [('before',before),('decisions',dec)]: (r/f'featured215-{k}.json').write_text(json.dumps(v,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
f=pathlib.Path('lobbying-map/research/publication-metadata.json');m=json.load(open(f));n=sum(v['status']=='unresolved' for v in before.values());m['counts']['unresolved']-=n;m['counts']['sourced']+=n;f.write_text(json.dumps(m,indent=2)+'\n');print('Saved 34 identities; old unresolved statuses',n)
