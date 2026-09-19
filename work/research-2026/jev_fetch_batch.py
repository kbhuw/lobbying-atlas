import gzip
"""Fetch a bounded official-site candidate batch, preserving failures and logo candidates."""
import json,concurrent.futures,urllib.request,urllib.parse,argparse,collections,subprocess
from pathlib import Path
from jev_clean_html import TextParser
from decode_source import decode_html
parser=argparse.ArgumentParser();parser.add_argument('--batch',required=True);parser.add_argument('--limit',type=int,default=50);parser.add_argument('--all-unfetched',action='store_true');args=parser.parse_args()
root=Path('work/research-2026');out=root/args.batch
assert out.parent==root and not out.exists(), 'Use a fresh batch directory'
seen=set()
for f in root.glob('jev-batch-*/fetch-results.json'):
 for row in json.loads(f.read_text()):seen.add((row['id'],row['requested_url']))
out.mkdir()
p=json.load(open(root/'reviewed.json'));a=[]
if args.all_unfetched:
 for k,v in p.items():
  if v.get('review_outcome')!='confirmed' and v.get('website') and (k,v['website']) not in seen:a.append({'id':k})
else:
 for b in json.load(open(root/'jev-queue/routing.json')):
  for x in b['result']['results']:
   if x['answers']['route']['choice']=='evidence_review' and p[x['id']]['review_outcome']!='confirmed' and p[x['id']].get('website') and (x['id'],p[x['id']]['website']) not in seen:a.append(x)
 a.sort(key=lambda x:-x['answers']['route'].get('confidence',0))
a=a[:args.limit]
class Assets(TextParser):
 def __init__(self):super().__init__();self.assets=[]
 def handle_starttag(self,t,a):
  super().handle_starttag(t,a);d=dict(a)
  if t=='img' and (any('logo' in str(d.get(k,'')).lower() for k in ('src','alt','class')) or 'bannerobject' in d.get('class','').lower() or 'homepage' in d.get('alt','').lower()):self.assets.append(d)
def fetch(x):
 k=x['id'];v=p[k];result={'id':k,'name':v['name'],'requested_url':v['website']}
 try:
  res=urllib.request.urlopen(urllib.request.Request(v['website'],headers={'User-Agent':'Mozilla/5.0'}),timeout=20)
  raw=res.read();assets=[]
  if raw.startswith(b"\x1f\x8b"): raw=gzip.decompress(raw)
  if raw.startswith(b'%PDF-'):
   source=out/(k+'.pdf');source.write_bytes(raw)
   info=subprocess.run(['pdfinfo',str(source)],check=True,capture_output=True,text=True,timeout=20)
   (out/(k+'.pdfinfo.txt')).write_text(info.stdout)
   extracted=subprocess.run(['pdftotext','-layout',str(source),'-'],check=True,capture_output=True,text=True,timeout=20).stdout
   result['source_format']='pdf'
  else:
   body=decode_html(raw, res.headers);(out/(k+'.html')).write_text(body);t=Assets();t.feed(body);extracted='\n'.join(t.parts);assets=t.assets
  text='Target filing name: '+v['name']+'\nSource URL: '+res.url+'\n\n'+extracted
  (out/(k+'.txt')).write_text(text)
  result.update(status=res.status,final_url=res.url,text_chars=len(text),logo_candidates=assets,path=str((out/(k+'.txt')).resolve()))
 except Exception as e:result['error']=str(e)
 return result
results=list(concurrent.futures.ThreadPoolExecutor(8).map(fetch,a));(out/'fetch-results.json').write_text(json.dumps(results,indent=2));print(json.dumps({'attempted':len(results),'readable':sum(x.get('text_chars',0)>300 for x in results),'errors':sum('error' in x for x in results),'file':str(out/'fetch-results.json')}))
