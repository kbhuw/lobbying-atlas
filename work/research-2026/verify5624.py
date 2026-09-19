import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5624-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5624,commit_sha='edef1375665ea1ef6afeb8fb1cecd6b3adf939b4',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_a28a4d8e92a88191880ce33ea4edaba9',deployment_id='appgdep_6a9cae1fa8c881919fefbe0b24e21cb5',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5624,current_local_reviewed=5624,remaining=12412,publication=p,completed_batch='Round30C30 published5624 version58 and live bytes verified',next_batch='Round31 A/B/C input files ready; bounded5 agent evidence in round31a-agent-evidence.md, root verification needed')
h['next_actions'][0:0]=['Round30C published5624 version58 via remote build fallback after archive upload transport failed twice. Checks passed and live decompressed bytes equal local build. No active agents; round31a-agent-evidence.md contains5 bounded findings unverified byroot. Correct6 malformed older websites before next publish.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5624 live bytes verified')
