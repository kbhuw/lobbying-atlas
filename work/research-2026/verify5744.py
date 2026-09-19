import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5744-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5744,commit_sha='bbcbd98eaf3bf51883333e0f1aa0f5dea1464edd',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_6e7c5cb644088191a3d8a039e59cc2ab',deployment_id='appgdep_6a9cce5a4ec88191a31ec6f1d74567a0',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5744,current_local_reviewed=5744,remaining=12292,publication=p,completed_batch='Round32A30 published5744 version63 and live bytes verified',next_batch='Round32A input ready; agent researching bounded5, root research pending')
h['next_actions'][0:0]=['Round32A published5744 version63 via remote build fallback after archive upload transport failed twice. Checks passed and live decompressed bytes equal local build. No active agents; round31c-agent-evidence.md contains5 bounded findings unverified byroot. Six older website repairs already live in preceding version59.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5744 live bytes verified')
