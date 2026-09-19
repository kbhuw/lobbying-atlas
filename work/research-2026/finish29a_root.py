import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round29a-root-draft.json'))
def source(k,u,c):p[k]['sources'].append(dict(label='Additional primary identity evidence',url=u,claim=c))
source('60dd00cf6bdfa293','https://www.cambriausa.com/privacy/','April 2026 privacy notice identifies Cambria Company LLC as the operator of CambriaUSA.com.')
source('0430a32704519d5a','https://www.calistacorp.com/shareholders/your-shareholder-role/','Calista states stock ownership is the basis of shareholder rights and benefits.')
source('c6339afc6d7582f4','https://camarapr.org/','Official chamber homepage describes private-business representation, advocacy, and member services.')
p['c6339afc6d7582f4']['website']='https://camarapr.org/'
# Historical take-private is firm, but current owner not re-established.
p['a1e0663a22fd5365']['review_outcome']='partial'
(r/'general-round29a-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
# Use checked organizational assets rather than a subsidiary or anniversary graphic.
exec((r/'check_general28.py').read_text().split('p=json.load(open(root/')[0])
for k,u,kind in [('39f9309ab800cb1b','https://www.calportland.com/wp-content/uploads/2026/04/cropped-calportland-favicon-180x180.png','site_icon'),('a1e0663a22fd5365','https://www.cambiumlearning.com/assets/img/C-logo-color.svg','logo')]:
 f=r/f'website-cache/{k}.json';c=json.load(open(f));dest,typ,b=get(u);assert typ.startswith('image/') and len(b)>80;c.update(logo_url=u,logo_kind=kind,logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=typ);f.write_text(json.dumps(c,indent=2)+'\n')
