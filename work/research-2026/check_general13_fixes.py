import json,pathlib,concurrent.futures
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round13-90-draft.json'));exec((r/'check_general13.py').read_text().split('profiles=json.load')[0])
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for k,c in ex.map(one,[(k,p[k]) for k in ['932c7b801523dff8','1f802cc519e32bc9']]):print(k,c.get('http_status'),flush=True)
for k,i in [('58a57a95e5dbc5a0',5),('0f567bde17a0a75d',1),('3fb545e0de15ced1',1),('c3178b232e4fbeb1',1)]:
 f=cache/(k+'.json');c=json.load(open(f));a=c['asset_candidates'][i]
 try:
  dest,mime,b=get(a['url']);assert mime.startswith('image/') and len(b)>80
  c.update(logo_url=a['url'],logo_kind=a['kind'],logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime)
 except Exception:c.pop('logo_url',None);c.pop('logo_http_status',None)
 f.write_text(json.dumps(c,indent=2));print('asset',k,flush=True)
