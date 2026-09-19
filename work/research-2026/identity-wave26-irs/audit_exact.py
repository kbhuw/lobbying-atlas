import csv,json,re,pathlib,sqlite3,zipfile,xml.etree.ElementTree as E,collections
D=pathlib.Path('work/research-2026');p=json.load(open(D/'reviewed.json'));norm=lambda s:re.sub('[^A-Z0-9]','',s.upper().replace('&','AND'));targets=collections.defaultdict(list)
for k,v in p.items():
 if v.get('review_outcome')!='confirmed':targets[norm(v['name'])].append(k)
irs=collections.defaultdict(dict)
for f in pathlib.Path('work/organization-research/irs').glob('eo*.csv'):
 for r in csv.DictReader(f.open()):
  n=norm(r['NAME'])
  if n in targets and r['STATUS']=='01':irs[n][r['EIN']]=dict(r,source_file=str(f))
print('Exact legal-name candidate sets',len(irs),flush=True)
c=sqlite3.connect('work/organization-research/bulk-profiles.sqlite');receipts=collections.defaultdict(list)
for name,z,m,u in c.execute("select name,source_zip,source_member,source_url from descriptions where source_zip like '%Registrations%'"):
 n=norm(name)
 if n in irs:receipts[n].append((z,m,u))
print('Candidates with registration names',len(receipts),flush=True)
zs={};accepted=[];deferred=[]
for n,rs in irs.items():
 matches=[]
 for z,m,u in receipts[n]:
  try:
   if z not in zs:zs[z]=zipfile.ZipFile('work/federal-directory/raw/'+z)
   e=E.fromstring(zs[z].read(m));fields={t.tag:(t.text or '').strip() for t in e.iter() if t.tag in ['clientName','clientAddress','clientCity','clientState','clientZip','clientGeneralDescription']}
   for ein,r in rs.items():
    if norm(fields.get('clientName',''))==norm(r['NAME']) and norm(fields.get('clientAddress',''))==norm(r['STREET']) and norm(fields.get('clientCity',''))==norm(r['CITY']) and fields.get('clientState')==r['STATE'] and fields.get('clientZip','')[:5]==r['ZIP'][:5]:
     matches.append(dict(irs=r,disclosure=dict(source_zip=z,source_member=m,source_url=u,fields=fields)))
  except (KeyError,FileNotFoundError,E.ParseError):pass
 eins={x['irs']['EIN'] for x in matches}
 for k in targets[n]:
  if len(eins)==1:accepted.append(dict(id=k,name=p[k]['name'],evidence=matches[0]))
  else:deferred.append(dict(id=k,name=p[k]['name'],reason='No unique full name/street/city/state/ZIP match'))
out=D/'identity-wave26-irs';out.mkdir(exist_ok=True);(out/'audit.json').write_text(json.dumps(dict(accepted=accepted,deferred=deferred,method='Exact normalized legal name and full business street, city, state, five-digit ZIP; unique EIN; active status in locally saved IRS file. No ownership, website or logo inference.'),indent=2));print('Accepted',len(accepted),'deferred',len(deferred),flush=True);print([(x['name'],x['evidence']['irs']['SUBSECTION']) for x in accepted[:20]])
