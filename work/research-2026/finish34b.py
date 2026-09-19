import json,pathlib
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round34-b-input.json'));exec((r/'check_general34a.py').read_text().split('p=json.load(open(root/')[0])
for i,selector in [(18,'christianacare-logo.svg'),(78,'/assets/logos/citgo-logo.svg')]:
 f=r/f"website-cache/{rows[i]['id']}.json";c=json.load(open(f));u=next(a['url'] for a in c['asset_candidates'] if selector in a['url']);dest,mime,data=get(u);assert mime.startswith('image/') and len(data)>80;c.update(logo_url=u,logo_kind='logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime);f.write_text(json.dumps(c,indent=2)+'\n');print(i,mime)
