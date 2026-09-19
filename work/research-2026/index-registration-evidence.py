"""Build review candidates from exact original names, retaining filing provenance.
No candidate in this index automatically changes a profile or its ownership.
"""
import collections, csv, datetime, gzip, json, pathlib, unicodedata, xml.etree.ElementTree as ET, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
RESEARCH=ROOT/'work/research-2026'
def key(s):return ' '.join(unicodedata.normalize('NFKC',s or '').upper().split())
p=json.loads((RESEARCH/'reviewed.json').read_text())
base=json.load(gzip.open(ROOT/'lobbying-map/research/directory-base.json.gz','rt'))
targets={i for i,v in p.items() if v.get('website_status')!='verified' or v.get('ownership')=='Unknown'}
lookup=collections.defaultdict(set)
for c in base['companies']:
 if c['id'] in targets:
  for alias in c['aliases']:lookup[key(alias)].add(c['id'])
results=collections.defaultdict(list);errors=[];archives=[]
for path in sorted((ROOT/'work/federal-directory/raw').glob('*Registrations_XML.zip')):
 archives.append(path.name)
 with zipfile.ZipFile(path) as z:
  for member in z.namelist():
   if not member.lower().endswith('.xml'):continue
   try:root=ET.fromstring(z.read(member))
   except Exception as exc:errors.append({'archive':path.name,'member':member,'error':str(exc)});continue
   d={x.tag.rsplit('}',1)[-1]:(x.text or '').strip() for x in root}
   matches=lookup.get(key(d.get('clientName')))
   if not matches:continue
   row={'archive':path.name,'member':member,'source_url':'https://disclosurespreview.house.gov/data/LD/'+path.name,
        'client_name':d.get('clientName',''),'house_id':d.get('houseID',''),'senate_id':d.get('senateID',''),
        'registrant':d.get('organizationName',''),'address':d.get('clientAddress',''),'city':d.get('clientCity',''),
        'state':d.get('clientState',''),'country':d.get('clientCountry',''),'description':d.get('clientGeneralDescription',''),
        'effective_date':d.get('effectiveDate',''),'signed_date':d.get('signedDate','')}
   for i in matches:results[i].append(row)
 print(path.name,flush=True)
queue=[]
for i in sorted(targets):
 rows=results[i];locations=sorted({(key(x['city']),key(x['state']),key(x['country'])) for x in rows if x['city'] or x['state']})
 queue.append({'id':i,'name':p[i]['name'],'review_outcome':p[i]['review_outcome'],'website_status':p[i].get('website_status'),
  'ownership':p[i].get('ownership'),'registration_count':len(rows),'distinct_reported_locations':locations,
  'triage': 'no_exact_registration' if not rows else 'location_review_required' if len(locations)>1 else 'single_reported_location' if locations else 'registration_without_location',
  'evidence':rows})
queue.sort(key=lambda x:(x['review_outcome']!='unresolved',x['triage']!='single_reported_location',x['name']))
(RESEARCH/'registration-evidence-queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n')
summary={'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target_profiles':len(targets),'archives':archives,
 'profiles_with_exact_name_registration':sum(bool(x['evidence']) for x in queue),'unresolved_with_registration':sum(x['review_outcome']=='unresolved' and bool(x['evidence']) for x in queue),
 'triage_counts':dict(collections.Counter(x['triage'] for x in queue)),'parse_errors':errors,
 'limitations':'Exact original-name candidate retrieval only. Shared names, changed addresses, different legal entities and client IDs require review. Location agreement alone is not identity or ownership verification.'}
(RESEARCH/'registration-evidence-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
with (RESEARCH/'registration-evidence-queue.csv').open('w',newline='') as f:
 fields=['id','name','review_outcome','triage','registration_count','reported_locations'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for x in queue:w.writerow({**{k:x[k] for k in fields if k!='reported_locations'},'reported_locations':' | '.join(', '.join(t) for t in x['distinct_reported_locations'])})
print(json.dumps({k:v for k,v in summary.items() if k not in ['archives','parse_errors']},indent=2),flush=True)
