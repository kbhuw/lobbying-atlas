import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live7724-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=7724,commit_sha='e5608acaa2b184cadf8207c4200a1839290db93c',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_a337d3523db08191b6671b8d14ae5ab4',deployment_id='appgdep_6a9d2e240a1881919015fd9368cb49ad',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=7724,current_local_reviewed=7724,remaining=10312,publication=p,completed_batch='Round47 100 published7724 version85 and live bytes verified',next_batch='Next pending entries after Edgemark Development; not started')
h['active_deployment']=None
h['next_actions']=['7724 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('7724 live bytes verified')
