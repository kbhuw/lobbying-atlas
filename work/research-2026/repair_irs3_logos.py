from pathlib import Path
exec(Path('work/research-2026/check_websites.py').read_text().split("profiles=json.load(open('lobbying-map/research/profiles.json'))")[0])
for k,u in [('bb19c440a77e87f5','https://www.kyha.com/wp-content/uploads/2023/06/logo-white.svg'),('79b69c5959ed0712','https://independentsector.org/wp-content/uploads/2025/10/IS-logo-green.svg')]:
 p=cache/(k+'.json');c=json.load(open(p));assert any(a['url']==u for a in c['asset_candidates']);f,m,d=get(u);assert 'image' in m and len(d)>80;c.update(logo_url=f,logo_kind='logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=m);p.write_text(json.dumps(c,indent=2)+'\n')
 a=root/'irs-round3-b-branding-audit.json';audit=json.load(open(a));audit[k].update(replacement_candidate_url=f,status='keep');a.write_text(json.dumps(audit,indent=2)+'\n')
 print(k,'replaced marketing/shared image with own observed logo')
