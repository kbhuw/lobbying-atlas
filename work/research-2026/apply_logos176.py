import json,pathlib,copy
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured176-before.json').exists();before={};dec=[]
for e in json.load(open(r/'featured176-logo-assets.json')):
 assert e['http_status']==200
 i='bd3d6bea83d8ab47' if e['name']=='microsoft' else 'd5e04ab791aa0e01';v=p[i];before[i]=copy.deepcopy(v)
 note='Logo extracted from the official website header, fetched successfully and visually inspected. Original asset retained.'
 v.update(logo_url=e['url'],logo_source_url=v['website'],logo_kind='logo',logo_status='official_site_asset',logo_background='light' if e['name']=='microsoft' else 'dark')
 v['sources'].append({'url':e['url'],'label':'Official logo asset','claim':note});dec.append(dict(id=i,name=v['name'],asset=e,source_page=v['website'],source_cache=str((r/f'featured176-{i}.html').resolve()),notes=note))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured176-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(len(dec),'logos saved')
