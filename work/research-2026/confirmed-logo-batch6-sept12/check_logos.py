import json,pathlib,urllib.request,urllib.parse,concurrent.futures,subprocess
from PIL import Image,ImageDraw
b=pathlib.Path('work/research-2026/confirmed-logo-batch6-sept12');c=b/'logos';c.mkdir(exist_ok=True);d=json.load(open('work/research-2026/reviewed.json'));q=[]
for r in json.loads((b/'website-results.json').read_text()):
 if r['status']!='fetched' or d[r['id']].get('logo_kind')=='logo' or not r.get('logo_candidates'):continue
 z=r['logo_candidates'][0]
 if not z.get('src') or z['src'].startswith('data:'):continue
 q.append({'id':r['id'],'name':r['name'],'source':r['resolved_url'],'url':urllib.parse.urljoin(r['resolved_url'],z['src']).replace('http://','https://',1),'alt':z.get('alt','')})
def run(r):
 try:
  raw=urllib.request.urlopen(urllib.request.Request(r['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read();is_svg=b'<svg' in raw[:500];p=c/(r['id']+('.svg' if is_svg else '.image'));p.write_bytes(raw);png=c/(r['id']+'.png')
  if is_svg:subprocess.run(['rsvg-convert','-w','350','-o',str(png),str(p)],check=True,capture_output=True)
  else:Image.open(p).convert('RGBA').save(png)
  r.update(status='downloaded',preview=str(png))
 except Exception as e:r.update(status='error',error=str(e))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:rr=list(ex.map(run,q))
(b/'logo-results.json').write_text(json.dumps(rr,indent=2));ok=[r for r in rr if r['status']=='downloaded'];sheet=Image.new('RGB',(800,len(ok)*155),'white');dr=ImageDraw.Draw(sheet)
for i,r in enumerate(ok):
 dr.text((10,i*155+5),r['name'],fill='black');im=Image.open(r['preview']).convert('RGBA');im.thumbnail((360,110));sheet.paste(im,(10,i*155+28),im);dr.rectangle((400,i*155+25,799,i*155+154),fill='#223344');sheet.paste(im,(410,i*155+28),im)

for n in range(0,len(ok),10):sheet.crop((0,n*155,800,min(n+10,len(ok))*155)).save(c/('sheet-'+str(n//10)+'.png'))
print('Downloaded',len(ok),'of',len(rr))
