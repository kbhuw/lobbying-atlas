import json,pathlib,copy,datetime
r=pathlib.Path('work/research-2026');site=pathlib.Path('lobbying-map');holds=json.load(open(site/'research/registry-match-holds.json'));reg=json.load(open('work/organization-research/registry-profiles.json'));ps=json.load(open(r/'reviewed.json'))
resolutions={
'a46e371f92938ea6':('Brady Campaign to Prevent Gun Violence','Advocates for reducing gun violence through changes to laws, industry practices, and public behavior.','The mission uses foundation as a policy metaphor, not as an entity name.'),
'22e1395df6176832':('Holzer Health System','Parent organization managing affiliated nonprofit healthcare providers.','The filed mission explicitly identifies Holzer Health System as the managing parent of named hospital and foundation subsidiaries.'),
'fccdc2ba1ae99342':('Exalt Youth','Provides education, paid internships, and career support for young people involved in the criminal justice system.','The foundation reference describes its historical incubator; the return identifies Exalt Youth itself.'),
'74e94842f1343935':('Investment Company Institute','Represents investment funds and advocates for the asset-management industry and long-term investors.','Foundation is used as a metaphor for the industry, not a related entity.'),
'e0a2f96345dbca25':('US Ignite, Inc.','Builds public-private partnerships supporting broadband applications and smart-city technology projects.','Foundations are listed as partners; the return identifies US Ignite itself.'),
'69071647caaead3d':('Reading Is Fundamental, Inc.','Promotes children’s literacy by encouraging reading and helping children develop reading skills.','Foundation is used metaphorically in its reading mission, not as a legal entity.'),
'50581786ee76c6b4':('Beaufort Regional Chamber of Commerce','Represents Beaufort-area businesses and promotes regional economic development.','Foundation refers metaphorically to successful businesses supporting the community.'),
'29b0dfd1a40dccd9':('Greater Minnesota Housing Fund','Finances affordable housing through loans, grants, and investments and supports community housing organizations.','The named foundations are its founders; the return identifies Greater Minnesota Housing Fund itself.')}
out={}
for k,(name,desc,reason) in resolutions.items():
 assert k not in ps
 d=json.load(open(r/'tax-return-evidence'/f'{k}.json'));base=reg[k];v={'name':name,'description':desc,'kind':base.get('kind','Nonprofit / initiative'),'ownership':'Not applicable','website':json.load(open(site/'research/registry-websites.json'))[k]['website'],'website_status':'filed','review_outcome':'partial','status':'sourced','as_of':'2026-09-05','checked_at':'2026-09-05','featured':False,'legal_form':'','logo_url':'','logo_kind':'','logo_source_url':'','logo_status':'unresolved','sources':copy.deepcopy(base['sources']),'notes':reason+' Description is based on the organization’s filed mission.','identity_evidence':'EIN '+d['ein']+'; legal name '+d['organization_name']+'. '+reason}
 v['sources'].append({'label':'Form 990 identity and mission','url':d['source_url'],'claim':'Return identifies '+d['organization_name']+' and reports its mission. '+reason})
 f=r/'website-cache'/f'{k}.json'
 if k in ['a46e371f92938ea6','29b0dfd1a40dccd9'] and f.exists():
  a=json.load(open(f));v.update(website_status='verified',review_outcome='confirmed');v['sources'].append({'label':'Official organization site','url':a['final_url'],'claim':'Page identifies this organization and its activities.'})
  if a.get('logo_http_status')==200:
   for field in ['logo_url','logo_kind','logo_source_url']:v[field]=a[field]
   v['logo_status']='official_site_asset'
 out[k]=v;holds.pop(k,None)
(r/'resolved-foundation-profiles.json').write_text(json.dumps(out,indent=2)+'\n');(r/'foundation-review-decisions.json').write_text(json.dumps({k:{'decision':'clear_hold','reason':v[2]} for k,v in resolutions.items()},indent=2)+'\n');(site/'research/registry-match-holds.json').write_text(json.dumps(holds,indent=2)+'\n');print('Resolved eight false-positive holds; three genuine entity questions remain.')
