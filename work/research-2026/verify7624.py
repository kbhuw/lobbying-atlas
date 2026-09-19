import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live7624-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=7624,commit_sha='1a9c0b3c56a2c4a1cb26b3ced3f3d758822030a0',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_22e6c6fca194819185b358a2fc09696c',deployment_id='appgdep_6a9d29ee43908191904bc735ec3318cf',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=7624,current_local_reviewed=7624,remaining=10412,publication=p,completed_batch='Round46 100 published7624 version84 and live bytes verified',next_batch='Next pending entries after DyStar; not started')
h['active_deployment']=None
h['next_actions']=['7624 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('7624 live bytes verified')
