import json,pathlib,gzip,sys
p=pathlib.Path('work/research-2026');batch=int(sys.argv[1]);dest=p/f'general-round{batch}-input.json'
assert not dest.exists(), 'Do not overwrite an existing assigned batch'
old=json.load(open(p/'reviewed.json'));q=[json.loads(s) for s in (p/'queue.jsonl').read_text().splitlines()]
companies={v['id']:v for v in json.load(gzip.open('lobbying-map/public/data/directory-v3.json.gz','rt'))['companies']};rows=[]
for v in q:
 if v['id'] in old:continue
 c=companies[v['id']];x={k:v[k] for k in ['id','name','year','prior_status','review_status','website_status','logo_status']}
 x.update(profile=c.get('profile',{}),aliases=c.get('aliases',[]),members=c.get('members',[]));rows.append(x)
 if len(rows)==100:break
assert len(rows)==100 and all(x['id'] not in old for x in rows)
dest.write_text(json.dumps(rows,indent=2)+'\n')
print(rows[0]['name'],'through',rows[-1]['name'])
