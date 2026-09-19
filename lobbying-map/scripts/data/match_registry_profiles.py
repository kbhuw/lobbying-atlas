"""Conservative, explicitly automatic registry matches using name plus city/state."""
import collections,datetime,gzip,json,pathlib,sqlite3
from organization_names import normalized
project=pathlib.Path(__file__).resolve().parents[2]
root=project.parent/'work/organization-research'
cs={c['id']:c for c in json.load(gzip.open(project/'public/data/directory-v2.json.gz'))['companies']}
candidate_names={normalized(x['sec']['name']) for x in json.loads((root/'sec-candidates.json').read_text())}
candidate_names.update(normalized(x['irs']['NAME']) for x in json.loads((root/'irs-candidates.json').read_text()))
byname=collections.defaultdict(list)
seen_locations=set()
with sqlite3.connect(f"file:{root/'bulk-profiles.sqlite'}?mode=ro",uri=True) as con:
 con.row_factory=sqlite3.Row
 for row in con.execute('SELECT * FROM descriptions'):
  r=dict(row)
  key=normalized(r['name'])
  loc=(key,r.get('city'),r.get('state'),r.get('principal_city'),r.get('principal_state'))
  if key in candidate_names and loc not in seen_locations:
   seen_locations.add(loc);byname[key].append(r)

def corroborate(id,name,city,state):
 if not city or not state:return None
 # Require the very same disclosed alias as the registry, not a different group member.
 if normalized(name) not in {normalized(a) for a in cs[id]['aliases']}:return None
 for r in byname.get(normalized(name),[]):
  locations=[(r.get('city'),r.get('state')),(r.get('principal_city'),r.get('principal_state'))]
  if any(normalized(c or '')==normalized(city) and normalized(s or '')==normalized(state) for c,s in locations):return r
 return None

def lda_source(r):
 return dict(label='House disclosure — '+r['source_member'],url=r['source_url'],claim=f"Disclosed client {r['name']}; reported location {r.get('city','')}, {r.get('state','')}; principal location {r.get('principal_city','')}, {r.get('principal_state','')}. Archive member {r['source_member']}; signed {r.get('signed_date') or 'date unavailable'}.")

def base(id,kind,ownership,description,sources,notes):
 return dict(name=cs[id]['name'],kind=kind,ownership=ownership,description=description,sources=sources,notes=notes,website='',status='registry_matched',as_of=datetime.datetime.now(datetime.timezone.utc).date().isoformat(),checked_at=datetime.datetime.now(datetime.timezone.utc).date().isoformat(),featured=False,legal_form='')
profiles={};rejected=collections.Counter()
for candidate in json.loads((root/'sec-candidates.json').read_text()):
 id=candidate['company_id'];sec=candidate['sec'];p=root/'sec-submissions'/f"{sec['cik']}.json"
 if not p.exists():continue
 doc=json.loads(p.read_text());d=doc['data'];address=d.get('addresses',{}).get('business',{})
 r=corroborate(id,d['name'],address.get('city'),address.get('stateOrCountry'))
 if not r:rejected['sec_no_location_corroboration']+=1;continue
 exchanges=[x for x in (d.get('exchanges') or []) if x];tickers=[x for x in (d.get('tickers') or []) if x]
 if not exchanges or not tickers:rejected['sec_no_exchange']+=1;continue
 description='SEC industry classification: '+d['sicDescription']+'.' if d.get('sicDescription') else 'Company appearing in SEC issuer records.'
 source=dict(label='SEC company record',url=doc['source_url'],claim=f"{d['name']} (CIK {sec['cik']}), industry {d.get('sicDescription') or 'unspecified'}, {address.get('city')}, {address.get('stateOrCountry')}; tickers {', '.join(tickers)}, exchanges {', '.join(exchanges)}.")
 profiles[id]=base(id,'Business','Publicly traded',description,[source,lda_source(r)],'Automatically matched by disclosed legal name and city/state against SEC records. This is a registry match, not an individual research review. The current issuer identity may not establish every historical filing or alias. Tickers: '+', '.join(tickers)+'. Exchanges: '+', '.join(exchanges)+'.')
 profiles[id]['registry']={'type':'SEC','id':str(sec['cik']),'match':'name_city_state'}

irs=collections.defaultdict(dict)
for r in json.loads((root/'irs-candidates.json').read_text()):irs[r['company_id']][r['irs']['EIN']]=r
ntee=dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXY',['Arts, culture and humanities','Education','Environment','Animal-related activities','Health care','Mental health and crisis intervention','Health associations and medical disciplines','Medical research','Crime and legal services','Employment','Food, agriculture and nutrition','Housing and shelter','Public safety and disaster relief','Recreation and sports','Youth development','Human services','International affairs and national security','Civil rights and advocacy','Community improvement','Philanthropy and grantmaking','Science and technology','Social science','Public and societal benefit','Religion-related activities','Mutual and membership benefit']))
for id,entries in irs.items():
 if id in profiles:rejected['registry_conflict']+=1;del profiles[id];continue
 matches=[]
 for candidate in entries.values():
  r=candidate['irs'];evidence=corroborate(id,r['NAME'],r['CITY'],r['STATE'])
  if evidence:matches.append((candidate,evidence))
 if len(matches)!=1:rejected['irs_ambiguous_or_no_location']+=1;continue
 candidate,evidence=matches[0];r=candidate['irs'];sub=r['SUBSECTION'].lstrip('0');status=r['STATUS'].zfill(2)
 if status not in ['01','02']:rejected['irs_unusual_status']+=1;continue
 kind='Trade / business association' if sub=='6' else 'Tax-exempt organization'
 sector=ntee.get((r.get('NTEE_CD') or '')[:1])
 description=('IRS activity classification: '+sector+'.') if sector else 'Organization appearing in the IRS tax-exempt organization register.'
 source=dict(label='IRS organization record — EIN '+r['EIN'],url=candidate['source_url'],claim=f"IRS extract record: {r['NAME']}, EIN {r['EIN']}, {r['CITY']}, {r['STATE']}; subsection {r['SUBSECTION']}, status {status}, NTEE {r.get('NTEE_CD') or 'unspecified'}. Data published {candidate['source_date']}.")
 profiles[id]=base(id,kind,'Not applicable',description,[source,dict(label='IRS field definitions',url='https://www.irs.gov/pub/irs-soi/eo-info.pdf',claim='Definitions of status, subsection and NTEE activity codes.'),lda_source(evidence)],'Automatically matched by disclosed name and city/state to one IRS identity. This is a registry match, not an individual research review. It does not establish every historical alias or imply donations are tax-deductible. Tax exemption is not a stock-market ownership category.')
 profiles[id]['as_of']=candidate['source_date'];profiles[id]['registry']={'type':'IRS','id':r['EIN'],'match':'name_city_state'}
(root/'registry-profiles.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2))
(root/'registry-progress.json').write_text(json.dumps({'matched':len(profiles),'types':dict(collections.Counter(p['registry']['type'] for p in profiles.values())),'excluded':dict(rejected),'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
print((root/'registry-progress.json').read_text())
