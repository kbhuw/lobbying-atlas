import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live8724-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=8724,commit_sha='9b0f0aba364ed19ae6c67b08f7d5d387a15a96bb',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_d903e6c8bb908191bfd0b0d4d5128bfb',deployment_id='appgdep_6a9d548ca6dc8191b837db134d9f6d9b',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=8724,current_local_reviewed=8724,remaining=9312,publication=p,completed_batch='Round57 100 published8724 version95 and live bytes verified',next_batch='Next pending entries after Genomatica; Round58 evidence saved and awaiting root review')
h['active_deployment']=None
h['next_actions']=['8724 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('8724 live bytes verified')
