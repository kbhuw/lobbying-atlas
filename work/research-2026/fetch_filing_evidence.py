"""Fetch a bounded, resumable set of LDA filing details without overrunning limits."""
import argparse
import datetime
import json
import pathlib
import time
import urllib.error
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('jobs', help='JSON list containing filing UUIDs in the filing field')
parser.add_argument('--cache', required=True)
parser.add_argument('--limit', type=int, default=20)
args = parser.parse_args()
cache = pathlib.Path(args.cache)
cache.mkdir(parents=True, exist_ok=True)
jobs = json.loads(pathlib.Path(args.jobs).read_text())
state_path = cache / 'fetch-state.json'
now = time.time()
state = json.loads(state_path.read_text()) if state_path.exists() else {}
if state.get('retry_at_epoch', 0) > now:
    print(json.dumps({'status': 'cooldown', 'retry_at_epoch': state['retry_at_epoch']}))
    raise SystemExit(0)
fetched = 0
seen = set()
for job in jobs:
    filing = job['filing']
    if filing in seen:
        continue
    seen.add(filing)
    path = cache / (filing + '.json')
    if path.exists():
        saved = json.loads(path.read_text())
        if saved.get('client') and saved.get('filing_uuid') == filing:
            continue
    if fetched >= args.limit:
        break
    try:
        request = urllib.request.Request(
            f'https://lda.gov/api/v1/filings/{filing}/?format=json',
            headers={'Accept': 'application/json'},
        )
        with urllib.request.urlopen(request, timeout=25) as response:
            raw = response.read()
        data = json.loads(raw)
        if data.get('filing_uuid') != filing or not data.get('client'):
            raise ValueError('Response does not identify requested filing and client')
        temporary = path.with_suffix('.tmp')
        temporary.write_bytes(raw)
        temporary.replace(path)
        fetched += 1
        time.sleep(1.1)
    except urllib.error.HTTPError as error:
        retry = error.headers.get('Retry-After', '')
        delay = int(retry) if retry.isdigit() else 60
        state = {'status': 'paused', 'http_status': error.code,
                 'filing': filing, 'retry_at_epoch': time.time() + delay,
                 'fetched_this_run': fetched}
        state_path.write_text(json.dumps(state, indent=2) + '\n')
        print(json.dumps(state))
        raise SystemExit(0)
state_path.write_text(json.dumps({'status': 'batch_finished', 'fetched_this_run': fetched,
    'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}, indent=2) + '\n')
print(json.dumps({'status': 'batch_finished', 'fetched_this_run': fetched}))
