import json,pathlib,subprocess,io
from PIL import Image,ImageDraw
r=pathlib.Path('work/research-2026');exec((r/'check_general37_final.py').read_text().split('p=json.load(open(root/')[0]);a=json.load(open(r/'round37-logo-fixes.json'));rows=json.load(open(r/'general-round37-input.json'));index={x['id']:i for i,x in enumerate(rows)}
f=r/'round37-logo-seven-fixes.json'
if f.exists():
 for k,v in json.load(open(f)).items():a[k]=v
# Exact official image exposed in the committee's own homepage.
a[rows[81]['id']]={'logo_url':'https://static.wixstatic.com/media/8976b2_bee04a740c974ff28163e1d642a11d1a~mv2.jpg','logo_source_url':'https://www.csustl.us/'}
dest=r/'round37-image-audit';canvas=Image.new('RGB',(1200,650),'#d6d6d6');d=ImageDraw.Draw(canvas);ok=[]
for j,(k,v) in enumerate(a.items()):
 u=v.get('logo_url',v.get('url',''))
 if not u:continue
 try:
  f,m,b=get(u);impath=dest/f'fix{index[k]}.png'
  if 'svg' in m:
   svg=dest/f'fix{index[k]}.svg';svg.write_bytes(b);subprocess.run(['node','-e',"require('./lobbying-map/node_modules/sharp')(process.argv[1]).resize(180,130,{fit:'inside'}).png().toFile(process.argv[2])",str(svg),str(impath)],check=True,capture_output=True);b=impath.read_bytes()
  im=Image.open(io.BytesIO(b)).convert('RGBA');im.thumbnail((180,130));x=(j%6)*200;y=(j//6)*180;canvas.paste(im,(x,y+25),im);d.text((x,y),str(index[k]),fill='black')
  cp=r/f'website-cache/{k}.json';c=json.load(open(cp));c.update(logo_url=u,logo_kind='logo',logo_source_url=v.get('logo_source_url',v.get('source_url')),logo_http_status=200,logo_content_type=m);cp.write_text(json.dumps(c,indent=2)+'\n');ok.append(index[k])
 except Exception as e:print(index[k],str(e))
canvas.save(dest/'fixes.png');print('Fetched',ok)
