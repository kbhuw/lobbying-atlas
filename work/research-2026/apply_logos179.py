import json,pathlib,copy,hashlib,xml.etree.ElementTree as E
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured179-before.json').exists();before={};dec=[]
b=(r/'featured179-chime.svg').read_bytes();svg=E.fromstring(b)
assert set(t.tag.split('}')[-1] for t in svg.iter())<={'svg','g','path','rect','style'}
for t in svg.iter():
 for k,v in t.attrib.items():assert not k.lower().startswith('on') and 'href' not in k.lower() and 'url(' not in v.lower()
assert b'url(' not in b.lower() and b'@import' not in b.lower()
h=hashlib.sha256(b).hexdigest();url=f'/assets/organization-logos/{h}.svg';pathlib.Path('lobbying-map/public'+url).write_bytes(b)
for i,u in [('cdff23807d2964b1','https://carlsmed.com/wp-content/uploads/2024/10/Frame-3-1.png'),('1abd7999f38e0640',url)]:
 v=p[i];before[i]=copy.deepcopy(v);note='Official logo extracted from the organization website, original bytes preserved and visually verified.'
 if i=='1abd7999f38e0640':note+=' Chime returned a branded HTTP403 block page containing the embedded logo. This is logo evidence only, not evidence that substantive page content was accessed.'
 v.update(logo_url=u,logo_source_url=v['website'],logo_kind='logo',logo_status='official_site_asset',logo_background='light');v['sources'].append({'url':v['website'],'label':'Official logo evidence','claim':note});dec.append(dict(id=i,logo_url=u,notes=note,source_cache=f'featured179-{i}.html'))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured179-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('2 logos saved')
