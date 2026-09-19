import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9224-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9224,commit_sha='b08c3bb63f19b995f90e96d651ee8df96c796fa2',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_cbee13c4e28c819193f6a231778622b3',deployment_id='appgdep_6a9d63fd76fc8191a7975b2e44bc89e1',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9224,current_local_reviewed=9224,remaining=8812,publication=p,completed_batch='Round62 100 published9224 version100 and live bytes verified',next_batch='Round63 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9224 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9224 live bytes verified')
