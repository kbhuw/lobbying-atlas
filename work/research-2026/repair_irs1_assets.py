import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'check_sec_round5.py').read_text().split('\np={}')[0])
indexes={'e576586125d9031f':4,'6b41227edd26d6b5':2,'9cb20b801924d7f8':2,'b3f905f590f6018d':1,'de386ea85ed5610b':1,'7429caf1cb4df4b6':1,'81ae1420aefc4515':3,'c8cbf355600e6551':1,'9d61c1aff686c9b0':1,'7cc9fb904d63bc4b':1}

for k,idx in indexes.items():
 p=cache/(k+'.json');c=json.load(open(p));a=c['asset_candidates'][idx]
 try:
  dest,mime,b=get(a['url']);assert mime.startswith('image/') and len(b)>80
  c.update(logo_url=a['url'],logo_kind=a['kind'],logo_http_status=200,logo_content_type=mime)
 except Exception:c.update(logo_url='',logo_kind='',logo_http_status=None)
 p.write_text(json.dumps(c,indent=2));print(k,c['logo_url'])
