import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));reviews=json.load(open(r/'government127-last65-review.json'));before={};dec=[]
notes={5: 'FDA’s April 8, 2025 warning letter identifies exact Tailstorm Health Inc. dba Medivant Health at its Phoenix outsourcing facility and describes drug production. This confirms the legal-name/DBA relationship; the letter is a regulatory warning, not an endorsement, and does not establish current ownership.', 7: 'Florida’s provider record identifies TELEEMC LLC as owner of FIRST VISIT MD, lists the clinic as for-profit and Jeffrey Applebaum with 100 percent ownership, and supplies TeleEMC.com. The record’s license status is IN REVIEW; it is not presented as an active-license approval.', 10: 'The official Fort Worth website identifies the Texas city government and City Hall at 100 Fort Worth Trail, Fort Worth. Original filing names remain visible.', 11: 'The official Oklahoma City website identifies the city government, departments and City Hall at 200 North Walker, Oklahoma City, Oklahoma.', 19: 'DOE’s 2011 environmental-review documents identify Tonopah Solar Energy LLC with the Crescent Dunes project in Nye County, Nevada. A 2026 FERC notice names the exact LLC’s notice of consummation; neither excerpt establishes current plant output or the current ownership chain.', 28: 'California Department of Food and Agriculture’s 2010–2011 resource directory lists exact Tulelake Growers Association, P.O. Box 338, Tulelake. This supports the historical association identity; current tax status and website remain unverified.', 30: 'A 2026 Commerce sunset-review notice names exact U.S. OCTG Manufacturers Association and describes its members as domestic producers of oil-country tubular goods. Current tax status remains unverified.', 32: 'United for Patent Reform’s December 20, 2018 USPTO comments identify the exact coalition, describe its business membership and patent-policy purpose, and list UnitedforPatentReform.com. Historical membership claims are not treated as present counts.', 34: 'Utah’s operator-change worksheet names exact Urban Oil & Gas Group LLC as new operator of the Drunkards Wash wells effective February 28, 2023. This verifies the exact operator; it does not establish current corporate ownership.', 53: 'South Dakota’s 2025 Board of Water and Natural Resources annual report identifies Western Dakota Regional Water System as recipient of study funding and describes Missouri River water-supply feasibility work. A study and funding record are not evidence of a completed water system.'}
assert not (r/'featured128-before.json').exists()
for n,note in notes.items():
 x=reviews[n];i=x['id'];assert p[i]['name']==x['original_name'];assert p[i]['review_outcome']!='confirmed'
 before[i]=json.loads(json.dumps(p[i]));own=x['ownership']
 p[i].update(description=x['description'],ownership=own,notes=note,identity_evidence=note,review_outcome='confirmed',checked_at='2026-09-13',as_of='2026-09-13')
 if n in [10,11]:p[i]['website_status']='verified'
 if n==19:p[i]['description']='The company associated with the Crescent Dunes solar-energy project in Nye County, Nevada; current operating output is not verified.'
 if n==5:p[i]['description']='Tailstorm Health Inc., doing business as Medivant Health, produces drug products at an outsourcing facility in Phoenix, Arizona.'
 sources={s['url']:s for s in p[i]['sources']}
 good={e['url'] for e in x['fetched_evidence'] if e['http_status']==200}
 for s in x['sources']:
  if s['url'] in good:sources[s['url']]=dict(s,label='Government primary evidence',claim=note)
 p[i]['sources']=list(sources.values());dec.append(dict(id=i,name=p[i]['name'],decision='confirmed',ownership=own,notes=note,fetched_evidence=x['fetched_evidence']))
(r/'featured128-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured128-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
m=pathlib.Path('lobbying-map/research/publication-metadata.json');meta=json.load(open(m))
for i in before:
 if p[i]['status']=='unresolved':
  p[i]['status']='sourced';meta['counts']['unresolved']-=1;meta['counts']['sourced']+=1
m.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(str(len(notes))+' primary-source identities saved')
