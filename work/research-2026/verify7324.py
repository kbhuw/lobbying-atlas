import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live7324-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=7324,commit_sha='bb01547db1183a87f089166461221458799ca3b4',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_f6828cc6d0788191be2f9f2523180198',deployment_id='appgdep_6a9d1f5dcad08191a7d4f6487f469ca1',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=7324,current_local_reviewed=7324,remaining=10712,publication=p,completed_batch='Round43 100 published7324 version81 and live bytes verified',next_batch='Next pending entries after Definium Therapeutics; not started')
h['active_deployment']=None
h['next_actions']=['7324 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('7324 live bytes verified')
