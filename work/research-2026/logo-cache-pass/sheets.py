import json,pathlib,subprocess,sys
p=pathlib.Path('work/research-2026/logo-cache-pass')/sys.argv[1];js=json.loads((p/'candidates.json').read_text())
for start in range(0,len(js),8):
 args=['magick','montage','-font','/System/Library/Fonts/Helvetica.ttc']
 for i in range(start,min(start+8,len(js))):
  j=js[i]
  if j.get('preview_ok'):args+=['-label',str(i)+' '+j['name'],str(p/(j['id']+'.png'))]
 args+=['-pointsize','11','-background','#d6dbe0','-fill','black','-tile','2x','-geometry','380x150+5+5',str(p/f'sheet-{start}.png')];subprocess.run(args,check=True)
