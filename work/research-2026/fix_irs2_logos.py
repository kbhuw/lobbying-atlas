from pathlib import Path
exec(Path('work/research-2026/check_websites.py').read_text().split("profiles=json.load(open('lobbying-map/research/profiles.json'))")[0])
u='https://fortbendregionalpartnership.com/';final,mime,data=get(u)
class Images(HTMLParser):
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='img' and 'logo' in str(a).lower():print(a)
Images().feed(data.decode(errors='replace'))
