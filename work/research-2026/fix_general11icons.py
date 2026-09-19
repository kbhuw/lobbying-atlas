import json,pathlib
r=pathlib.Path('work/research-2026');exec((r/'check_general11.py').read_text().split('profiles=json.load')[0])
for k,i in [('159b85ba8b579af9',1),('abb61594b355269a',1),('a6cbf1d5188bbb52',2),('5fc2586d8c3eab01',2),('d2f521a45006a9b0',2),('07fd992979a352eb',2)]:
 f=cache/(k+'.json');c=json.load(open(f));a=c['asset_candidates'][i]
 try:
  dest,mime,b=get(a['url']);assert mime.startswith('image/') and len(b)>80
  c.update(logo_url=a['url'],logo_kind=a['kind'],logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime);f.write_text(json.dumps(c,indent=2));print(k,'corrected',flush=True)
 except Exception as e:
  c.pop('logo_url',None);c.pop('logo_http_status',None);f.write_text(json.dumps(c,indent=2));print(k,'held',flush=True)
