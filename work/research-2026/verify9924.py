import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9924-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9924,commit_sha='95cc450edb9232f750e86353f1e21d01a4d5e770',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_69d566640440819187cea3e8674ecb3c',deployment_id='appgdep_6a9d7cbf4d388191a7d60673752a4ad9',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9924,current_local_reviewed=9924,remaining=8112,publication=p,completed_batch='Round69 100 published9924 version107 and live bytes verified',next_batch='Round70 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9924 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9924 live bytes verified')
