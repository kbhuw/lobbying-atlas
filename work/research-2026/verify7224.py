import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live7224-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=7224,commit_sha='36a3ca300386b746be97864e019aec74ca7d0667',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_fe09eb5a1bb081919768d63904af4215',deployment_id='appgdep_6a9d1c03b6b88191bf2585dc0d788753',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=7224,current_local_reviewed=7224,remaining=10812,publication=p,completed_batch='Round42 100 published7224 version80 and live bytes verified',next_batch='Next pending entries after Dakota Creek Industries; not started')
h['active_deployment']=None
h['next_actions']=['7224 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('7224 live bytes verified')
