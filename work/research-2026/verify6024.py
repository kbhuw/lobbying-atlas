import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live6024-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=6024,commit_sha='2b4feb7d35aae7a8fd7245ed22a76edc27c725c0',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_2466db0f71348191a5f45bbb0544aca3',deployment_id='appgdep_6a9cf0869e408191b8961e497008c0f4',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=6024,current_local_reviewed=6024,remaining=12012,publication=p,completed_batch='Round34B100 published6024 version70 and live bytes verified',next_batch='Round34C100 municipal government evidence delegated; no integration yet')
h['active_deployment']=None
h['next_actions']=['6024 live verified. Complete Round34C evidence and logo audit, validate, integrate and publish.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('6024 live bytes verified')
