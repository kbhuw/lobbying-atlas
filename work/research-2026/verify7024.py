import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live7024-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=7024,commit_sha='599ba02f912d3621ede3d49f7a7d04bbacd949a4',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_6c5ae8aef1988191b3be218cd89b163b',deployment_id='appgdep_6a9d152c80c88191b01da6d0ef323f6e',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=7024,current_local_reviewed=7024,remaining=11012,publication=p,completed_batch='Round40 100 published7024 version78 and live bytes verified',next_batch='Next pending entries after County of Mariposa; not started')
h['active_deployment']=None
h['next_actions']=['7024 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('7024 live bytes verified')
