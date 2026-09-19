"""Validate exact input membership and required evidence before accepting research drafts."""
import json,pathlib,sys

def no_duplicates(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError(f'Duplicate JSON key: {k}')
  d[k]=v
 return d

def read(path):return json.loads(pathlib.Path(path).read_text(),object_pairs_hook=no_duplicates)
inputs=read(sys.argv[1]);draft=read(sys.argv[2]);expected={r['id'] for r in inputs}
if isinstance(draft,list):
 assert len({r['id'] for r in draft})==len(draft),'Duplicate record IDs'
 draft={r['id']:r for r in draft}
assert set(draft)==expected,f'ID mismatch: missing={expected-set(draft)}, extra={set(draft)-expected}'
for k,v in draft.items():
 assert isinstance(v,dict),f'{k}: unfinished record'
 assert v.get('id',k)==k,f'{k}: inner/outer ID mismatch'
 for field in ['name','description','kind','ownership','identity_evidence','review_outcome']:
  assert isinstance(v.get(field),str) and v[field].strip(),f'{k}: missing {field}'
 assert v['review_outcome'] in {'confirmed','partial','unresolved'},f'{k}: invalid review outcome'
 assert v.get('sources'),f'{k}: missing sources'
 for s in v['sources']:
  assert s.get('url','').startswith('https://') and s.get('claim','').strip(),f'{k}: invalid source'
 assert not(v['ownership'].lower()=='unknown' and v['review_outcome']=='confirmed'),f'{k}: unknown ownership marked confirmed'
print(f'{len(draft)} exact IDs validated; this checks structure, not truth of source claims')
