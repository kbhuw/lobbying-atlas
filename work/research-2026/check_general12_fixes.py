import json,pathlib,concurrent.futures
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round12-90-draft.json'));exec((r/'check_general12.py').read_text().split('profiles=json.load')[0])
keys=['79da0fc003581999','95b569a84e4e369c','523322fdda892d71','f96d6015ad0b7f0a','47dc83eef2babc76']
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for k,c in ex.map(one,[(k,p[k]) for k in keys]):print(k,c.get('http_status'),c.get('error',''),flush=True)
for k,i in [('7455229aee613a2a',1),('220e0f714572af9b',1),('d7290ad234c8ae76',2)]:
 f=cache/(k+'.json');c=json.load(open(f));a=c['asset_candidates'][i]
 try:
  dest,mime,b=get(a['url']);assert mime.startswith('image/') and len(b)>80
  c.update(logo_url=a['url'],logo_kind=a['kind'],logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime)
 except Exception:c.pop('logo_url',None);c.pop('logo_http_status',None)
 f.write_text(json.dumps(c,indent=2));print('asset',k,flush=True)
