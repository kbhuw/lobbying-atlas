import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'check_gov132.py').read_text().split('\np=json.load')[0])
for k,idx in {'06a1f43b3b862151':1,'34b5fa8b312df6de':2,'b9110a4740c12434':1}.items():
 p=cache/(k+'.json');c=json.load(open(p));a=c['asset_candidates'][idx]
 try:
  dest,mime,b=get(a['url']);assert mime.startswith('image/') and len(b)>80;c.update(logo_url=a['url'],logo_kind=a['kind'],logo_http_status=200,logo_content_type=mime)
 except Exception:c.update(logo_url='',logo_kind='',logo_http_status=None)
 p.write_text(json.dumps(c,indent=2));print(k,c['logo_url'])
