import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live10424-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=10424,commit_sha='d0205160b6438ed2f6fa3c4c983f5c775c9aee32',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_be57b909797081919f2ffa8db75be90e',deployment_id='appgdep_6a9e095640bc81918be4a654e6760819',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=10424,current_local_reviewed=10424,remaining=7612,publication=p,completed_batch='Round74 100 published10424 version112 and live bytes verified',next_batch='Round74 selected; agents researching; 73 filing contexts and 11 IRS candidates saved')
h['active_deployment']=None
h['next_actions']=['10424 live verified. Review Round74 evidence and audit exact identities, ownership, and logos. Spark stays evidence-only.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('10424 live bytes verified')
