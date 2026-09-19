import json,pathlib,concurrent.futures
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round91-input.json'));p=json.load(open(r/'round91-root-incremental-evidence.json'))
p[rows[9]['id']].update(ownership='Unknown',review_outcome='partial')
p[rows[10]['id']]['sources'].append(dict(url='https://ncrc.org/donate/',claim='Official donation FAQ explicitly identifies NCRC as a 501(c)(3) nonprofit coalition.'))
p[rows[15]['id']]['sources'].append(dict(url='https://www.nccn.org/',claim='Official homepage explicitly identifies NCCN as a not-for-profit alliance of leading cancer centers.'))
v=p[rows[16]['id']];v.update(description='Former trade association for concrete masonry producers, unified with the Interlocking Concrete Pavement Institute in July 2022 to form the organization now called the Concrete Masonry & Hardscapes Association. Its successor provides technical resources, education, standards and industry advocacy.',notes='Historical NCMA filing name retained. Successor CMHA website; do not conflate the association with the separately named NCMA Foundation.')
v['sources'].append(dict(url='https://www.cmha.org/news-and-insights/icpi-ncma-changes-name-to-the-concrete-masonry-hardscapes-association/',claim='Official successor announcement states NCMA and ICPI unification took effect July 1 2022, followed by adoption of CMHA name in 2023.'))
for i in [12,13]:p[rows[i]['id']]['sources']=[s for s in p[rows[i]['id']]['sources'] if 'philanthropy.org' not in s['url'] and 'propublica.org' not in s['url']]
(r/'round91-root-incremental-evidence.json').write_text(json.dumps(p,indent=2)+'\n')
exec((r/'check_round91_incremental.py').read_text().split('p=json.load(open(root/')[0])
changes={32:'https://www.ncpdp.org/NCPDP/media/images/NCPDPLogoImage.png',38:'https://www.ncssma.com/moto3/mt-content/uploads/2021/02/ncssma_logo_transparent.png',52:'https://www.ndrn.org/wp-content/uploads/2019/02/logo-white.png',53:'https://ndss.org/themes/custom/b5_subtheme/img/logo_NDSS_reverse.svg',63:'https://www.neefusa.org/themes/custom/neef/logo.svg',64:'https://www.firehero.org/wp-content/uploads/2023/02/NFFF-Logo-rev2023.png',79:'https://www.cdcfoundation.org/themes/foundation_cdcf/imgs/logo2.svg'}
def change(iv):
 i,u=iv;f=r/f"website-cache/{rows[i]['id']}.json";c=json.load(open(f))
 try:
  final,typ,b=get(u,1000000);assert typ.startswith('image/') and len(b)>80
  c.update(logo_url=u,logo_kind='logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=typ);f.write_text(json.dumps(c,indent=2)+'\n');return i,'corrected candidate'
 except Exception as e:return i,str(e)
for z in concurrent.futures.ThreadPoolExecutor(6).map(change,changes.items()):print(z)
