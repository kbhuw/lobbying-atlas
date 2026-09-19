import json,pathlib
r=pathlib.Path('work/research-2026');exec((r/'check_general30a.py').read_text().split('p=json.load(open(root/')[0])
f=r/'general-round30a-root-draft.json';p=json.load(open(f))
v=p['de1c9cbc427accb3'];v.update(description='U.S. subsidiary of Bayer AG, part of a group supplying medicines, consumer-health products, and agricultural products.',ownership='Subsidiary',website='https://www.bayer.com/en/us/conditions-of-use',notes='Bayer Corporation is the U.S. subsidiary; Bayer AG is the parent. Group website is linked, with parent logo held.',identity_evidence='Exact Bayer Corporation legal name and subsidiary relationship are stated on Bayer United States conditions of use.');v['sources'].append(dict(url=v['website'],label='Bayer US legal identity',claim='Official conditions identify Bayer Corporation, headquartered in Whippany, NJ, as a subsidiary of Bayer AG.'))
# Changed website needs its own check.
one(('de1c9cbc427accb3',v))
p['5d5dc15f7dda446e']['ownership']='Nonprofit / tax-exempt';p['5d5dc15f7dda446e']['sources'].append(dict(url='https://www.southcentralfoundation.com/wp-content/uploads/2017/01/CodeConduct.pdf',label='SCF code of conduct',claim='Identifies Southcentral Foundation as an Alaska Native owned and managed nonprofit health-care organization.'))
f.write_text(json.dumps(p,indent=2)+'\n')
k='c8bfdd9cf0d9921b';u='https://www.cookinlethousing.org/wp-content/uploads/2017/03/CIHA-all-white_2010_logo-1-291x140.png';dest,typ,b=get(u);assert typ.startswith('image/') and len(b)>80;c=json.load(open(r/f'website-cache/{k}.json'));c.update(logo_url=u,logo_kind='logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=typ);(r/f'website-cache/{k}.json').write_text(json.dumps(c,indent=2))
s=(r/'build_general29c.py').read_text().replace('29c','30a');a=s.index('hold=');b=s.index('\n',a);s=s[:a]+"hold={'de1c9cbc427accb3','046c31d4d337a1fb','b3c2d29c6b03754f'}"+s[b:];(r/'build_general30a.py').write_text(s)
