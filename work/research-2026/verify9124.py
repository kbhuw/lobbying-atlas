import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9124-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9124,commit_sha='d2553d3d18c86e6a6f7116da9c2a978a671d355a',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_909328db631481919ae79831559bbf23',deployment_id='appgdep_6a9d613cf77c8191991fb50ec1212a82',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9124,current_local_reviewed=9124,remaining=8912,publication=p,completed_batch='Round61 100 published9124 version99 and live bytes verified',next_batch='Round62 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9124 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9124 live bytes verified')
