"""Minimal JEV MCP stdio client. Usage: python3 jev_stdio.py <requests.json> [out.json]
requests.json: [{"tool": "jev_classify", "arguments": {...}}, ...]
Env: AI_GATEWAY_API_KEY must be set (source ~/.jev/env)."""
import json, subprocess, sys, os, select

server = os.path.join(os.path.dirname(__file__), 'node_modules/@jkudish/jev-mcp/dist/index.js')
reqs = json.loads(open(sys.argv[1]).read())
out = sys.argv[2] if len(sys.argv) > 2 else 'jev-out.json'

p = subprocess.Popen(['node', server], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.DEVNULL, text=True, bufsize=1)
def request(i, method, params):
    p.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': i, 'method': method, 'params': params}) + '\n')
    p.stdin.flush()
    while True:
        if not select.select([p.stdout], [], [], 300)[0]:
            raise TimeoutError(method)
        line = p.stdout.readline()
        if not line: raise RuntimeError('jev server ended')
        r = json.loads(line)
        if r.get('id') == i:
            if 'error' in r: raise RuntimeError(r['error'])
            return r['result']

try:
    request(0, 'initialize', {'protocolVersion': '2024-11-05', 'capabilities': {},
        'clientInfo': {'name': 'lobbying-atlas', 'version': '1'}})
    p.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n')
    p.stdin.flush()
    results = []
    for i, q in enumerate(reqs):
        res = request(i + 1, 'tools/call', {'name': q['tool'], 'arguments': q['arguments']})
        results.append(res)
        open(out, 'w').write(json.dumps(results, indent=2))
        print(f'{i+1}/{len(reqs)} done', flush=True)
finally:
    p.terminate()
