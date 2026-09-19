import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5924-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5924,commit_sha='916316bab9ea0a2071a6cf5cd8febaf5d8f9cf42',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_f13c469d7c9c81919688e64cf5e2e69f',deployment_id='appgdep_6a9cec4e25788191a9e5d85bacaeb484',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5924,current_local_reviewed=5924,remaining=12112,publication=p,completed_batch='Round34A30 published5924 version69 and live bytes verified',next_batch='Round34B100 evidence review underway; no integration yet')
h['next_actions'].insert(0,'5924 live verified. Complete Round34B evidence and logo audit, validate, integrate and publish.')
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5924 live bytes verified')
