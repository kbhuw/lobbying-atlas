import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'research33a_root.py').read_text());index={x['id']:i for i,x in enumerate(rows)};a=json.load(open(r/'round33a-first10-evidence.json'))
for k,v in a.items():
 i=index[k];own='Nonprofit / tax-exempt' if i==1 else 'Publicly traded' if i==5 else 'Subsidiary' if i in [7,8,9] else 'Unknown';notes=v['notes'];name=v['name'];web=v['website'];sources=v['sources'];kind=v['kind'].replace('Public ','');desc=v['description'];outcome=None
 if i==2:name='CertiK (Certified Kernel Tech LLC)'
 if i==3:name='Certree (Auth9, Inc.)'
 if i==6:name='CesiumAstro, Inc.'
 if i==7:
  name='CF Industries, Inc.';notes='Latest filing identifies CF Industries Inc, a wholly owned subsidiary of CF Industries Holdings Inc. Parent ticker NYSE: CF is not assigned to this operating subsidiary. Shortened filing variant retained.';sources=[s for s in sources if 'stock-info' not in s['url']];sources.append(dict(url='https://www.sec.gov/Archives/edgar/data/1324404/000132440426000007/cf-20251231.htm',claim='2025 annual report explicitly distinguishes CF Industries Holdings Inc from 100% owned subsidiary CF Industries Inc.'))
 if i==8:notes+=' Exact intermediate ownership chain not independently established.';outcome='partial'
 if i==9:
  name='CF&I Steel LP (Rocky Mountain Steel Mills)';web='https://www.rockymountainsteelmills.com/';desc='Pueblo, Colorado steel producer manufacturing rail, wire rod, reinforcing bar and tubular products.';notes='Historical CF&I Steel LP and Rocky Mountain Steel identity supported by filings. EVRAZ ownership references are historical: Atlas completed acquisition of EVRAZ North America in July 2025 and formed Orion Steel. Current exact direct legal holding chain remains partial.';outcome='partial'
  sources.append(dict(url='https://www.atlasholdingsllc.com/news/atlas-completes-acquisition-of-steelmaker-evraz-north-america-forms-orion-steel-and-appoints-doug-matthews-ceo/',claim='Atlas July 31 2025 announcement confirms acquisition and Orion Steel ownership of Rocky Mountain Steel Mills.'));sources.append(dict(url=web,claim='Current mill website identifies Pueblo location and steel products.'))
 add(i,name,desc,web,kind=kind,own=own,sources=[(s['url'],s['claim']) for s in sources],notes=notes,outcome=outcome,featured=i in [2,6,7])
(r/'general-round33a-root-draft.json').write_text(json.dumps(p,indent=2)+'\n');print(len(p),'drafts assembled')
(r/'check_general33a.py').write_text((r/'check_general32c.py').read_text().replace('32c','33a'))
