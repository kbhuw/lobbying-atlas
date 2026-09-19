import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live8824-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=8824,commit_sha='3d926fa38834665ec52339bf482f451f43e7a1c5',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_8c4948a163e4819189f21395618536b2',deployment_id='appgdep_6a9d57cf46488191ae696f8a500ac7ff',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=8824,current_local_reviewed=8824,remaining=9212,publication=p,completed_batch='Round58 100 published8824 version96 and live bytes verified',next_batch='Next pending entries after Global Medical Response; Round59 evidence saved and awaiting root review')
h['active_deployment']=None
h['next_actions']=['8824 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('8824 live bytes verified')
