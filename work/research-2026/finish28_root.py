import pathlib,json
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round28-root-draft.json'))
v=p['b3790821676701bd'];v.update(ownership='Tribal-owned business',review_outcome='confirmed',identity_evidence='Caliber identifies itself as a federally chartered Section 17 corporation wholly owned by the Otoe-Missouria Tribe of Indians.');v['sources'].append(dict(url=v['website'],label='Official ownership disclosure',claim=v['identity_evidence']))
v=p['e09fd7a3ccb44984'];v['website']='https://www.calbioenergy.com/';v['sources']=[s for s in v['sources'] if 'cabioenergy.com' not in s['url']];v['sources'].append(dict(url='https://www.treasurer.ca.gov/caeatfa/meeting/2024/0916/4b3.pdf',label='State project record',claim='Letter from California Bioenergy LLC identifies www.calbioenergy.com as its website.'))
v=p['69b185a2ac4432ff'];v['website']='';v['sources']=[s for s in v['sources'] if 'calcoastalcrab.com' not in s['url']];v['identity_evidence']='California fisheries records identify the California Coastal Crab Association and its industry survey and policy work.';v['sources'].append(dict(url='https://opc.ca.gov/wp-content/uploads/2009/04/DCTF-Draft-Meeting-Summary-October-27-28-2021.pdf',label='State fisheries working group',claim=v['identity_evidence']))
for k,v in p.items():
 if v['ownership']=='Unknown' and v['review_outcome']=='confirmed':v['review_outcome']='partial'
(r/'general-round28-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
s=(r/'build_general27.py').read_text().replace('round27','round28');a=s.index('hold=');b=s.index('\nfor k,v',a);s=s[:a]+"hold={'dd304b3fd4586505','316b29bbc805fd93','cc67e0a104c5c1ad','274e5aa422676e2b','a4c2d6d6c4b63ea5','f4dea54181885e19'}"+s[b:];(r/'build_general28.py').write_text(s)
inputs=sum([json.load(open(r/f'general-round28-{s}-input.json')) for s in 'abc'],[]);(r/'general-round28-input.json').write_text(json.dumps(inputs,indent=2))
