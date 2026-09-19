import pathlib,json
exec(pathlib.Path('work/research-2026/check_general15.py').read_text().split('profiles=json.load')[0])
for k,n in [('871ffc6a73e4f04d',1),('ba1bceca92088b4b',4),('1b43ea38b6251998',2)]:
 f=pathlib.Path(f'work/research-2026/website-cache/{k}.json');c=json.load(open(f));a=c['asset_candidates'][n]
 try:
  u,m,b=get(a['url']);assert 'image' in m;c.update(logo_url=u,logo_kind=a['kind'],logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=m);f.write_text(json.dumps(c,indent=2)+'\n');print(k,m,len(b))
 except Exception as e:print(k,str(e))
