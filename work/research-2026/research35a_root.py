import json,pathlib,gzip,re,csv,urllib.parse
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round35-a-input.json'));e={};p={}
for part in ['first67','middle67','last66']:e.update(json.load(open(r/f'round35a-{part}-evidence.json')))
s=(r/'research30c_root.py').read_text();helper=s[s.index('def add('):s.index("add(0,'Carbon")];exec((r/'filing_evidence.py').read_text());helper=helper.replace("filing=json.load(gzip.open('lobbying-map/public/data/reports/'+row['id'][:2]+'.json.gz','rt'))[row['id']][0]","filing,filing_member=latest_filing(row)");exec(helper)
state_src=(r/'match_government_domains.py').read_text();exec(state_src[state_src.index('state_names='):state_src.index('out={}')]);states=dict(zip(state_codes,state_names))
candidates=json.load(open(r/'round35a-government-domain-candidates.json'))
extra={4:'NJ',7:'OK',8:'OR',31:'CO',59:'FL',63:'CA',65:'WA',70:'IN',86:'AK',95:'FL',100:'AR',109:'CA',117:'FL',122:'CA',130:'CA',142:'AK',144:'NV',146:'SC',148:'NJ',164:'CA',165:'OH',168:'CA',171:'FL',177:'CA',188:'CA',195:'WA',196:'CO'}
for i,row in enumerate(rows):
 v=e[row['id']];codes=candidates[row['id']]['filing_states'];code=extra.get(i,codes[0] if len(codes)==1 else '');state=states.get(code,'');name=v['name']
 if i not in [58,63,109,110,173]:
  label=re.sub(r'^(City|Village) of\s+','',name,flags=re.I)
  if state:
   for j in range(3):label=re.sub(r'(?:,?\s+|\s*\()'+re.escape(state)+r'\)?$','',label,flags=re.I);label=re.sub(r',?\s+'+code+r'$','',label,flags=re.I)
  label=label.strip(' ,').title().replace('Mcallen','McAllen').replace('Mckinney','McKinney').replace("Lee'S", "Lee's")
  name=('Village of ' if i==57 else 'City of ')+label+(', '+state if state else '')
  desc='Municipal government serving '+label+(', '+state if state else '')+'.'
 else:desc=v['description']
 web=v.get('website','');sources=[(z['url'],z['claim']) for z in v['sources']]
 add(i,name,desc,web,kind=v.get('kind','Municipal government'),own=v.get('ownership','Government body'),sources=sources,notes=v.get('notes',''),outcome=v.get('review_outcome'),featured=i in [8,16,19,22,26,38,66,70,78,85,94,100,105,109,124,125,129,159,172,174,189,194])
(r/'general-round35a-root-draft.json').write_text(json.dumps(p,indent=2)+'\n');print(len(p),'normalized profiles')
