import json,pathlib
r=pathlib.Path('work/research-2026');exec((r/'check_general30b.py').read_text().split('p=json.load(open(root/')[0])
for k,u in {'b3dad2a7cf06d4fa':'https://www.elastic.co/apple-touch-icon.png','ebcf6de3b3bcff4a':'https://vaulteddeep.com/wp-content/uploads/2026/08/cropped-favicon-180x180.png'}.items():
 dest,typ,b=get(u);assert typ.startswith('image/') and len(b)>80;c=json.load(open(r/f'website-cache/{k}.json'));c.update(logo_url=u,logo_kind='site_icon',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=typ);(r/f'website-cache/{k}.json').write_text(json.dumps(c,indent=2))
s=(r/'build_general30a.py').read_text().replace('30a','30b');a=s.index('hold=');b=s.index('\n',a);s=s[:a]+"hold={'b2bb71c3e281865d','68d880b44027b0dd','087b73c2be4de158','f19c35f1531a135e'}"+s[b:];(r/'build_general30b.py').write_text(s)
