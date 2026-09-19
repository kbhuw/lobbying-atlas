import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live10024-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=10024,commit_sha='ea4d4dc8b4cf3afc225822556d900c6c512e6013',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_e1af7a35dba08191a3ea6302fa6dd329',deployment_id='appgdep_6a9d8019c8d48191b6d27083b8bf7de5',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=10024,current_local_reviewed=10024,remaining=8012,publication=p,completed_batch='Round70 100 published10024 version108 and live bytes verified',next_batch='Round71 100 researched; identity and asset audits active')
h['active_deployment']=None
h['next_actions']=['10024 live verified. Finish Round71 identity and logo audits, then validate and integrate.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('10024 live bytes verified')
