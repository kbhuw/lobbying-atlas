from pathlib import Path
exec(Path('work/research-2026/check_websites.py').read_text().split("profiles=json.load(open('lobbying-map/research/profiles.json'))")[0])
audit=json.load(open(root/'irs-round3-c-branding-audit.json'));am={x['id']:x for x in audit['records']}
for k,index in [('712e80216499b07e',1),('ba8aeee6eac76de7',5),('e774787beee879e8',1),('eeb047ecbe16ecaa',1),('9e20b34856c500da',1)]:
 p=cache/(k+'.json');c=json.load(open(p));candidate=c['asset_candidates'][index];u=candidate['url'];f,m,d=get(u);assert 'image' in m and len(d)>80
 if k=='ba8aeee6eac76de7':print('Blindmerchants SVG labels',re.findall(r'<(?:title|desc)[^>]*>(.*?)</',d.decode(errors='replace'))[:10])
 c.update(logo_url=f,logo_kind=candidate['kind'],logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=m);p.write_text(json.dumps(c,indent=2)+'\n');am[k].update(decision='keep',logo_url=f,logo_kind=candidate['kind'],replacement_candidate=f,reason='Root selected the organization-specific site asset; removed partner or program image.');print(k,'verified',candidate['kind'])
(root/'irs-round3-c-branding-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
