import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live5684-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=5684,commit_sha='df0d369f22be20b5abd88e758666fc49ad881444',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_5c1ca622512c81919c30090cf7abeee8',deployment_id='appgdep_6a9cb608a5108191b2565d373e18ddde',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=5684,current_local_reviewed=5684,remaining=12352,publication=p,completed_batch='Round31B30 published5684 version61 and live bytes verified',next_batch='Round31C input ready; agent researching bounded5, root verification needed')
h['next_actions'][0:0]=['Round31B published5684 version61 via remote build fallback after archive upload transport failed twice. Checks passed and live decompressed bytes equal local build. No active agents; round31c-agent-evidence.md contains5 bounded findings unverified byroot. Six older website repairs already live in preceding version59.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('5684 live bytes verified')
