import pathlib,json,urllib.request,time,sqlite3
root=pathlib.Path(__file__).resolve().parent
p=root/'year-counts.json';out=json.loads(p.read_text()) if p.exists() else {}
for y in range(1999,2027):
 if str(y) in out:continue
 for attempt in range(5):
  try:
   d=json.load(urllib.request.urlopen(f'https://lda.gov/api/v1/filings/?format=json&page_size=1&filing_year={y}',timeout=40));out[str(y)]=d['count'];p.write_text(json.dumps(out,indent=2));print(y,d['count'],flush=True);break
  except Exception as e:print(e,flush=True);time.sleep(30)
 time.sleep(6)
print('DONE',flush=True)
