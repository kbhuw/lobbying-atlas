import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9324-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9324,commit_sha='3253e2d407bc7b1c915a23554bb09a91f09ab55a',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_985fe71176688191b36fec3a6310ebe3',deployment_id='appgdep_6a9d67d6477c8191ad7e5d9ce1646c73',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9324,current_local_reviewed=9324,remaining=8712,publication=p,completed_batch='Round63 100 published9324 version101 and live bytes verified',next_batch='Round64 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9324 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9324 live bytes verified')
