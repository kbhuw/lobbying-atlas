import json,pathlib
r=pathlib.Path('work/research-2026')
exec((r/'check_general31c.py').read_text().split('p=json.load(open(root/')[0])
k='ed7e42683ded4195';f=r/f'website-cache/{k}.json';c=json.load(f.open());u=c['asset_candidates'][-1]['url'];final,mime,data=get(u);assert mime.startswith('image/') and len(data)>80;c.update(logo_url=final,logo_kind='site_icon',logo_http_status=200,logo_content_type=mime);f.write_text(json.dumps(c,indent=2)+'\n')
f=r/'general-round31c-root-draft.json';p=json.load(f.open());v=p['22bc4ac1e0e16b45'];v['notes']='Specific current owners not verified. Official company website confirms metals and raw-material trading.';v['sources'].append(dict(url='https://www.ccmallc.com/',label='Official organization website',claim='Current company website identifies raw-material and metals trading.'));f.write_text(json.dumps(p,indent=2)+'\n')
print('CVMS social image replaced with official icon; CCMA verified-site note corrected')
