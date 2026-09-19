import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live8924-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=8924,commit_sha='7b626fd6d9b015a236cf9bd3567e5f01097df4c4',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_b888f8f3c4808191bc65646d7ecb02da',deployment_id='appgdep_6a9d5ab5cd18819196128f26833d99ea',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=8924,current_local_reviewed=8924,remaining=9112,publication=p,completed_batch='Round59 100 published8924 version97 and live bytes verified',next_batch='Next pending entries after Government of US Virgin Islands; prepare Round60 input')
h['active_deployment']=None
h['next_actions']=['8924 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('8924 live bytes verified')
