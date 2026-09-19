import pathlib,json,urllib.request,urllib.parse,subprocess,re
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw
b=pathlib.Path('work/research-2026/confirmed-logo-batch-sept12/recovery');rows=json.loads((b/'results.json').read_text());byname={r['name']:r for r in rows};q=[]
for name,idx in [('New England Telehealth Consortium',1),('Consumer Bankers Association',0),('National Home Infusion Association',0),('Washington Association Of Wheat Growers',0),('Data Center Coalition',0)]:
 r=byname[name];q.append(dict(id=r['id'],name=name,url=r['candidates'][idx]['url'],source=r['resolved_url']))
r=byname['Self Insurance Institute of America Inc'];q.append(dict(id=r['id'],name=r['name'],url='https://www.siia.org/templates/1012/images/siia_logo.svg',source=r['resolved_url']))
for name,selector in [('South Carolina Council on Competitiveness','div.logo svg'),('Davidson College','a.site-header__logo--desktop svg'),('Reading Is Fundamental, Inc.','a.logo svg')]:
 r=byname[name];s=BeautifulSoup((b/(r['id']+'.html')).read_text(),'html.parser');svg=s.select_one(selector);assert svg is not None
 assert not svg.find(['script','foreignobject'])
 svg['xmlns']='http://www.w3.org/2000/svg'
 if 'viewbox' in svg.attrs:svg['viewBox']=svg.attrs.pop('viewbox')
 raw=str(svg).encode();p=b/(r['id']+'-inline.svg');p.write_bytes(raw);q.append(dict(id=r['id'],name=name,local_source=str(p),source=r['resolved_url']))
for r in q:
 try:
  if r.get('local_source'):p=pathlib.Path(r['local_source']);raw=p.read_bytes()
  else:
   raw=urllib.request.urlopen(urllib.request.Request(r['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read();p=b/(r['id']+'-asset');p.write_bytes(raw)
  png=b/(r['id']+'-asset.png')
  if b'<svg' in raw[:600]:subprocess.run(['rsvg-convert','-w','350','-o',str(png),str(p)],capture_output=True,check=True)
  else:Image.open(p).convert('RGBA').save(png)
  r.update(status='downloaded',preview=str(png))
 except Exception as e:r.update(status='error',error=str(e))
(b/'asset-results.json').write_text(json.dumps(q,indent=2));ok=[r for r in q if r['status']=='downloaded'];sheet=Image.new('RGB',(800,len(ok)*155),'white');dr=ImageDraw.Draw(sheet)
for i,r in enumerate(ok):
 dr.text((10,i*155+5),r['name'],fill='black');im=Image.open(r['preview']).convert('RGBA');im.thumbnail((360,110));sheet.paste(im,(10,i*155+28),im);dr.rectangle((400,i*155+25,799,i*155+154),fill='#223344');sheet.paste(im,(410,i*155+28),im)
sheet.save(b/'recovered-sheet.png');print('Recovered assets',len(ok),'of',len(q))
