import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live6824-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=6824,commit_sha='591cb536fa69e33c132ac25e023d32b604327657',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_71e5a003cfd481919724399bb99c9834',deployment_id='appgdep_6a9d0e938d5481919ca6c4c010d603ca',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=6824,current_local_reviewed=6824,remaining=11212,publication=p,completed_batch='Round38 100 published6824 version76 and live bytes verified',next_batch='Next pending entries after Constellation Energy Generation; not started')
h['active_deployment']=None
h['next_actions']=['6824 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('6824 live bytes verified')
