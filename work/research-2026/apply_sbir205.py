import json,pathlib,copy,urllib.parse,hashlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));c=json.load(open(r/'sbir-unresolved-candidates.json'))
assert not (r/'featured205-before.json').exists()
excluded={'8183c712da0f2f98':'DNA technology versus energy-storage conflict; investigate identity before applying.','906ba6f6120a10b0':'Current Rebellion Industries branding requires continuity evidence.','a275308ae7608cba':'1999 award evidence too old for unresolved current identity.','2f0a598260e19c64':'2003 award evidence requires a current corroborating identity source.'}
def host(s):return urllib.parse.urlparse(s if '://' in s else 'https://'+s).netloc.lower().removeprefix('www.')
before={};dec=[]
for a in c:
 if not a['same_domain'] or a['id'] in excluded:continue
 i=a['id'];v=p[i];rows=[x for x in a['records'] if host(x['Company Website'])==host(v['website'])];assert rows
 before[i]=copy.deepcopy(v);x=max(rows,key=lambda x:x['Award Year'])
 n=f"Official SBIR award-data export names {x['Company']} (UEI {x['UEI']}) in {x['City']}, {x['State']}, and explicitly links the same organization domain {host(v['website'])}. The {x['Award Year']} award concerns {x['Award Title']}. This corroborates the legal-name and domain bridge alongside the prior activity evidence. Award records do not establish current ownership or website availability."
 if i=='a59ddfda41a16a84':n+=' Matched the New York entity CKMMHPL4HUU7; excluded the distinct Kansas DECISIVE-POINT LLC, UEI F4BHVL57MPD9.'
 v.update(review_outcome='confirmed',checked_at='2026-09-13',identity_evidence=n,notes=n)
 v['sources'].append(dict(url='https://data.www.sbir.gov/mod_awarddatapublic_no_abstract/award_data_no_abstract.csv',label='SBIR official award data: '+x['UEI'],claim=n))
 dec.append(dict(id=i,decision='confirmed_identity_only',evidence=rows,previous_notes=before[i]['notes'],notes=n))
assert len(dec)==43
for label,val in [('before',before),('decisions',dec),('deferred',excluded)]: (r/f'featured205-{label}.json').write_text(json.dumps(val,indent=2)+'\n')
(r/'sbir-source-manifest.json').write_text(json.dumps(dict(url='https://data.www.sbir.gov/mod_awarddatapublic_no_abstract/award_data_no_abstract.csv',discovery_url='https://www.sbir.gov/data-resources',downloaded_at='2026-09-14',sha256=hashlib.sha256((r/'sbir-awards-no-abstract.csv').read_bytes()).hexdigest(),candidate_count=96,matching_domain_candidates=47,reviewed_confirmed=43),indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print('Saved',len(dec),'identities; website and ownership statuses preserved')
