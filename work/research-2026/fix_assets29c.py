import json,pathlib,concurrent.futures
r=pathlib.Path('work/research-2026')
exec((r/'check_general29c.py').read_text().split('p=json.load(open(root/')[0])
a={
'1f760e12cc6211d2':('https://cdn.prod.website-files.com/67ed54ece0b3196c1247b3d9/68b278d3fe0a8091476183e2_d0d3e662d198807e50764e0e38ee7c73_canopy%20ad%20logo.png','logo'),
'f417e5d8bf5bba5d':('https://cdn.prod.website-files.com/6970b8a0eb7e9ae5e1a148f0/69862a9d345f8712e271bb16_favicon-1.png','site_icon'),
'f614dfba6d1bd915':('https://cdn.prod.website-files.com/6970b8a0eb7e9ae5e1a148f0/69862a9d345f8712e271bb16_favicon-1.png','site_icon'),
'3700782bff2b5c43':('https://www.capitalhealth.org/themes/custom/capital/logo.svg','logo'),
'77889abe2b31fde3':('https://cdn.prod.website-files.com/66181b36aa48913ffd698dc6/69540407c399dc18099b442b_Judi-Icon_Gradient%20(3).png','site_icon'),
'1006ae5d73744f90':('https://cdn.prod.website-files.com/69decdc967182082b5ab4215/69deece8b2651a1f8b18df2b_Webclip.png','site_icon')}
def fix(item):
 k,(u,kind)=item;dest,typ,b=get(u);assert typ.startswith('image/') and len(b)>80,(k,typ,len(b));p=r/f'website-cache/{k}.json';c=json.load(open(p));c.update(logo_url=u,logo_kind=kind,logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=typ);p.write_text(json.dumps(c,indent=2));return k
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:print(list(ex.map(fix,a.items())))
s=(r/'build_general29b.py').read_text().replace('29b','29c');start=s.index('hold=');end=s.index('\n',start);s=s[:start]+"hold={'6f00612bc29b9b3e','1c649db611f6fbd6','4a59b791b4a00d9f'}"+s[end:];(r/'build_general29c.py').write_text(s)
