import json,pathlib,copy,csv
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));e=json.load(open(r/'identity204-sbir-evidence.json'));rows=list(csv.DictReader(open(r/'sbir-awards-no-abstract.csv',encoding='utf-8-sig')))
keys={'13e19285103276dd':'FLUXWORKS','3c9c3e42e6fcfe36':'EMPOWER EQUITY','89019dadeca1bce5':'EXOANALYTIC','4d51583f0100224f':'KNOWMADICS','540b1e3ac6baf821':'VANNEVAR','61806bad46ad4568':'X-BOW'}
assert not (r/'featured206-before.json').exists();before={};dec=[]
for i,k in keys.items():
 v=p[i];before[i]=copy.deepcopy(v);a=max([x for x in rows if k in x['Company'].upper()],key=lambda x:x['Award Year']);ev=next(x for x in e if x['id']==i)
 n=f"Official SBIR award export names {a['Company']} (UEI {a['UEI']}) in {a['City']}, {a['State']}, and links {a['Company Website']}. This supports the legal identity behind the existing operating name and domain. Ownership, intermediary relationships and existing activity descriptions are preserved from the prior review."
 v.update(review_outcome='confirmed',checked_at='2026-09-13',identity_evidence=n,notes=before[i]['notes']+' '+n)
 v['sources'].append(dict(url='https://data.www.sbir.gov/mod_awarddatapublic_no_abstract/award_data_no_abstract.csv',label='SBIR official award data: '+a['UEI'],claim=n))
 dec.append(dict(id=i,decision='confirmed_identity_only',record={k:a[k] for k in ['Company','Company Website','UEI','Award Year','City','State','Award Title']},portfolio_url=ev['sbir_url'],notes=n))
for k,v in [('before',before),('decisions',dec)]: (r/f'featured206-{k}.json').write_text(json.dumps(v,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('Saved 6 identity confirmations')
