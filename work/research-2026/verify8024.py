import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live8024-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=8024,commit_sha='e7498e59ef5fa8272747d5a0bf884ee019b90919',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_a803f798ffa0819184b6b91f2eb694de',deployment_id='appgdep_6a9d38028e7c8191b4b18df7d442b778',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=8024,current_local_reviewed=8024,remaining=10012,publication=p,completed_batch='Round50 100 published8024 version88 and live bytes verified',next_batch='Next pending entries after Equus Development, L.P.; not started')
h['active_deployment']=None
h['next_actions']=['8024 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('8024 live bytes verified')
