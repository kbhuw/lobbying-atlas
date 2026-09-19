import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9024-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9024,commit_sha='17dde078dc71c01ed2114b91cc25186b89df7d53',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_b599380aa82081918d8279e228d6e97f',deployment_id='appgdep_6a9d5e85272c81919375a64108ec0ead',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9024,current_local_reviewed=9024,remaining=9012,publication=p,completed_batch='Round60 100 published9024 version98 and live bytes verified',next_batch='Round61 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9024 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9024 live bytes verified')
