import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live8424-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=8424,commit_sha='8ad1bcfccbce89e11f08e8afb53a9134f2933a43',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_23d0045c32988191925cdc34b2bb0929',deployment_id='appgdep_6a9d48625de08191816c2033d04f574d',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=8424,current_local_reviewed=8424,remaining=9612,publication=p,completed_batch='Round54 100 published8424 version92 and live bytes verified',next_batch='Next pending entries after Fluor Enterprises; not started')
h['active_deployment']=None
h['next_actions']=['8424 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('8424 live bytes verified')
