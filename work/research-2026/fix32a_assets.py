import json,pathlib
r=pathlib.Path('work/research-2026');exec((r/'check_general32a.py').read_text().split('p=json.load(open(root/')[0])
for k,n,kind in [('2f92cf62b611ed86',2,'logo'),('5bac83a64c490023',1,'logo'),('c3c4943f5b1963b6',1,'site_icon'),('164b01596bc553f7',1,'logo')]:
 f=r/f'website-cache/{k}.json';c=json.load(f.open());u=c['asset_candidates'][n]['url'];final,mime,b=get(u);assert mime.startswith('image/') and len(b)>80;c.update(logo_url=final,logo_kind=kind,logo_http_status=200,logo_content_type=mime);f.write_text(json.dumps(c,indent=2)+'\n');print(k,'asset corrected')
