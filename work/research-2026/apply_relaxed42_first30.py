import json,pathlib,copy,collections
r=pathlib.Path(__file__).resolve().parents[2];b=r/'work/research-2026';path=b/'reviewed.json';p=json.load(open(path));a=json.load(open(b/'relaxed-address42-agent30.json'));rows=json.load(open(b/'relaxed-address-candidates42.json'));m={x['id']:x for x in rows};holdindices={1,2,3,4,8,16,18,20,21,26};extra={rows[i]['id'] for i in holdindices};backup={x['id']:copy.deepcopy(p[x['id']]) for x in a}
for d in a:
 id=d['id'];d['decision']='confirm' if d['decision']=='propose' else 'hold'
 if id in extra:d.update(decision='hold',evidence='Exact registered legal entity or represented-client scope requires additional corroboration beyond displayed operating brand.')
 if id==rows[3]['id']:d['evidence']='Cached official contact page includes unrelated gambling promotion; seek independent primary identity evidence and a clean current page.'
 if d['decision']!='confirm':continue
 x=p[id];assert x['review_outcome']=='partial';z=m[id]['matches'][0]['registration'];proof=d['evidence']+' Street/city corroboration allows omitted suite: '+z['address']+', '+z['city']+'. Registration '+z['archive']+' / '+z['member'];old=x.get('identity_evidence','');x.update(review_outcome='confirmed',website_status='verified',status='sourced',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=(old if isinstance(old,str) else json.dumps(old))+' '+proof);x['sources'] += [{'url':d['url'],'label':'Official identity and street/city corroboration','claim':proof},{'url':z['source_url'],'label':'House registration archive: '+z['member'],'claim':proof}]
(b/'relaxed42-first30-before.json').write_text(json.dumps(backup,indent=2,ensure_ascii=False));(b/'relaxed42-first30-decisions.json').write_text(json.dumps(a,indent=2,ensure_ascii=False));assert len(a)==30 and set(x['id'] for x in a)==set(x['id'] for x in rows[:30])
for f,pretty in [(path,True),(r/'lobbying-map/research/reviewed-2026.json',False),(r/'outputs/2026-research-trial/profiles.json',True)]:f.write_text(json.dumps(p,indent=2 if pretty else None,ensure_ascii=False))
print(collections.Counter(x['decision'] for x in a))
