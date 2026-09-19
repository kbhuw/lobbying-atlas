"""Select current disclosure evidence across every member of a directory name group."""
import gzip,json,pathlib
REPORTS=pathlib.Path('lobbying-map/public/data/reports')
def latest_filing(row):
    candidates=[]
    for member in dict.fromkeys([row['id']]+row.get('members',[])):
        shard=REPORTS/(member[:2]+'.json.gz')
        if not shard.exists(): continue
        records=json.load(gzip.open(shard,'rt')).get(member,[])
        candidates.extend((record,member) for record in records)
    if not candidates: raise ValueError('No disclosure records for '+row['id'])
    return max(candidates,key=lambda pair:(pair[0].get('year',0),pair[0].get('posted_iso','')))
