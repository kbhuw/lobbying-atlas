import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5714-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5714,commit_sha='4394b1207d9f17d38f476d6ec35e61b0c59fccdd',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_62c7b6cfd71881919a716a3b5314bfbc',deployment_id='appgdep_6a9ccb226c1c8191a70782e04c203391',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5714,current_local_reviewed=5714,remaining=12322,publication=p,completed_batch='Round31C30 published5714 version62 and live bytes verified',next_batch='Round32A input ready; agent researching bounded5, root research pending')
h['next_actions'][0:0]=['Round31C published5714 version62 via remote build fallback after archive upload transport failed twice. Checks passed and live decompressed bytes equal local build. No active agents; round31c-agent-evidence.md contains5 bounded findings unverified byroot. Six older website repairs already live in preceding version59.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5714 live bytes verified')
