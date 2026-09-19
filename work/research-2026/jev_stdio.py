"""Run the installed Jev MCP server freshly; preserve the user's provider config."""
import argparse, json, select, subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('batch')
parser.add_argument('--output', default='classifier-results.json')
parser.add_argument('--limit', type=int, default=50)
parser.add_argument('--start-index', type=int, default=0)
args = parser.parse_args()
folder = Path(__file__).resolve().parent / args.batch
output = folder / args.output
assert not output.exists(), 'Do not overwrite a previous classification run'
rows = json.loads((folder / 'fetch-results.json').read_text())
items = [{'id': str(i) + '-' + x['id'], 'path': x['path']}
         for i, x in enumerate(rows) if i >= args.start_index and x.get('path') and x.get('text_chars', 0) > 300][:args.limit]
server = Path.home() / '.codex/plugins/cache/personal/jev-sift/0.2.0+codex.20260918200547/dist/server.mjs'
process = subprocess.Popen(['node', str(server)], stdin=subprocess.PIPE,
    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)

def request(number, method, params):
    process.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': number, 'method': method, 'params': params}) + '\n')
    process.stdin.flush()
    while True:
        if not select.select([process.stdout], [], [], 180)[0]:
            raise TimeoutError(method)
        line = process.stdout.readline()
        if not line:
            raise RuntimeError('Jev process ended before returning the request')
        response = json.loads(line)
        if response.get('id') == number:
            if 'error' in response:
                raise RuntimeError(response['error'])
            return response['result']

try:
    request(1, 'initialize', {'protocolVersion': '2024-11-05', 'capabilities': {},
        'clientInfo': {'name': 'research-evidence', 'version': '1'}})
    process.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n')
    process.stdin.flush()
    results = []
    for offset in range(0, len(items), 5):
        result = request(offset + 2, 'tools/call', {'name': 'classify', 'arguments': {
            'items': items[offset:offset + 5], 'questions': {
                'identity': {'type': 'boolean', 'instructions': 'Does actual source body explicitly identify the exact Target filing entity, including legal suffix or explicit former-name relationship? Ignore Target filing header. A parent brand alone or different legal entity is insufficient.'},
                'ownership': {'type': 'boolean', 'instructions': 'Does actual body explicitly establish ownership/status for this exact target (public/private/family/employee owned, named parent, nonprofit or government)? Do not infer from legal suffix or related entities.'}
            }}})
        results.append(result)
        output.write_text(json.dumps(results, indent=2) + '\n')
        data = result.get('structuredContent', {})
        entries = data.get('results', [])
        errors = sum(bool(x.get('error')) for x in entries)
        print(json.dumps({'screened': len(entries), 'errors': errors, 'usage': data.get('usage')}), flush=True)
        if result.get('isError') or (entries and errors == len(entries)):
            raise RuntimeError('Jev batch failed; inspect saved response before retrying')
finally:
    process.terminate()
    process.wait(timeout=5)
