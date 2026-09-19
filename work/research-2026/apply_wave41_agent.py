import json,pathlib,copy,collections
root=pathlib.Path(__file__).resolve().parents[2];b=root/'work/research-2026/identity-wave41-bulk';path=root/'work/research-2026/reviewed.json';p=json.loads(path.read_text());a=json.loads((b/'agent-first44.json').read_text());m={x['id']:x for x in json.loads((b/'matches.json').read_text())};extra={'3534e57896e22af2','4c8cca02b17bdee5','6192c0f8e4654e7f','e2b7ab8ff75f9048','208372ea345a9712'}
for d in a:
 if d['id']=='1a0ca187daafb01':d['id']='1a0ca187daafb01e'
backup={x['id']:copy.deepcopy(p[x['id']]) for x in a}
for d in a:
 id=d['id']
 if id in extra:d.update(decision='hold',evidence='Exact filed legal entity remains uncorroborated beyond operating brand/group page; retain partial status.')
 if id=='93b73c519a37fda0':d.update(decision='confirm',evidence='Official page repeatedly identifies USA Rice including copyright, at the exact filed Arlington address.')
 if id=='e63516e3b7e277d1':d['evidence']='Full matched page does contain 3 Gill Street Suite D Woburn; exact Inc legal identity remains uncorroborated.'
 if d['decision']!='confirm':continue
 x=p[id];assert x['review_outcome']=='partial';r=m[id]['matches'][0]['registration'];proof=f"{d['evidence']} Registration: {r['client_name']}, {r['address']}, {r['city']}, {r['state']}; {r['archive']} / {r['member']}.";x.update(status='sourced',review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12');old=x.get('identity_evidence','');x['identity_evidence']=(old if isinstance(old,str) else json.dumps(old))+' '+proof;x['sources'] += [{'url':d['url'],'label':'Official identity and registration-address corroboration','claim':proof},{'url':r['source_url'],'label':'House registration archive: '+r['member'],'claim':proof}]
(b/'agent44-before.json').write_text(json.dumps(backup,indent=2,ensure_ascii=False));(b/'agent44-decisions.json').write_text(json.dumps(a,indent=2,ensure_ascii=False))
for f,pretty in [(path,True),(root/'lobbying-map/research/reviewed-2026.json',False),(root/'outputs/2026-research-trial/profiles.json',True)]:f.write_text(json.dumps(p,indent=2 if pretty else None,ensure_ascii=False))
allids=[x['id'] for x in a+json.loads((b/'local44-decisions.json').read_text())];assert len(allids)==88 and set(allids)==set(m);print(collections.Counter(x['decision'] for x in a));print(collections.Counter(x['review_outcome'] for x in p.values()))
