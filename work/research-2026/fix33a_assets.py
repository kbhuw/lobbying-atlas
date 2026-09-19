import pathlib,json
r=pathlib.Path('work/research-2026');s=(r/'check_general33a.py').read_text();exec(s[:s.index('p=json.load(open(root/')])
fix={
'd52a26727e03a8f1':('https://www.chainalysis.com/wp-content/themes/chainalysis/static/icon-192x192.png','site_icon'),
'fe9d0552f94ff3f2':('https://www.uschamber.com/dist/icons/apple-touch-icon.png','site_icon'),
'dcb8ee384fca8b48':('https://cdn.prod.website-files.com/5fe306caa0a61675092c68dc/65c2760658fc9d743c65185f_CesiumAstro_Favicon_256px.png','site_icon'),
'ebcc3d87cb1ad000':('https://csashipping.org/wp-content/uploads/2022/09/Official-CSA-LOGO-PNG.png','logo'),
'0184b8b9c1f0aaff':('https://static.wixstatic.com/media/4b98ed_21f889a24ba84d47ac27b707b7d4bc44~mv2.png','logo')}
for k,(u,kind) in fix.items():
 try:
  dest,mime,b=get(u);assert mime.startswith('image/') and len(b)>80
  f=r/f'website-cache/{k}.json';c=json.load(open(f));c.update(logo_url=u,logo_kind=kind,logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime);f.write_text(json.dumps(c,indent=2)+'\n');print(k,'corrected')
 except Exception as e:print(k,str(e))
s=(r/'build_general32c.py').read_text().replace('32c','33a');start=s.index('hold=');end=s.index('\n',start);s=s[:start]+"hold={'411dadce4230d620','514b36f2f26ccbdc','77fa863fe9a581de','4d1458cd78200a28','bf53efddefc53f4f','34cb8b1807fed9df'}"+s[end:];(r/'build_general33a.py').write_text(s)
