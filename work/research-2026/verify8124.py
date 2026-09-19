import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live8124-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=8124,commit_sha='a5fd5f5f07db8c1121ba89a115e195898df30af3',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_e75a4c2527e881918d434ccee2c8543c',deployment_id='appgdep_6a9d3c51566081919dfecf41f307959f',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=8124,current_local_reviewed=8124,remaining=9912,publication=p,completed_batch='Round51 100 published8124 version89 and live bytes verified',next_batch='Next pending entries after Exelon Business Services Company; not started')
h['active_deployment']=None
h['next_actions']=['8124 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('8124 live bytes verified')
