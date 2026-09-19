import json,pathlib,io,concurrent.futures
from PIL import Image,ImageDraw
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round45-input.json'));exec((r/'check_general34a.py').read_text().split('p=json.load(open(root/')[0]);dest=r/'round45-image-audit';dest.mkdir(exist_ok=True)
def fetch(iv):
 i,v=iv;f=r/f"website-cache/{v['id']}.json";c=json.load(open(f)) if f.exists() else {};u=c.get('logo_url','');out={'id':v['id'],'index':i,'url':u}
 if not u:return out
 try:
  final,mime,b=get(u,1000000);out.update(http_status=200,mime=mime)
  if 'svg' in mime:
   import subprocess
   f=dest/f'{i}.svg';f.write_bytes(b);png=dest/f'{i}.png'
   subprocess.run(['node','-e',"require('./lobbying-map/node_modules/sharp')(process.argv[1]).resize(145,100,{fit:'inside'}).png().toFile(process.argv[2])",str(f),str(png)],capture_output=True,check=True,timeout=15)
   b=png.read_bytes()
  im=Image.open(io.BytesIO(b)).convert('RGBA');im.thumbnail((145,100));out['image']=im;out['size']=len(b)
 except Exception as e:out['error']=str(e)
 return out
results=list(concurrent.futures.ThreadPoolExecutor(max_workers=8).map(fetch,enumerate(rows)))
canvas=Image.new('RGB',(1600,1450),'#d6d6d6');d=ImageDraw.Draw(canvas)
for z in results:
 i=z['index'];x=(i%10)*160;y=(i//10)*145;d.text((x+3,y+3),str(i)+' '+rows[i]['name'].replace('City Of ','')[:20],fill='black')
 im=z.pop('image',None)
 if im:canvas.paste(im,(x+8,y+27),im)
 else:d.text((x+8,y+50),'SVG' if z.get('svg') else 'no image',fill='black')
canvas.save(dest/'contact-sheet.png');(dest/'fetches.json').write_text(json.dumps(results,indent=2)+'\n');print('Image audit sheet ready')
