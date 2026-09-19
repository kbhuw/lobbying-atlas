import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5864-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5864,commit_sha='c0aedc1cf0756d4455da94898d68fb52e3b06d14',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_ecc31ffb63648191b47787907aba95b4',deployment_id='appgdep_6a9ce7da7d548191b0ca4062346d740b',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5864,current_local_reviewed=5864,remaining=12172,publication=p,completed_batch='Round33B30 published5864 version67 and live bytes verified',next_batch='Round33C30 evidence review underway; no integration yet')
h['next_actions'].insert(0,'5864 live verified. Complete Round33C evidence and logo audit, validate, integrate and publish.')
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5864 live bytes verified')
