import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[]
def put(i,patch,ev,urls):
 before[i]=json.loads(json.dumps(p[i]));a=p[i];a.update(patch);a.update(review_outcome='confirmed',identity_evidence=ev,notes=ev,checked_at='2026-09-13',as_of='2026-09-13',website_status='verified',status='sourced')
 for u in dict.fromkeys(urls):
  if u not in [s['url'] for s in a['sources']]:a['sources'].append(dict(url=u,label='Primary organization evidence',claim=ev))
 dec.append(dict(id=i,patch=patch,evidence=ev,urls=urls))
for x in json.load(open(r/'featured58-root-plan.json')):put(x['id'],{k:v for k,v in x.items() if k in ['name','description','ownership']},x['evidence'],[x['url']])
for x in json.load(open(r/'featured58-first10.json')):
 if x['decision']!='confirm':continue
 i=x['originalID'];patch=x['proposed'].copy();patch.pop('aliases',None);patch.pop('on_behalf_of',None);ev=x['evidence'];urls=[s['url'] for s in x['exact_quotes']]
 if i=='5af72fc367857fa1':urls.append('https://www.engie-na.com/privacy/');ev='Official ENGIE North America privacy policy, last updated October 2024, explicitly identifies ENGIE North America Inc., matching the original Inc. aliases. Energy-services activity corroborated; ownership remains Unknown.'
 if i=='528b7a4d75e35d36':urls.append('https://www.enpro.com/for-investors/investor-news/news-details/2023/EnPro-Industries-Inc.-Announces-Upcoming-Name-Change-to-Enpro-Inc/default.aspx');ev='Official 2023 announcement explicitly documents EnPro Industries, Inc. changing its name to Enpro Inc. Preserve historical filed name and link to current company; current ownership not newly inferred.'
 if i=='1719c674c8b4b1e9':urls.append('https://www.enterprisemobility.com/en/news-stories/news-stories-archive/2026/08/scoring-big-for-communities.html');patch['ownership']='Private company (Taylor family)';ev+=' Official August 2026 company release states it is privately held by the Taylor family.'
 if i=='dcf84b78ec2593f1':patch['name']='Enterprise Mobility (represented by HB Strategies)';patch['kind']='Car rental and fleet management';ev+=' Display website belongs to represented Enterprise Mobility, not to HB Strategies.'
 if i=='0f69f34aa437686c':patch['ownership']='Unknown';ev+=' Public status is not established by the cited homepage; ownership remains Unknown.'
 put(i,patch,ev,urls)
for x in json.load(open(r/'featured58-middle10.json')):
 if x['decision']=='hold':continue
 patch=x['final_patch'].copy();ev=x['evidence']
 if x['id'] in ['a1f8c61f5deb5cb6','26d979bfcd8ea0ba']:patch['ownership']='Unknown';ev+=' Ownership/listing category is not independently proven by the quoted evidence and remains Unknown.'
 put(x['id'],patch,ev,[v for k,v in x.items() if k.endswith('_url')])
(r/'featured58-root-before.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n');(r/'featured58-root-decisions.json').write_text(json.dumps(dec,indent=2,ensure_ascii=False)+'\n')
for f,c in [(r/'reviewed.json',False),(Path('lobbying-map/research/reviewed-2026.json'),True),(Path('outputs/2026-research-trial/profiles.json'),False)]:f.write_text(json.dumps(p,ensure_ascii=False,indent=None if c else 2)+('' if c else '\n'))
print('Saved',len(dec),'confirmed identities')
