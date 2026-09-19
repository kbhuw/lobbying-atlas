import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live6324-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=6324,commit_sha='c5e037c1e0d8273534c2868a0f16a54c9e35322a',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_a235384b92e88191b87ac48e86b3a951',deployment_id='appgdep_6a9cf6e492cc8191bf0343d7ff44953f',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=6324,current_local_reviewed=6324,remaining=11712,publication=p,completed_batch='Round35A200 published6324 version72 and live bytes verified',next_batch='Round35B200 evidence delegated; no integration yet')
h['active_deployment']=None
h['next_actions']=['6324 live verified. Complete Round35B evidence and logo audit, validate, integrate and publish.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('6324 live bytes verified')
