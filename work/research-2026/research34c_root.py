import json,pathlib,gzip,re,csv,urllib.parse
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round34-c-input.json'));e=json.load(open(r/'round34c-working-evidence.json'));p={}
s=(r/'research30c_root.py').read_text();helper=s[s.index('def add('):s.index("add(0,'Carbon")];exec((r/'filing_evidence.py').read_text());helper=helper.replace("filing=json.load(gzip.open('lobbying-map/public/data/reports/'+row['id'][:2]+'.json.gz','rt'))[row['id']][0]","filing,filing_member=latest_filing(row)");exec(helper)
g={z['Domain name']:z for z in csv.DictReader(open(r/'dotgov-current.csv'))}
states={'GA':'Georgia','TX':'Texas','FL':'Florida','NC':'North Carolina','CA':'California','AZ':'Arizona','NH':'New Hampshire','MN':'Minnesota','WA':'Washington','NY':'New York','ID':'Idaho','WV':'West Virginia','OH':'Ohio','IA':'Iowa'}
extra={4:'Ann Arbor, Michigan',6:'Arroyo Grande, California',16:'Baltimore, Maryland',20:'Baton Rouge and Parish of East Baton Rouge, Louisiana',22:'Bay Village, Ohio',26:'Benicia, California',30:'Bishop, California',35:'Boise, Idaho',38:'Brewton, Alabama',40:'Buckeye, Arizona',41:'Buena Park, California',48:'Calumet City, Illinois',50:'Camas, Washington',52:'Carlton, Oregon',53:'Carson, California',61:'Chewelah, Washington',63:'Chowchilla, California',71:'Coachella, California',72:'Coalinga, California',73:'Cocoa, Florida',76:'College Place, Washington',77:'Commerce City, Colorado',78:'Compton, California',84:'Daphne, Alabama',85:'Davenport, Iowa',86:'Daytona Beach, Florida',88:'Del Mar, California',91:'Des Moines, Iowa',94:'Dinuba, California'}
for i,row in enumerate(rows):
 v=e[row['id']];label=re.sub(r'^City of\s+','',v['name'],flags=re.I)
 for code,state in states.items():label=re.sub(r',?\s+'+code+r'$',', '+state,label,flags=re.I)
 label=extra.get(i,label.title());name='City of '+label
 desc=v['description'];notes=re.sub(r';? logo left blank.*','',v.get('notes',''),flags=re.I);web=v.get('website','');sources=[(s['url'],s['claim']) for s in v['sources']]
 if i>=66:desc='Municipal government serving '+label+'.'
 if i==52:notes+=' Historical House registration 301318844.xml explicitly identifies Carlton, Oregon.'
 if i==65:web='https://clantonal.gov/';sources=[(web,'Official Clanton city site identifies Clanton, Alabama, its City Council and municipal departments.')];notes='Correct current municipal domain established from official city site.'
 if i==68:
  name='City of Cleveland — Hopkins and Burke Lakefront airports';desc='City-owned airport system operating Cleveland Hopkins International Airport and Cleveland Burke Lakefront Airport in Ohio.';notes='The disclosed client is the City of Cleveland in its airport capacity, not an independent airport company.';sources=[(web,'City Port Control FAQ states Cleveland owns and operates both named airports and that the airport system is a city enterprise fund.')]
 if i in [73,74]:notes+=' Same municipality appears under two preserved filing-name groups; names alone are not treated as distinct governments.'
 host=urllib.parse.urlsplit(web).hostname or '';z=g.get(host.removeprefix('www.'))
 if z:sources.append(('https://github.com/cisagov/dotgov-data/blob/main/current-full.csv',f"CISA registry identifies {host.removeprefix('www.')} as registered to {z['Organization name'].strip()} in {z['City']}, {z['State']}; website content was checked separately."))
 add(i,name,desc,web,kind='Municipal airport system' if i==68 else 'Municipal government',own='Government body',sources=sources,notes=notes,outcome='partial' if i==68 else None,featured=i in [4,11,16,35,42,64,82,91])
(r/'general-round34c-root-draft.json').write_text(json.dumps(p,indent=2)+'\n');print(len(p),'normalized city profiles')
s=(r/'check_general34c.py').read_text().replace('round34c-working-evidence.json','general-round34c-root-draft.json');(r/'check_general34c_final.py').write_text(s)
