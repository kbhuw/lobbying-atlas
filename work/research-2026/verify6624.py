import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live6624-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=6624,commit_sha='579af8b326ba1b681d34f69a578d4f3110e05c4a',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_cfdcf9e3fe408191a86392a816056b03',deployment_id='appgdep_6a9d0674929c819189b46d08b6473235',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=6624,current_local_reviewed=6624,remaining=11412,publication=p,completed_batch='Round36 100 published6624 version74 and live bytes verified',next_batch='Next pending entries after Coleridge Initiative; not started')
h['active_deployment']=None
h['next_actions']=['6624 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('6624 live bytes verified')
