import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live7524-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=7524,commit_sha='f53973ede3697da0cd4b18dc49ed34636a9be844',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_3aecc335c7f48191bd33c96733d4e7c4',deployment_id='appgdep_6a9d260b56a4819197f7d39786a22df8',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=7524,current_local_reviewed=7524,remaining=10512,publication=p,completed_batch='Round45 100 published7524 version83 and live bytes verified',next_batch='Next pending entries after Doucet Consulting Solutions on behalf of GNC Holdings; not started')
h['active_deployment']=None
h['next_actions']=['7524 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('7524 live bytes verified')
