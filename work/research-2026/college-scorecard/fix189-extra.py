import pathlib,json
exec(pathlib.Path('work/research-2026/check_websites.py').read_text().split("profiles=json.load(open('lobbying-map/research/profiles.json'))")[0])
picks={'3b2da133959a1817':1}
audit=[]
for k,i in picks.items():
 f=cache/(k+'.json');v=json.loads(f.read_text());old=v.get('logo_url');a=v['asset_candidates'][i]
 try:
  dest,typ,img=get(a['url'],1000000);assert typ.startswith('image/') and len(img)>80
  v.update(logo_url=a['url'],logo_kind=a['kind'],logo_content_type=typ,logo_http_status=200)
  f.write_text(json.dumps(v,indent=2)+'\n');audit.append({'id':k,'rejected':old,'selected':a,'http_status':200})
 except Exception as e:
  for key in ['logo_url','logo_kind','logo_source_url','logo_http_status']:v.pop(key,None)
  f.write_text(json.dumps(v,indent=2)+'\n');audit.append({'id':k,'rejected':old,'error':str(e)})
pathlib.Path('work/research-2026/college-scorecard/round2-branding-extra-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))
