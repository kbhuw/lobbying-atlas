import json,pathlib,copy,collections
r=pathlib.Path(__file__).resolve().parents[2];b=r/'work/research-2026/transport-recovery43';path=r/'work/research-2026/reviewed.json';p=json.loads(path.read_text());a=json.load(open(b/'agent-first31.json'));m={x['id']:x for x in json.load(open(b/'matches.json'))};a=[x for x in a if x['id']!='0b88954e885188cb'];backup={x['id']:copy.deepcopy(p[x['id']]) for x in a}
for d in a:
 id=d['id'];d['decision']=d['decision']
 if id in {'ee5c59fb09be0ef9','bee7cada24d3982d'}:d.update(decision='confirm',evidence='Official site identifies the filed unsuffixed operating name, same address and same business activity. This does not assign subsidiary identity or parent ownership.')
 if d['decision']!='confirm':continue
 x=p[id];assert x['review_outcome']=='partial';reg=m[id]['matches'][0]['registration'];proof=d['evidence']+' Registration: '+reg['client_name']+', '+reg['address']+', '+reg['city']+'; '+reg['archive']+' / '+reg['member'];old=x.get('identity_evidence','');x.update(review_outcome='confirmed',website_status='verified',status='sourced',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=(old if isinstance(old,str) else json.dumps(old))+' '+proof);x['sources'] += [{'url':d['url'],'label':'Official identity and address corroboration','claim':proof},{'url':reg['source_url'],'label':'House registration archive: '+reg['member'],'claim':proof}]

(b/'agent31-before.json').write_text(json.dumps(backup,indent=2,ensure_ascii=False));(b/'agent31-decisions.json').write_text(json.dumps(a,indent=2,ensure_ascii=False));ids=[x['id'] for x in a+json.load(open(b/'local31-decisions.json'))];assert len(ids)==62 and set(ids)==set(m)
for f,pretty in [(path,True),(r/'lobbying-map/research/reviewed-2026.json',False),(r/'outputs/2026-research-trial/profiles.json',True)]:f.write_text(json.dumps(p,indent=2 if pretty else None,ensure_ascii=False))
print(collections.Counter(x['decision'] for x in a));print(collections.Counter(x['review_outcome'] for x in p.values()))
