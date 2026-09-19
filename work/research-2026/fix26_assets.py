import pathlib,json
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
for k,i in {'895791c3cdada06d':1,'2e997dbd7c963af2':1,'53b932bcd6e5ea04':1,'205baf74f47265e4':1,'d31094a53f90b6e5':1}.items():
 path=cache/(k+'.json');c=json.load(open(path));a=c['asset_candidates'][i]
 try:
  dest,mime,b=get(a['url']);assert mime.startswith('image/') and len(b)>80;c.update(logo_url=a['url'],logo_kind=a['kind'],logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime);print(k,'corrected',flush=True)
 except Exception as e:c.pop('logo_url',None);print(k,str(e),flush=True)
 path.write_text(json.dumps(c,indent=2))
# Same verified government domain and content, reused for the second disclosed alias.
a=json.load(open(cache/'7fbb120b19e7a6b0.json'));a['id']='b62f7bd87e97c9df';(cache/'b62f7bd87e97c9df.json').write_text(json.dumps(a,indent=2))
