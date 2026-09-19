import pathlib,json,re,html,urllib.parse
r=pathlib.Path('work/research-2026');exec((r/'check_general33b.py').read_text().split('p=json.load(open(root/')[0]);p=json.load(open(r/'general-round33b-root-draft.json'));byname={v['name']:k for k,v in p.items()}
def asset(name,u):
 k=byname[name];f=r/f'website-cache/{k}.json';c=json.load(open(f));dest,m,b=get(u);assert m.startswith('image/') and len(b)>80;(c.update(logo_url=u,logo_kind='logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=m));f.write_text(json.dumps(c,indent=2)+'\n');print(name,m,len(b))
_,_,b=get('https://charmindustrial.com/');s=b.decode();tag=re.search(r'<img[^>]*alt="Charm Industrial Homepage"[^>]*>',s).group();u=html.unescape(re.search(r' src="([^"]+)"',tag).group(1));u=urllib.parse.urljoin('https://charmindustrial.com/',u);asset('Charm Industrial',u)
asset('CharterCARE Health of Rhode Island','https://chartercarehealth.org/wp-content/uploads/2025/06/CCHRI-Blue-Hill-No-Tag-RGB-OL.png')
