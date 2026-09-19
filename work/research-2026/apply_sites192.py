import json,pathlib,copy,zipfile
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured192-before.json').exists();before={};dec=[]
rows=[]
for i in ['da69aa23f81788bb','2169ba6606f294db']:
 rows.append((i,'https://www.centerforlearnerequity.org/who-we-are/our-story/','Official history explicitly connects Center for Learner Equity with its former National Center for Special Education in Charter Schools name and documents its education advocacy. Identity is confirmed; exact tax classification remains unknown. Original filing IDs remain separate.'))
for i in ['9eeab96f1385f7b7','8420f4ca1fe89392']:
 rows.append((i,'https://cencoregroup.com/about-cencore/','Official company history uses both CenCore and CenCore Group for the business founded in 2010, identifies its Utah location and describes security and defense technology services. This confirms the operating identity; specific legal entities and ownership are not established, and filing IDs are not merged.'))
rows.append(('2add3941d22f2b59','https://www.cennox.com/wp-content/uploads/2025/03/Health-Coverage_USA.pdf','Official employee tax-document notice explicitly identifies Cennox, Inc., its Alpharetta address and cennox.com website. This establishes the U.S. company identity; the parent ownership chain remains unknown.'))
rows.append(('db5e15d515e7daf2','https://www.cprf.org/','Official website identifies Cerebral Palsy Research Foundation of Kansas, Inc. in Wichita and documents disability employment and housing programs. House registration 301270757.xml independently places the client in Wichita, KS 67208 with disability employment activity. The filing street number is 511 versus official 5111, so this is a name, locality and activity match, not an exact street-address match.'))
for i,u,n in rows:
 v=p[i];before[i]=copy.deepcopy(v);v.update(review_outcome='confirmed',status='sourced',website_status='verified',checked_at='2026-09-13',identity_evidence=n,notes=n);v['sources'].append(dict(url=u,label='Official identity evidence',claim=n));dec.append(dict(id=i,decision='confirmed',notes=n))
p['db5e15d515e7daf2']['description']='Wichita nonprofit offering accessible housing, job placement, wheelchair customization and assistance with medical equipment for people with disabilities.'
z=zipfile.ZipFile('work/federal-directory/raw/2021_Registrations_XML.zip');name=next(n for n in z.namelist() if n.endswith('301270757.xml'));(r/'featured192-cprf-registration.xml').write_bytes(z.read(name))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured192-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('6 identities saved')
