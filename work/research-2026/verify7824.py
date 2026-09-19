import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live7824-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=7824,commit_sha='4a14395ba5e85748580d3ea211ef04e48280ee40',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_32e1d422f4488191af5ac82b4c199a6c',deployment_id='appgdep_6a9d319dd3d4819186043d241f529abd',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=7824,current_local_reviewed=7824,remaining=10212,publication=p,completed_batch='Round48 100 published7824 version86 and live bytes verified',next_batch='Next pending entries after ELLWOOD Quality Steels; not started')
h['active_deployment']=None
h['next_actions']=['7824 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('7824 live bytes verified')
