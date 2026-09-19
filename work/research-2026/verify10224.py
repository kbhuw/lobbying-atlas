import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live10224-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=10224,commit_sha='ea711edd522e7a4b2cdc6ba550caca32c9b78645',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_fd479498ee4c81919e13c153f99c2745',deployment_id='appgdep_6a9dff7479e8819195361056fb6a555c',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=10224,current_local_reviewed=10224,remaining=7812,publication=p,completed_batch='Round72 100 published10224 version110 and live bytes verified',next_batch='Round73 selected; research not started')
h['active_deployment']=None
h['next_actions']=['10224 live verified. Start Round73 research; Spark quote extraction pilot results and validator saved.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('10224 live bytes verified')
