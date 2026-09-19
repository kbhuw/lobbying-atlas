import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live6724-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=6724,commit_sha='06e881507cc122a34baf42340be399909f9736c7',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_540177aa528c81918865f9c4554ce143',deployment_id='appgdep_6a9d0a694e008191af0cc8b56f88e228',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),registry_websites=1522,gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=6724,current_local_reviewed=6724,remaining=11312,publication=p,completed_batch='Round37 100 published6724 version75 and live bytes verified',next_batch='Next pending entries after Community Choice Financial Holdings; not started')
h['active_deployment']=None
h['next_actions']=['6724 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('6724 live bytes verified')
