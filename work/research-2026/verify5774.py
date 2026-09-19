import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5774-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5774,commit_sha='877f8ddf156d4a8cf6c67fdeec0d94240eae357c',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_4a96d3893fe8819197518cc26b40b2aa',deployment_id='appgdep_6a9cd2860e6881919cf25cf9ca0b959a',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5774,current_local_reviewed=5774,remaining=12262,publication=p,completed_batch='Round32B30 published5774 version64 and live bytes verified',next_batch='Round32C:21 drafts and last9 agent evidence pending; no integration yet')
h['next_actions'].insert(0,'5774 live verified. Round32C input and21 drafts saved; latest_filing helper traverses all members. Need last9 evidence, logo audit, validation and integration.')
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5774 live bytes verified')
