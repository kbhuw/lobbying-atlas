import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9424-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9424,commit_sha='b1c10604b0960df2653d19c0d31fd076fdc47c03',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_0cacf5fdb74c8191aa87ef21ff7a6258',deployment_id='appgdep_6a9d6b2dbb14819188ead059535161f2',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9424,current_local_reviewed=9424,remaining=8612,publication=p,completed_batch='Round64 100 published9424 version102 and live bytes verified',next_batch='Round65 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9424 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9424 live bytes verified')
