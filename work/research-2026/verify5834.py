import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5834-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5834,commit_sha='041b62ef6e58eacbdbad9b6189061f87dcca00ab',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_5c32da0916d08191b8513df90fa96b35',deployment_id='appgdep_6a9ce58a7038819184c432206ab6a13c',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5834,current_local_reviewed=5834,remaining=12202,publication=p,completed_batch='Round33A30 published5834 version66 and live bytes verified',next_batch='Round33B30 evidence review underway; no integration yet')
h['next_actions'].insert(0,'5834 live verified. Complete Round33B evidence and logo audit, validate, integrate and publish.')
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5834 live bytes verified')
