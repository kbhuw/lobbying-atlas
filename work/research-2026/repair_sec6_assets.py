import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'check_sec_round5.py').read_text().split('\np={}')[0])
indexes={'b600cfa4bc6c7292':1,'193139e22bf59f68':1,'71473afde707a002':1,'d4c9ad786b808b24':1,'f48a70159c2357b3':1}

for k,idx in indexes.items():
 p=cache/(k+'.json');c=json.load(open(p));a=c['asset_candidates'][idx]
 try:
  dest,mime,b=get(a['url']);assert mime.startswith('image/') and len(b)>80
  c.update(logo_url=a['url'],logo_kind=a['kind'],logo_http_status=200,logo_content_type=mime)
 except Exception:c.update(logo_url='',logo_kind='',logo_http_status=None)
 p.write_text(json.dumps(c,indent=2));print(k,c['logo_url'])
