import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live8624-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=8624,commit_sha='0c27e9293b9d68abb4ad97be7ec4ae30286ab2f1',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_c9a7fc46069c819187e761e6c23b16b7',deployment_id='appgdep_6a9d4fdef5c08191b420b87b98d84a5d',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=8624,current_local_reviewed=8624,remaining=9412,publication=p,completed_batch='Round56 100 published8624 version94 and live bytes verified',next_batch='Next pending entries after Galderma Laboratories; Round57 research started')
h['active_deployment']=None
h['next_actions']=['8624 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('8624 live bytes verified')
