import json,pathlib,datetime
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def src(u,c):return {'url':u,'label':'Official organization evidence','claim':c}
for d in json.load(open(r/'featured75-first10.json'))+json.load(open(r/'featured75-middle10.json')):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f={k:d[k] for k in ['description','kind','ownership','website']};f.update(review_outcome='confirmed' if d['decision'] in ['confirm','confirmed'] else 'partial',notes=d['evidence'],identity_evidence=d['evidence'],checked_at='2026-09-13',as_of='2026-09-13',status='sourced');s=[src(d['official_url'],d['exact_official_excerpt'])]
 if i=='1696fc45e607f5ea':f['ownership']='Government body'
 if i=='f533a2f5368438b1':f['ownership']='Public institution'
 if i=='e467f7f093ba0853':
  f.update(ownership='Government body',website='https://miamination.com/',logo_url='https://www.miamination.com/wp-content/uploads/2023/03/MTOK-seal-March2023-1.png',logo_kind='logo',logo_status='official_site_asset',logo_source_url='https://miamination.com/',logo_background='dark')
  s.append(src('https://miamination.com/','Official tribal website welcomes visitors as Miami Tribe of Oklahoma; header seal and wordmark fetched and visually verified. Replaces invalid-certificate www2 subdomain.'))
 if i=='03195d8d58b4dcab':f['ownership']='Unknown'
 if i=='0ff6cfe7173c32dd':f['description']='Mill develops household food-scrap processing products. The filing describes Chewie Labs as a former name; that historical relationship remains unverified.'
 if i=='5d098dccb567d6fd':f.update(review_outcome='partial',notes='Current Alliance identity and activity supported; the filed former-name relationship to National Association for Home Care & Hospice needs separate primary evidence. A current brand page alone does not establish a legal rename.')
 if i=='2fa558397b58d443':
  f.update(review_outcome='confirmed',description='Motorola, Inc. changed its name to Motorola Solutions in January 2011 after separating Motorola Mobility. Motorola Solutions provides communications and public-safety technology.',notes='Official January 18, 2011 announcement explicitly records the completed January 4 rename from Motorola, Inc. to Motorola Solutions, Inc. Motorola Mobility was separated; it is not treated as the renamed entity.',identity_evidence='Company announcement explicitly establishes legal-name continuity between Motorola, Inc. and Motorola Solutions, Inc.')
  s.append(src('https://www.motorolasolutions.com/newsroom/press-releases/motorola-solutions-to-issue-fourth-quarter-2010-earnings-results-on-jan-27.html','January 18, 2011 release states Motorola, Inc. completed the separation of Motorola Mobility Holdings and changed its name to Motorola Solutions, Inc. on January 4, 2011.'))
 if f['review_outcome']=='confirmed':f['website_status']='verified'
 p[i].update(f);seen={x['url'] for x in p[i]['sources']}
 for x in s:
  if x['url'] not in seen:p[i]['sources'].append(x);seen.add(x['url'])
 dec.append({'id':i,'decision':f['review_outcome'],'notes':f['notes']})
(r/'featured75-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured75-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
f=pathlib.Path('lobbying-map/research/verified-entity-merges.json');m=json.load(open(f));(r/'featured75-merges-before.json').write_text(json.dumps(m,indent=2)+'\n');ids=['0713b1f76f9979d7','ac47d9a7542eb23d'];assert not any(set(ids)&set(x['source_ids']) for x in m)
claim='Official NASCAR history explicitly expands NASCAR to National Association for Stock Car Auto Racing; the two unsuffixed source names are the acronym and full name of the same organization.'
m.append({'canonical_id':ids[0],'source_ids':ids,'rationale':claim,'sources':[{'url':'https://www.nascar.com/nascar-history/','claim':claim}],'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});f.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('Confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()),'new identities; one logo and one merge')
