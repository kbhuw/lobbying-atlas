import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5804-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5804,commit_sha='5d46e14bd8612bfafc131b2255486d838c2c8375',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_ab72866526c08191a73a07ec33d043c2',deployment_id='appgdep_6a9cd4f0e5bc8191b24e6f79e0e43c89',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5804,current_local_reviewed=5804,remaining=12232,publication=p,completed_batch='Round32C30 published5804 version65 and live bytes verified',next_batch='Round33A30 drafts and checks underway; no integration yet')
h['next_actions'].insert(0,'5804 live verified. Round32C input and21 drafts saved; latest_filing helper traverses all members. Need last9 evidence, logo audit, validation and integration.')
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5804 live bytes verified')
