import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live7924-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=7924,commit_sha='74b1336af00643ae4cfc06eff2a367d19cd3be84',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_e384619bfb60819197caf797d2f48192',deployment_id='appgdep_6a9d34a111f881918db2f4ab539768d5',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=7924,current_local_reviewed=7924,remaining=10112,publication=p,completed_batch='Round49 100 published7924 version87 and live bytes verified',next_batch='Next pending entries after Energyforward; not started')
h['active_deployment']=None
h['next_actions']=['7924 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('7924 live bytes verified')
