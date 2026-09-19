import json,pathlib
r=pathlib.Path('work/research-2026');f=r/'general-round24-b-rootchecked.json';p=json.load(open(f));orig=json.load(open(r/'general-round24-b-researched.json'));fix=json.load(open(r/'general-round24-b-corrections.json'))
bmo=fix['f0bf8ebfe9f52517'];blg=fix['47b8341eed4dc92d']
for k,patch in [('f0b2a8ec1c996681',bmo),('f0bf8ebfe9f52517',blg)]:p[k]={**orig[k],**patch};p[k]['sources']+=orig[k]['sources']
k='47b8341eed4dc92d';p[k]=orig[k];p[k].update(website='https://www.firstcarolinabank.com/bmtechnologies/disclosures',ownership='Subsidiary of private or public company',review_outcome='confirmed',description='Provides digital banking technology and higher-education fund-disbursement services through BankMobile; acquired by First Carolina Bank in January 2025.',identity_evidence='The January 31, 2025 SEC 8-K states BM Technologies survived the completed acquisition as a wholly owned subsidiary of First Carolina Bank.');p[k]['sources'].append(dict(url='https://www.sec.gov/Archives/edgar/data/1725872/000121390025009521/ea0229196-8k_bmtech.htm',label='BM Technologies acquisition closing filing',claim='First Carolina completed its acquisition January 31, 2025 and BM Technologies survived as its wholly owned subsidiary.'))
v=p['59bf28014972933f'];v.update(website='',description='Biosecurity advocacy client whose exact legal relationship to Blueprint Biosecurity remains unverified.',review_outcome='partial',notes='The similarly named 501(c)(3) website is supporting context only; the Action entity has not been equated with it.')
v=p['05d8bf067cb761bf'];v.update(name='SPARC (via Blue Star Strategies)',ownership='Nonprofit / tax-exempt',review_outcome='confirmed')
f.write_text(json.dumps(p,indent=2)+'\n')
f=r/'general-round24-a-rootchecked.json';p=json.load(open(f));p['77aa8568273eef69'].update(ownership='Unknown',review_outcome='partial',notes='Current Florida insurer identity established; old nonprofit classification is not carried forward without current legal-form verification.')
p['d0b0b91706dbf8e6'].update(name='Blue Owl Capital Holdings LP',ownership='Unknown',review_outcome='partial',identity_evidence='The filing names Blue Owl Capital Holdings LP; the public Blue Owl Capital Inc. issuer is a separate legal entity. The group website provides operating context, but exact current ownership requires subsidiary evidence.',notes='Do not classify this LP as the NYSE-listed parent.');p['d0b0b91706dbf8e6']['sources']=[s for s in p['d0b0b91706dbf8e6']['sources'] if 'NYSE' not in s['claim']]
f.write_text(json.dumps(p,indent=2)+'\n')
p={}
for x in 'abc':p.update(json.load(open(r/f'general-round24-{x}-rootchecked.json')))
for k,v in p.items():
 if v['ownership'].startswith('Publicly traded') or v['ownership'].startswith('Public company'):v['ownership']='Publicly traded'
 if v['ownership'] in ['Government entity','Government / public institution']:v['ownership']='Government body'
 if v['ownership']=='Private nonprofit':v['ownership']='Nonprofit / tax-exempt'
 if v['ownership'].startswith('Privately held') or v['ownership']=='Private company (family-owned)':v['ownership']='Private company'
 if v['ownership']=='Unknown' and v['review_outcome']=='confirmed':v['review_outcome']='partial'
 v.setdefault('notes','')
 if v['ownership']=='Publicly traded':print(v['name'],json.dumps(v['sources']))
(r/'general-round24-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
