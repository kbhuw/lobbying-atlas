import json,pathlib,subprocess,io,concurrent.futures
from PIL import Image,ImageDraw
r=pathlib.Path('work/research-2026');exec((r/'check_general34a.py').read_text().split('p=json.load(open(root/')[0]);a=json.load(open(r/'round35b-logo-fixes.json'));dest=r/'round35b-image-audit';canvas=Image.new('RGB',(1200,400),'#d6d6d6');d=ImageDraw.Draw(canvas)
rows=json.load(open(r/'general-round35-b-input.json'));index={x['id']:i for i,x in enumerate(rows)};ok=[]
for j,(k,v) in enumerate(a.items()):
 if not v['url']:continue
 try:
  f,m,b=get(v['url']);impath=dest/f'fix{index[k]}.png'
  if 'svg' in m:
   svg=dest/f'fix{index[k]}.svg';svg.write_bytes(b);subprocess.run(['node','-e',"require('./lobbying-map/node_modules/sharp')(process.argv[1]).resize(160,130,{fit:'inside'}).png().toFile(process.argv[2])",str(svg),str(impath)],check=True,capture_output=True);b=impath.read_bytes()
  im=Image.open(io.BytesIO(b)).convert('RGBA');im.thumbnail((160,130));x=(j%6)*200;y=(j//6)*150;canvas.paste(im,(x,y+20),im);d.text((x,y),str(index[k]),fill='black')
  cp=r/f'website-cache/{k}.json';c=json.load(open(cp));c.update(logo_url=v['url'],logo_kind='logo',logo_source_url=v['source_url'],logo_http_status=200,logo_content_type=m);cp.write_text(json.dumps(c,indent=2)+'\n');ok.append(index[k])
 except Exception as e:print(index[k],str(e))
canvas.save(dest/'fixes.png');print('Fetched',ok)
