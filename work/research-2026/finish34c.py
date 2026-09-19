import pathlib,json,io
from PIL import Image,ImageDraw
r=pathlib.Path('work/research-2026');rows=json.load(open(r/'general-round34-c-input.json'));exec((r/'check_general34a.py').read_text().split('p=json.load(open(root/')[0]);changes={2:'https://www.amarillo.gov/wp-content/uploads/2024/12/cropped-Web-Favicon-180x180.png',15:'https://cmsv2-assets.apptegy.net/uploads/20003/logo/22603/bainbridge_logo.png',16:'https://www.baltimorecity.gov/apple-touch-icon.png',39:'https://www.brownsvilletx.gov/ImageRepository/Document?documentID=13931',73:'https://www.cocoafl.gov/ImageRepository/Document?documentID=15896',74:'https://www.cocoafl.gov/ImageRepository/Document?documentID=15896',99:'https://www.durhamnc.gov/ImageRepository/Document?documentID=65744'}
canvas=Image.new('RGB',(1400,160),'#c6c6c6');d=ImageDraw.Draw(canvas)
for n,(i,u) in enumerate(changes.items()):
 try:
  dest,mime,b=get(u);assert mime.startswith('image/') and len(b)>80;im=Image.open(io.BytesIO(b)).convert('RGBA');im.thumbnail((190,120));canvas.paste(im,(n*200,25),im);d.text((n*200+5,5),str(i),fill='black');f=r/f"website-cache/{rows[i]['id']}.json";c=json.load(open(f));c.update(logo_url=u,logo_kind='site_icon' if i in [2,16] else 'logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime);f.write_text(json.dumps(c,indent=2)+'\n');print(i,mime)
 except Exception as ex:print(i,str(ex))
canvas.save(r/'round34c-image-audit/replacements.png')
