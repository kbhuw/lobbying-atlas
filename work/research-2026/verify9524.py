import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9524-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9524,commit_sha='8da767e4902bf02a450e21e9cfbd218b97f8011e',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_ad0b9cae6c488191af71cce32888a111',deployment_id='appgdep_6a9d6e3dfd2c819193ea41fb2d1875e5',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9524,current_local_reviewed=9524,remaining=8512,publication=p,completed_batch='Round65 100 published9524 version103 and live bytes verified',next_batch='Round66 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9524 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9524 live bytes verified')
