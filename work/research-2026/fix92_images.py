import json,pathlib,concurrent.futures
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round92-input.json'));exec((r/'check_round92_incremental.py').read_text().split('p=json.load(open(root/')[0])
changes={7:'https://images.squarespace-cdn.com/content/v1/5e91157c96fe495a4baf48f2/3ab115b6-600c-4856-9ddd-017ca2d4e434/NIva-website.png?format=1500w',49:'https://rarediseases.org/wp-content/uploads/2024/05/NORD_Logo-with-tag_Wide_Print_RGB-01.png',51:'https://rarediseases.org/wp-content/uploads/2024/05/NORD_Logo-with-tag_Wide_Print_RGB-01.png',60:'https://nationalpawnbrokers.org/assets/2020/09/npa-logo-new-blue@2x.png',70:'https://prod-eks-static-assets.npr.org/chrome_svg/npr-logo-2025.svg'}
def onefix(iv):
 i,u=iv;f=r/f"website-cache/{rows[i]['id']}.json";c=json.load(open(f))
 try:
  _,typ,b=get(u);assert typ.startswith('image/') and len(b)>80;c.update(logo_url=u,logo_kind='logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=typ);f.write_text(json.dumps(c,indent=2)+'\n');return i,'updated'
 except Exception as e:return i,str(e)
for z in concurrent.futures.ThreadPoolExecutor(5).map(onefix,changes.items()):print(z)
