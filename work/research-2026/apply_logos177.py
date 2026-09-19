import json,pathlib,copy
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured177-before.json').exists();before={};dec=[]
for e in [{'url':'https://www.canpack.com/wp-content/themes/canpack-theme/dist/img/logo.svg','http_status':200,'name':'canpack'}]:
 assert e['http_status']==200
 i='61c5e79dec150ee9';v=p[i];before[i]=copy.deepcopy(v)
 note='Logo extracted from the official website header, fetched successfully and visually inspected. Original asset retained. This is the CANPACK group wordmark; it does not establish separate branding for each affiliate.'
 v.update(logo_url=e['url'],logo_source_url=v['website'],logo_kind='logo',logo_status='official_site_asset',logo_background='light')
 v['sources'].append({'url':e['url'],'label':'Official logo asset','claim':note});dec.append(dict(id=i,name=v['name'],asset=e,source_page=v['website'],source_cache=str((r/f'featured177-{i}.html').resolve()),notes=note))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured177-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(len(dec),'logos saved')
