import json,pathlib
r=pathlib.Path('work/research-2026'); p=json.loads((r/'reviewed.json').read_text()); before={}; decisions=[]
def update(i,fields,sources):
 before[i]=p[i].copy();p[i].update(fields);p[i].update(checked_at='2026-09-13',as_of='2026-09-13',status='sourced')
 seen={s['url'] for s in p[i]['sources']}
 for s in sources:
  if s['url'] not in seen:p[i]['sources'].append(s);seen.add(s['url'])
 decisions.append({'id':i,'review_outcome':p[i]['review_outcome'],'notes':p[i]['notes']})
def src(url,claim):return {'url':url,'label':'Official organization evidence','claim':claim}
for d in json.loads((r/'featured73-first10.json').read_text()):
 i=d['originalID']; f=d['proposed'].copy();f['review_outcome']=d['decision'];f['website_status']='verified';f['identity_evidence']=d['evidence'];f['notes']=d['evidence']
 sources=[src(q['url'],q['quote']) for q in d['exact_quotes']]
 if i=='676b3d0c6d35fe4b':
  f.update(review_outcome='confirmed',description='Develops ground-based accelerators for hypersonic testing and future space launches.',notes='Official company page names Longshot Space Technologies in its copyright notice and describes its accelerator work. The filing uses this unsuffixed name; a legal suffix is not inferred.',identity_evidence='Official page copyright identifies Longshot Space Technologies; activity matches the filed space-technology name.')
  sources.append(src('https://longshotspace.com/company','Copyright notice names Longshot Space Technologies; page describes ground-based accelerators.'))
 if i=='70defc422a83b3b2':
  f.update(description='Helps medical, dental, and pharmaceutical suppliers sell to federal healthcare agencies.')
  sources.append(src('https://www.lovellgov.com/','Company identifies itself as an SBA-certified service-disabled veteran-owned small business and describes federal healthcare supply services.'))
 if i=='e24163905a439589':f['name']='Lone Star Analysis (filed former name: Lone Star Aerospace; unverified)'
 update(i,f,sources)
for d in json.loads((r/'featured73-middle10.json').read_text()):
 i=d['id']
 if d['decision']!='confirm' and i not in ['67b253be951dbc14','5c94a48d137cf5c9']:continue
 f={k:d[k] for k in ['description','website','kind','ownership']};f.update(review_outcome='confirmed',website_status='verified',notes=d['evidence'],identity_evidence=d['evidence'])
 sources=[src(d['official_url'],d['exact_official_excerpt'])]
 if i=='67b253be951dbc14':
  f.update(name='Lupin Pharmaceuticals, Inc.',website='https://www.lupin.com/US/',ownership='Subsidiary',notes='Lupin official U.S. privacy notice names the exact Inc. entity; its subsidiary list identifies it as a U.S. subsidiary. Parent listing status is not assigned to this subsidiary.',identity_evidence='Official U.S. privacy notice names Lupin Pharmaceuticals, Inc.; original aliases differ only in suffix omission and punctuation.')
  sources=[src('https://www.lupin.com/US/notice','Privacy notice names Lupin Pharmaceuticals, Inc.'),src('https://www.lupin.com/investors/financial-statements-of-subsidiaries','Subsidiary financial statements list Lupin Pharmaceuticals, Inc., USA.')]
 if i=='8da7bba6a00344b6':
  f.update(ownership='Public company',notes='Exact Ltd entity and ASX: LYC listing identified in company exchange announcement dated October 29, 2025.',identity_evidence='Official ASX announcement names Lynas Rare Earths Ltd, ACN 009 066 648.')
  sources.append(src('https://announcements.asx.com.au/asxpdf/20251029/pdf/06r5yjts631s6j.pdf','October 29, 2025 company announcement identifies Lynas Rare Earths Ltd (ASX: LYC), rare-earth separation activity, and ACN 009 066 648.'))
 if i=='7d13d882ca1186b8':f['notes']='Confirmed as the Macquarie Asset Management business. The unsuffixed filing does not identify one specific operating legal entity.'
 if i=='5c94a48d137cf5c9':
  f.update(review_outcome='partial',description='U.S. shipping and logistics company associated with Maersk. The filing includes a former-name claim that remains unverified.',notes='Maersk official history traces Maersk Inc. through Interseas Shipping and Moller Steamship, while describing Maersk Line Limited separately. The filing FKA is retained as a reported claim, not an established rename.',identity_evidence='Official history supports Maersk Inc. but does not establish the filed former-name bridge.')
  sources.append(src('https://www.maersk.com/ko-KR/News/Articles/2019/07/10/maersk-one-hundred-years-usa','2019 company history gives Maersk Inc. and Maersk Line Limited distinct historical lineages; does not establish the filed FKA.'))
 update(i,f,sources)
(r/'featured73-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured73-decisions.json').write_text(json.dumps(decisions,indent=2)+'\n')
(r/'reviewed.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
print('Saved',len(decisions),'updates; new confirmations',sum(before[i]['review_outcome']!='confirmed' and p[i]['review_outcome']=='confirmed' for i in before))
