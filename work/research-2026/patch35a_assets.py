import json,pathlib,concurrent.futures
r=pathlib.Path('work/research-2026');exec((r/'check_general34a.py').read_text().split('p=json.load(open(root/')[0]);rows=json.load(open(r/'general-round35-a-input.json'))
urls={11:'https://www.fairmontwv.gov/ImageRepository/Document?documentID=2831',55:'https://www.hialeahfl.gov/ImageRepository/Document?documentId=17461',61:'https://www.cityofhomer-ak.gov/sites/all/themes/aha_compass/images/footer/footer-logo.png',66:'https://www.houstontx.gov/_siteAssets/images/citySeal125x125.png',68:'https://www.idahofallsidaho.gov/ImageRepository/Document?documentID=14220',108:'https://cityoflosalamitos.org/ImageRepository/Document?documentID=66',126:'https://ci.millbrae.ca.us/ImageRepository/Document?documentID=70',133:'https://storage.googleapis.com/proudcity/montclairca/uploads/2021/01/City-Seal-300x300.png',142:'https://www.nomealaska.org/ImageRepository/Document?documentID=235',155:'https://opalockafl.gov/ImageRepository/Document?documentID=4298'}
def f(iv):
 i,u=iv;path=r/f"website-cache/{rows[i]['id']}.json";c=json.load(open(path))
 try:
  final,mime,b=get(u,1000000);assert mime.startswith('image/');c.update(logo_url=u,logo_http_status=200,logo_kind='logo',logo_source_url='https://www.houstontx.gov/abouthouston/cityseal.html' if i==66 else c['final_url']);path.write_text(json.dumps(c,indent=2)+'\n');return i,'ok'
 except Exception as ex:return i,str(ex)
for z in concurrent.futures.ThreadPoolExecutor(max_workers=6).map(f,urls.items()):print(z)
