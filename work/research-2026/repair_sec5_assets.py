import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'check_sec_round5.py').read_text().split('\np={}')[0])
indexes={'37b3912a9a6a87bd':1,'63a4e14315246f27':1,'1cf529cb4c65c5d3':1,'8ca31f24ef318955':1,'51b9fc24f523b193':1,'a1f7219a66c3394f':2}
for k,idx in indexes.items():
 p=cache/(k+'.json');c=json.load(open(p));a=c['asset_candidates'][idx]
 try:
  dest,mime,b=get(a['url']);assert mime.startswith('image/') and len(b)>80
  c.update(logo_url=a['url'],logo_kind=a['kind'],logo_http_status=200,logo_content_type=mime)
 except Exception:c.update(logo_url='',logo_kind='',logo_http_status=None)
 p.write_text(json.dumps(c,indent=2));print(k,c['logo_url'])
for k,n,u in [('7166526f18a9a999','PTC Therapeutics','https://www.ptcbio.com/about-ptc/'),('554f4b4e05423d7b','VivoSim Labs','https://vivosim.ai/')]:
 _,c=one((k,dict(name=n,website=u)));print(k,c.get('http_status'),c.get('error'))
