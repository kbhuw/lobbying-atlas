import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live8324-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=8324,commit_sha='ea41a7c3505ae68af5f3b3452c86f186d4c4b91a',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_213de4b788308191a21d2e264c6d819f',deployment_id='appgdep_6a9d445628f081919a164a6afcf8def5',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=8324,current_local_reviewed=8324,remaining=9712,publication=p,completed_batch='Round53 100 published8324 version91 and live bytes verified',next_batch='Next pending entries after FINRA; not started')
h['active_deployment']=None
h['next_actions']=['8324 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('8324 live bytes verified')
