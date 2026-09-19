import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round3-a-researched.json'));e=json.load(open(r/'general-round3-a-research-evidence.json'));e.update(json.load(open(r/'general-round3-a-last15-evidence.json')))
# Agent evidence IDs contained transcription errors; remap only against supplied exact IDs.
for a,b in [('ce5c81386d9b6b69','ce5c81386d9d6b69'),('93053fc4455a6524','93053fe4455a6524'),('6e5aeb771e1e2ea','6e5aeb771e1e2ea6'),('9e81748974129a','9e81748974129ac8')]:
 if a in e:e[b]=e.pop(a)
assert not(set(e)-set(p))
for k,v in e.items():
 p[k]['identity_evidence']=v['identitybasis']+' '+v['uncertainties']
 if v.get('primaryexcerpt') and v['observedURLs'] and v.get('fieldsresolved'):
  p[k]['sources']+= [dict(url=v['observedURLs'][0],label='Primary page evidence',claim=v['primaryexcerpt'])]

def fix(k,name,description,website,claim,source=None,ownership=None):
 v=p[k];v.update(name=name,description=description,website=website,status='sourced',review_outcome='partial',identity_evidence=claim,website_status='partial' if website else 'unresolved')
 if source or website:v['sources'].append(dict(url=source or website,label='Primary identity and activity evidence',claim=claim))
 if ownership:v['ownership']=ownership
fix('0c2c6214cf3102f4','ActionStreamer','Develops wearable cameras, wireless video transmission, and software for live first-person video in sports, industrial work, and emergency response.','https://actionstreamer.com/','Official 2026 product announcements describe connected-camera workflows and a wearable 5G first-responder camera.','https://actionstreamer.com/blog/actionstreamer-partners-with-safeware-on-5g-first-responder-camera')
fix('aa814a85314970e7','Action Now Initiative','Advocacy organization working on electoral, criminal-justice, healthcare, higher-education, and charitable-giving reforms.','https://actionnowinitiative.org/','Official issues page describes its current reform campaigns.','https://actionnowinitiative.org/issues')
fix('4907f60faf72d0da','ACTE (Association for Career and Technical Education)','Professional association supporting career and technical education through educator development, policy advocacy, and state associations.','https://www.acteonline.org/','Official ACTE site identifies the Association for Career and Technical Education, its divisions, state associations, and governance. Exact acronym-to-client linkage remains partial.','https://www.acteonline.org/about/')
fix('ce5c81386d9d6b69','EarnIn (Activehours, Inc.)','Financial-technology company providing access to earned wages before payday and related budgeting and savings tools.','https://www.earnin.com/','Official EarnIn site identifies Activehours, Inc. and earned-wage-access products. The disclosed DBA explicitly names EarnIn.')
fix('330fc64e31ae5183','Acuity International','Provides healthcare, disaster-response, humanitarian, security, logistics, and project-support services to governments and commercial clients.','https://acuityinternational.com/','Company about page describes these service lines and its formation from Caliburn businesses.','https://acuityinternational.com/about-acuity/')
fix('a8c16aabad5ecb64','Active Optical Systems','Develops optical-control components and systems for defense, aerospace, and commercial applications.','https://www.activeopticalsystems.com/','Company page identifies Active Optical Systems and its optical components; disclosed LLS spelling is retained as an alias.','https://www.activeopticalsystems.com/about-us/')
fix('12041a39c1eadbeb','Ad Astra Rocket Company','Develops the VASIMR plasma propulsion engine for spacecraft and related advanced propulsion technology.','https://www.adastrarocket.com/','Official company site identifies Ad Astra Rocket Company and its VASIMR propulsion program.')
fix('50d09dc51630a680','Adams Memorial Foundation','Works to establish a Washington, D.C. memorial commemorating President John Adams and the Adams family.','https://www.theadamsmemorial.org/','Official foundation mission identifies its Adams-family commemoration work.','https://www.theadamsmemorial.org/our-mission')
fix('6b1b7a039a9b7e7e','Additive Manufacturing Coalition','Membership organization advocating for 3D-printing research, manufacturing policy, and federal support for additive-manufacturing technology.','https://www.addmfgcoalition.org/','Official coalition site describes member advocacy before Congress and federal agencies. Guessed long-form domain excluded.')
fix('db422ae416e860bc','ADDMAN','Provides additive manufacturing, precision machining, injection molding, and engineering services for industrial, aerospace, medical, and defense customers.','https://addmangroup.com/','Official ADDMAN site describes its manufacturing processes and customer industries.')
# Never describe an individual or ambiguous county as an identified contractor or jurisdiction.
for k,desc in [('3d4cbf373e4ce302','Individual named in the lobbying records. No separate company identity or current business has been independently established.'),('70f1f9364e9bf618','County government disclosed as Adams County. The state and exact jurisdiction remain unconfirmed.')]:
 p[k].update(description=desc,website='',ownership='Unknown',kind='Individual' if k.startswith('3d4') else 'Government',status='unresolved',review_outcome='unresolved')
for k in ['d3af6bbdbcf752a1','3f30608ef8ddfbab','a3c63db490a21edc','9e81748974129ac8','ffb750c413483b4c']:
 p[k]['review_outcome']='unresolved';p[k]['status']='unresolved';p[k]['website']='';p[k]['ownership']='Unknown'
for k,v in p.items():
 v.update(as_of='2026-09-05',checked_at='2026-09-05');v.setdefault('logo_url','');v.setdefault('logo_kind','');v.setdefault('logo_source_url','');v.setdefault('logo_status','unresolved')
(r/'general-round3-a-root-draft.json').write_text(json.dumps(p,indent=2)+'\n');print('30 exact IDs; root source corrections saved')
