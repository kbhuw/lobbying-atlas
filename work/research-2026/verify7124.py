import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live7124-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=7124,commit_sha='81a36772be1b8ccf9e9baa9f58540b87ad0b4e7a',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_8f6f50dd8b18819197704a9cbd647caf',deployment_id='appgdep_6a9d1828baf08191926af7dfcef23119',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=7124,current_local_reviewed=7124,remaining=10912,publication=p,completed_batch='Round41 100 published7124 version79 and live bytes verified',next_batch='Next pending entries after Crowe LLP; not started')
h['active_deployment']=None
h['next_actions']=['7124 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('7124 live bytes verified')
