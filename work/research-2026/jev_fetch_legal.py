import gzip
"""Fetch linked legal/about pages for unresolved identities; never auto-promote."""
import argparse, collections, concurrent.futures, json, subprocess, urllib.request, urllib.parse
from html.parser import HTMLParser
from pathlib import Path
from jev_clean_html import TextParser
from decode_source import decode_html

parser = argparse.ArgumentParser()
parser.add_argument('--batch', required=True)
parser.add_argument('--limit', type=int, default=50)
args = parser.parse_args()
root = Path(__file__).resolve().parent
out = root / args.batch
assert out.parent == root and not out.exists()
profiles = json.loads((root / 'reviewed.json').read_text())
seen = set()
history = []
def canonical(url):
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip('/'), parts.query, ''))

for f in sorted(root.glob('jev-batch-*/fetch-results.json')):
    for row in json.loads(f.read_text()):
        seen.add((row['id'], canonical(row['requested_url'])))
        if row.get('final_url'):
            seen.add((row['id'], canonical(row['final_url'])))
        history.append((f.parent, row))

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href') or ''
            if any(x in href.lower() for x in ('privacy', 'terms', 'legal', 'about')):
                self.urls.append(href)

jobs = []
for folder, row in history:
    key = row['id']
    source = folder / (key + '.html')
    if profiles[key]['review_outcome'] == 'confirmed' or not source.exists():
        continue
    base = row.get('final_url', row['requested_url'])
    links = Links(); links.feed(source.read_text())
    candidates = sorted(set(links.urls), key=lambda u: (not any(x in u.lower() for x in ('privacy', 'terms', 'legal')), len(urllib.parse.urlparse(u).path.split('/')), len(u), u))
    count = 0
    for href in candidates:
        url = urllib.parse.urljoin(base, href).split('#')[0]
        parts = urllib.parse.urlparse(url)
        # A news archive nested under /about/ is not an identity/legal page.
        if any((segment in ('news', 'blog', 'press', 'articles', 'events', 'publications') or segment.endswith('-blog')) for segment in parts.path.lower().split('/')):
            continue
        if parts.scheme not in ('https', 'http') or parts.netloc != urllib.parse.urlparse(base).netloc or (key, canonical(url)) in seen:
            continue
        seen.add((key, canonical(url))); jobs.append((key, url)); count += 1
        if count == 2: break
# Prioritize less-investigated entities rather than repeatedly consuming the batch
# with deep subpages from the earliest historical records.
attempt_counts = collections.Counter(row["id"] for _, row in history)
jobs.sort(key=lambda job: attempt_counts[job[0]])
jobs = jobs[:args.limit]
out.mkdir()

def fetch(job):
    index, (key, url) = job
    result = {'id': key, 'name': profiles[key]['name'], 'requested_url': url}
    try:
        response = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=20)
        raw = response.read(3000000)
        if raw.startswith(b"\x1f\x8b"): raw = gzip.decompress(raw)
        stem = str(index) + '-' + key
        if raw.startswith(b'%PDF-'):
            source = out / (stem + '.pdf'); source.write_bytes(raw)
            info = subprocess.run(['pdfinfo', str(source)], check=True, capture_output=True, text=True, timeout=20)
            (out / (stem + '.pdfinfo.txt')).write_text(info.stdout)
            extracted = subprocess.run(['pdftotext', '-layout', str(source), '-'], check=True, capture_output=True, text=True, timeout=20).stdout
            result['source_format'] = 'pdf'
        else:
            body = decode_html(raw, response.headers)
            (out / (stem + '.html')).write_text(body)
            parser = TextParser(); parser.feed(body)
            extracted = '\n'.join(parser.parts)
        text = 'Target filing name: ' + profiles[key]['name'] + '\nSource URL: ' + response.url + '\n\n' + extracted
        path = out / (stem + '.txt'); path.write_text(text)
        result.update(status=response.status, final_url=response.url, path=str(path), text_chars=len(text))
    except Exception as error:
        result['error'] = str(error)
    return result

results = list(concurrent.futures.ThreadPoolExecutor(8).map(fetch, enumerate(jobs)))
(out / 'fetch-results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps({'attempted': len(results), 'readable': sum(x.get('text_chars', 0) > 300 for x in results), 'errors': sum('error' in x for x in results)}))
