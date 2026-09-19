import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live10124-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=10124,commit_sha='fe2541702d9f61668c004a68e419765f3eb697ae',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_13fe99ccb3508191a08b1deee17284e1',deployment_id='appgdep_6a9dfcb8ae3c819193b7eae7c596c287',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=10124,current_local_reviewed=10124,remaining=7912,publication=p,completed_batch='Round71 100 published10124 version109 and live bytes verified',next_batch='Round72 selected; research not started')
h['active_deployment']=None
h['next_actions']=['10124 live verified. Start Round72 research; Spark quote extraction pilot results and validator saved.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('10124 live bytes verified')
