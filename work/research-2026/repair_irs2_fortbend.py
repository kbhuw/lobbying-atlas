from pathlib import Path
exec(Path('work/research-2026/check_websites.py').read_text().split("profiles=json.load(open('lobbying-map/research/profiles.json'))")[0])
u='https://fortbendregionalpartnership.com/wp-content/uploads/2023/02/FBRP_Logo_Primary.svg';f,m,d=get(u);assert 'image' in m and len(d)>80
p=cache/'dc3faa4b4000309a.json';c=json.load(open(p));c.update(logo_url=f,logo_kind='logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=m);c['asset_candidates'].insert(0,{'url':u,'kind':'logo'});p.write_text(json.dumps(c,indent=2)+'\n')
