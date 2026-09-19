import json,pathlib,concurrent.futures
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round93-input.json'));exec((r/'check_round93_incremental.py').read_text().split('p=json.load(open(root/')[0])
changes={6:'https://nssta.com/themes/nssta/images/logo-dark.svg',32:'https://www.nwtf.org/android-chrome-192x192.png',42:'https://nafoa.org/wp-content/uploads/2022/04/NAFOA_new_Logo_small.png',52:'https://www.npanational.org/wp-content/uploads/2025/06/npa-logo.svg',63:'https://navenergy.com/wp-content/uploads/2024/10/23-NEH-08761-NTEC-Logo-Suite-2017_Colors_Vertical-4C.png',64:'https://navenergy.com/wp-content/uploads/2024/10/23-NEH-08761-NTEC-Logo-Suite-2017_Colors_Vertical-4C.png',72:'https://prod-eks-static-assets.npr.org/chrome_svg/npr-logo-2025.svg',76:'https://www.navyfederal.org/etc.clientlibs/nfculibs/clientlibs/uife/clientlib-uife-nfculibs-site/resources/images/favicon.ico'}
def onefix(iv):
 i,u=iv;f=r/f"website-cache/{rows[i]['id']}.json";c=json.load(open(f))
 try:
  _,typ,b=get(u);assert typ.startswith('image/') and len(b)>80;c.update(logo_url=u,logo_kind='logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=typ);f.write_text(json.dumps(c,indent=2)+'\n');return i,'updated'
 except Exception as e:return i,str(e)
for z in concurrent.futures.ThreadPoolExecutor(5).map(onefix,changes.items()):print(z)
