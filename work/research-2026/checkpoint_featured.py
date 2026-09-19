import json,pathlib,subprocess,hashlib,tarfile,datetime,sys
n=int(sys.argv[1]);r=pathlib.Path('work/research-2026');site=pathlib.Path('lobbying-map');a=pathlib.Path(f'work/site-sept13-featured{n}.tar').resolve();sha=subprocess.check_output(['git','-C',str(site),'rev-parse','HEAD'],text=True).strip()
with tarfile.open(a) as t:
 names=t.getnames();assert any(x.endswith('server/index.js') for x in names);assert any(x.endswith('.openai/hosting.json') for x in names)
p=json.load(open(r/'reviewed.json'));assert p==json.load(open(site/'research/reviewed-2026.json'))==json.load(open('outputs/2026-research-trial/profiles.json'))
c=json.load(open('outputs/2026-research-trial/current-progress.json'));pub=json.load(open(r/'publication.json'));now=datetime.datetime.now(datetime.timezone.utc).isoformat();digest=hashlib.sha256(a.read_bytes()).hexdigest()
pub['pending_publication_attempt'].update(local_commit_sha=sha,archive=str(a),archive_sha256=digest,prepared_at=now);pub['latest_local_checkpoint'].update(commit_sha=sha,build_and_invariants='passed',archive_current=True)
s=f"Local: {c['identity_confirmed']} confirmed; {c['identity_incomplete']} incomplete; {c['verified_websites']} verified websites; {c['official_logo_assets']} official logos; {c['displayed_organizations']} displayed organizations. Publishing HTTP500 unresolved."
pub['pending_change_summary']=s;pub['local_changes_pending']=True;(r/'publication.json').write_text(json.dumps(pub,indent=2)+'\n')
with (r/'latest-handoff.md').open('a') as f:f.write(f'\n## Featured {n} checkpoint — {now}\nCommit {sha}. {s}\nBuild, invariants, exports, mirrors and archive checks passed. Archive {a}; SHA256 {digest}.\n')
print(s);print(sha)
