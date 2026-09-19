import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live6924-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=6924,commit_sha='ca2cf0a56940ef1f8b0abed116b946c34fd2bb75',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_b04b3fae640481918bdfec944585ca37',deployment_id='appgdep_6a9d1215be708191bbbdf93d34ac9616',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=6924,current_local_reviewed=6924,remaining=11112,publication=p,completed_batch='Round39 100 published6924 version77 and live bytes verified',next_batch='Next pending entries after Cornell Atkinson Center for Sustainability; not started')
h['active_deployment']=None
h['next_actions']=['6924 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('6924 live bytes verified')
