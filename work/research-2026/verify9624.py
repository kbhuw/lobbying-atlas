import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9624-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9624,commit_sha='c725e19fb89900f5dfc4bab9b67a4e150668ae40',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_83c4a9456e8c8191bb195785443653cd',deployment_id='appgdep_6a9d71dcf68c819182d5331bbfc83c28',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9624,current_local_reviewed=9624,remaining=8412,publication=p,completed_batch='Round66 100 published9624 version104 and live bytes verified',next_batch='Round67 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9624 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9624 live bytes verified')
