import gzip,json,hashlib,pathlib,datetime
r=pathlib.Path('work/research-2026')
a=pathlib.Path('work/live9724-check.gz').read_bytes();b=pathlib.Path('lobbying-map/dist/client/data/directory-v3.json.gz').read_bytes()
assert gzip.decompress(a)==gzip.decompress(b),'Live data differs from validated local build'
p=dict(reviewed=9724,commit_sha='8e0570d18186bebc7755e1fcbc194a1a36b4c6a4',version_id='appgprj_6a9b5690c32c8191a5efe6eb7ab19a84~appgver_f06e7f2a290081919b7fa8e25e3f1a7c',deployment_id='appgdep_6a9d74d942748191b4ad4a622b48a008',status='succeeded',live_bytes_verified=True,verification_scope='Decompressed live JSON exactly matches the validated local build.',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),gzip_sha256=hashlib.sha256(a).hexdigest(),json_sha256=hashlib.sha256(gzip.decompress(a)).hexdigest())
(r/'publication.json').write_text(json.dumps(p,indent=2)+'\n')
h=json.load(open(r/'latest-handoff.json'));h.update(current_live_reviewed=9724,current_local_reviewed=9724,remaining=8312,publication=p,completed_batch='Round67 100 published9724 version105 and live bytes verified',next_batch='Round68 next 100 selected; three research agents active')
h['active_deployment']=None
h['next_actions']=['9724 live verified. Select and research the next unreviewed 2026 entries.']
(r/'latest-handoff.json').write_text(json.dumps(h,indent=2)+'\n');print('9724 live bytes verified')
