from pathlib import Path
exec(Path('work/research-2026/check_websites.py').read_text().split("profiles=json.load(open('lobbying-map/research/profiles.json'))")[0])
print(str(one(('dace0d3b40c66cba',{'name':'Southeast Alaska Regional Health Consortium','website':'https://searhc.org/'})))[:200])
