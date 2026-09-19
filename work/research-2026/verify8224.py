import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live8224-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=8224,commit_sha='880f293ef3db5fb1a765e5ee04622dd21b6d8648',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_b4e34dff8bc88191bf5904baec0b040b',deployment_id='appgdep_6a9d3f85cba08191a13d0e951f99c30e',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=8224,current_local_reviewed=8224,remaining=9812,publication=p,completed_batch='Round52 100 published8224 version90 and live bytes verified',next_batch='Next pending entries after FCA International; not started')
h['active_deployment']=None
h['next_actions']=['8224 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('8224 live bytes verified')
