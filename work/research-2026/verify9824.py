import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9824-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9824,commit_sha='a246d2a9ea8cf5653a7e28fbd810ad920810624d',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_f3bfd799e0ec81919695337ab5b3bf4c',deployment_id='appgdep_6a9d7947b98881919f32cc049c84aea0',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9824,current_local_reviewed=9824,remaining=8212,publication=p,completed_batch='Round68 100 published9824 version106 and live bytes verified',next_batch='Round69 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9824 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9824 live bytes verified')
