import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5654-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5654,commit_sha='3c915b5ec99ae0d9ffe999a7f83448a29c48f35e',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_9f968aa131d08191a866ac85c08dd22b',deployment_id='appgdep_6a9cb235c690819194970fda23a8c180',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5654,current_local_reviewed=5654,remaining=12382,publication=p,completed_batch='Round31A30 published5654 version60 and live bytes verified',next_batch='Round31B/C input files ready; bounded5 agent evidence in round31b-agent-evidence.md, root verification needed')
h['next_actions'][0:0]=['Round31A published5654 version60 via remote build fallback after archive upload transport failed twice. Checks passed and live decompressed bytes equal local build. No active agents; round31b-agent-evidence.md contains5 bounded findings unverified byroot. Six older website repairs already live in preceding version59.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5654 live bytes verified')
