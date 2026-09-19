import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'merge32c_evidence.py').read_text());a=json.load(open(r/'round32c-last9-evidence.json'))
for k,v in a.items():
 i=index[k];own='Government body' if i==28 else 'Nonprofit / tax-exempt' if i in [22,25] else 'Unknown';outcome='confirmed' if i==28 else 'partial';name=v['name'];desc=v['description'];notes=v['notes']
 if i==21:notes+=' Founder and corporate form do not establish current equity ownership; private ownership claim withheld.'
 if i==22:name='Center for Employment Opportunities (CEO)';notes+=' Exact tax subsection requires primary confirmation; nonprofit identification supported by organization reporting.'
 if i==23:
  name='CEPI-U.S.';desc='United States advocacy and education organization representing the Coalition for Epidemic Preparedness Innovations in Norway.';notes='A 2020 self-registration describes advocacy and education on behalf of CEPI Norway. Group website provided for context; exact current US legal and tax status remain unconfirmed.'
  v['sources'].append(dict(url='https://disclosurespreview.house.gov/data/LD/2020_Registrations_XML.zip',claim='House self-registration 301227313.xml identifies advocacy and education on behalf of CEPI Norway, signed November 24, 2020.'))
 if i==24:notes+=' Investment in private equity does not establish whether the adviser itself is privately held; current owner structure not verified.'
 if i==26:notes+=' Exact direct ownership chain of the US filing entity not established; group logo held.'
 if i==27:notes+=' Current ownership not established by cited activity descriptions.'
 if i==29:notes+=' Historical website retained as transition evidence; no diagnostic-effectiveness claims adopted.'
 add(i,name,desc,v['website'],kind=v['kind'].replace('Privately held ','').replace('Private ',''),own=own,sources=[(s['url'],s['claim']) for s in v['sources']],notes=notes,outcome=outcome,featured=i==24)
assert len(p)==30
(r/'general-round32c-root-draft.json').write_text(json.dumps(p,indent=2)+'\n');print('30 drafts assembled; pending verification')
