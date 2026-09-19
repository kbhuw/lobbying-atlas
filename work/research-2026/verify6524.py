import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live6524-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=6524,commit_sha='6c7def6c5fc61deb0ea54446d35a1028c861a971',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_dd3c999c93a48191b301877cdd28e442',deployment_id='appgdep_6a9cfca0446c8191aad88424b2984b7e',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=6524,current_local_reviewed=6524,remaining=11512,publication=p,completed_batch='Round35B200 published6524 version73 and live bytes verified',next_batch='Next 200 pending entries after Coachella Valley Water District; not started')
h['active_deployment']=None
h['next_actions']=['6524 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('6524 live bytes verified')
