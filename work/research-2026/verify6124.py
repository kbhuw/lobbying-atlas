import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live6124-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=6124,commit_sha='275544c66d79d3d821a0812f9c0bbd74858e4cfa',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_057257becf9c8191928c9ddcaa79b7f7',deployment_id='appgdep_6a9cf384172881919aeb49cdf0ff0361',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=6124,current_local_reviewed=6124,remaining=11912,publication=p,completed_batch='Round34C100 published6124 version71 and live bytes verified',next_batch='Round35A200 municipal government evidence delegated; no integration yet')
h['active_deployment']=None
h['next_actions']=['6124 live verified. Complete Round35A evidence and logo audit, validate, integrate and publish.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('6124 live bytes verified')
