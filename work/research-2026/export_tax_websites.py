import pathlib,json,urllib.parse,re,datetime
root=pathlib.Path('work/research-2026');out={}
for f in (root/'tax-return-evidence').glob('*.json'):
 d=json.load(open(f))
 if d.get('parser_version')!=2 or d.get('status')!='filing_website_found':continue
 raw=d['filed_website'].strip().lower();url=raw if raw.startswith(('https://','http://')) else 'https://'+raw
 try:
  u=urllib.parse.urlparse(url)
  if not u.hostname or '.' not in u.hostname or ' ' in url or re.search(r'[,;\\]',u.netloc) or '@' in u.netloc or raw in ['n/a','none']:continue
  if u.scheme=='http':url='https://'+url[7:]
 except ValueError:continue
 out[d['id']]={'website':url,'website_status':'filed','website_ein':d['ein'],'website_checked_at':d['checked_at'],'website_source':{'label':'Website reported in IRS Form 990','url':d['source_url'],'claim':'The return for EIN '+d['ein']+' reports this website: '+d['filed_website']+'. Historical self-reported website; current control has not been independently checked.'}}
pathlib.Path('lobbying-map/research/registry-websites.json').write_text(json.dumps(out,indent=2)+'\n');print('Tax-return websites',len(out))
