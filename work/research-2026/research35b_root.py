import json,pathlib,gzip,re
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round35-b-input.json'));e={};p={}
for part in ['first67','middle67','last66']:e.update(json.load(open(r/f'round35b-{part}-evidence.json')))
e.update(json.load(open(r/'round35b-root-exceptions.json')))
s=(r/'research30c_root.py').read_text();helper=s[s.index('def add('):s.index("add(0,'Carbon")];exec((r/'filing_evidence.py').read_text());helper=helper.replace("filing=json.load(gzip.open('lobbying-map/public/data/reports/'+row['id'][:2]+'.json.gz','rt'))[row['id']][0]","filing,filing_member=latest_filing(row)");exec(helper)
c=json.load(open(r/'round35b-middle-critical-corrections.json'))
webfix={97:'https://clairity.com/about/',121:'https://cleanecon.org/contact-us/',122:'https://www.cleanenergyfuels.com/',126:'https://cleanfuels.org/',133:'https://cleancapital.com/'}
for i,row in enumerate(rows):
 v=e[row['id']];notes=v.get('notes','');own=v['ownership'];sources=[(x['url'],x['claim']) for x in v['sources']];out=v.get('review_outcome','partial');desc=v['description'];name=v['name'];web=v.get('website','')
 if row['id'] in c:
  z=c[row['id']];name=z['name'];desc=z['corrected_description'];own=z['proposed_ownership'];sources += [(x['url'],x['claim']) for x in z['sources']];notes=z['reasoning'];out='partial';web=webfix.get(i,web)
 if own.startswith('Public company'):own='Public company'
 if own.startswith('Subsidiary'):own='Subsidiary'
 if own in ['Nonprofit','Nonprofit organization','Nonprofit trade association']:own='Nonprofit / tax-exempt'
 if own=='Unknown':out='partial' if out!='unresolved' else out
 if i in [84,86,103,109,110,113,117,118,133]:own='Unknown';out='partial';notes+=' Current ownership has not been independently established by the cited sources.'
 if i in list(range(89,96))+list(range(109,117))+[172,173]:name+=' (via '+('CJ Lake' if i<96 else 'Clark Street Associates' if i<117 else 'Cline Strategic Consulting')+')';notes+=' Represents the named end client; the intermediary is not treated as its parent company.'
 if i in [125,126,127,128,129]:desc='Trade association representing biodiesel, renewable diesel and sustainable aviation fuel producers and related businesses.';own='Not applicable';v['kind']='Trade association';notes+=' Formerly National Biodiesel Board. Repeated filing-name variants retained for provenance.'
 if i==138:desc='Hong Kong-based lobbying client describing its business as consulting.'
 if i==184:desc='Belgium-based lobbying client describing advisory and consulting services.'
 add(i,name,desc,web,kind=v['kind'],own=own,sources=sources,notes=notes,outcome=out,featured=i in [7,12,13,22,42,46,57,99,100,101,102,111,112,114,115,116,136,145,155,156,181,183,192,194,196,197])
(r/'general-round35b-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
s=(r/'check_general34c_final.py').read_text().replace('general-round34c-root-draft','general-round35b-root-draft');(r/'check_general35b_final.py').write_text(s)
print(len(p),'normalized profiles')
