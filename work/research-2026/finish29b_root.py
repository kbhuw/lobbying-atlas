import pathlib,json
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round29b-root-draft.json'))
p['a0c7fe1c2bb3c8b5']['website']=''
p['a0c7fe1c2bb3c8b5']['notes']+=' Former website no longer resolves; retained historical policy document as evidence only.'
p['a0c7fe1c2bb3c8b5']['sources'].append(dict(label='Coalition member evidence',url='https://media.cancercare.org/documents/378/original/Cures-2.0-Letter_CLC_8.2.2024.pdf',claim='CancerCare hosts a 2024 Cancer Leadership Council policy letter identifying the coalition.'))
(r/'general-round29b-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
exec((r/'check_general28.py').read_text().split('p=json.load(open(root/')[0])
for k,u,kind in [('c24c1f530abe5fa0','https://www.securepassage.com/assets/svgs/trademark-logo.svg','logo'),('5bf6eb6e89c1ea0e','https://static.wixstatic.com/media/f1c650_88d94d79bcdc489cab1895a12ec5351a%7Emv2.png/v1/fill/w_180%2Ch_180%2Clg_1%2Cusm_0.66_1.00_0.01/f1c650_88d94d79bcdc489cab1895a12ec5351a%7Emv2.png','site_icon')]:
 f=r/f'website-cache/{k}.json';c=json.load(open(f));_,typ,b=get(u);assert typ.startswith('image/') and len(b)>80;c.update(logo_url=u,logo_kind=kind,logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=typ);f.write_text(json.dumps(c,indent=2)+'\n')
s=(r/'build_general29a.py').read_text().replace('general-round29a-root-draft.json','general-round29b-root-draft.json').replace('general-round29a-30-rootchecked.json','general-round29b-30-rootchecked.json')
a=s.index('hold=');b=s.index('\nfor k,v',a);s=s[:a]+"hold={'fac178db29f07a00','330c93e502ef1f4c','351a7de5f6934df6','760b1bedd0d35f4c'}"+s[b:];(r/'build_general29b.py').write_text(s)
