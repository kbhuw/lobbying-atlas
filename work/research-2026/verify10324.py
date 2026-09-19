import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live10324-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=10324,commit_sha='7f9074c73c688ba631586bfb9021e7bee1ca30e0',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_c2fecccd10108191b13987538060cdc3',deployment_id='appgdep_6a9e02f85b208191981127f34e57991e',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=10324,current_local_reviewed=10324,remaining=7712,publication=p,completed_batch='Round73 100 published10324 version111 and live bytes verified',next_batch='Round74 selected; agents researching; 73 filing contexts and 11 IRS candidates saved')
h['active_deployment']=None
h['next_actions']=['10324 live verified. Review Round74 evidence and audit exact identities, ownership, and logos. Spark stays evidence-only.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('10324 live bytes verified')
