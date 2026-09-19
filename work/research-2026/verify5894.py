import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5894-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5894,commit_sha='09b713e1bb131e4cc860f857e41d9ca9099ef4ac',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_a7981476ec088191933027095dabcf80',deployment_id='appgdep_6a9ceb4238fc81918bee1b0653046f4f',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5894,current_local_reviewed=5894,remaining=12142,publication=p,completed_batch='Round33C30 published5894 version68 and live bytes verified',next_batch='Round34A30 evidence review underway; no integration yet')
h['next_actions'].insert(0,'5894 live verified. Complete Round34A evidence and logo audit, validate, integrate and publish.')
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5894 live bytes verified')
