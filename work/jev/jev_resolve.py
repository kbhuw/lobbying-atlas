"""Run jev_find over entity-jobs.json to map unmatched client names to groups.

Usage: python3 jev_resolve.py <entity-jobs.json> <out.json> [workers]
Resumable: out.json accumulates {norm_name: {group_id, name, prob, verdict}}.
"""
import json, os, queue, select, subprocess, sys, threading

JEV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'node_modules/@jkudish/jev-mcp/dist/index.js')


class W(threading.Thread):
    def __init__(self, jobs, results):
        super().__init__(daemon=True)
        self.jobs, self.results, self.seq = jobs, results, 0
        self.p = subprocess.Popen(['node', JEV], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                  text=True, bufsize=1)
        self.req('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {},
                                'clientInfo': {'name': 'lobbying-atlas', 'version': '1'}})
        self.p.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n')
        self.p.stdin.flush()

    def req(self, method, params):
        self.seq += 1
        self.p.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': self.seq, 'method': method,
                                       'params': params}) + '\n')
        self.p.stdin.flush()
        while True:
            if not select.select([self.p.stdout], [], [], 180)[0]:
                raise TimeoutError(method)
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError('ended')
            r = json.loads(line)
            if r.get('id') == self.seq:
                if 'error' in r:
                    raise RuntimeError(r['error'])
                return r['result']

    def run(self):
        while True:
            try:
                job = self.jobs.get(timeout=3)
            except queue.Empty:
                break
            if job is None:
                break
            try:
                res = self.req('tools/call', {'name': 'jev_find', 'arguments': {
                    'query': f"A federal lobbying filing lists the client organization as \"{job['name']}\". Which candidate is the same legal entity (allow for name variants, abbreviations, former names, d/b/a, Inc./LLC suffixes; reject same-name different entities)?",
                    'candidates': job['candidates'], 'top_k': 1}})
                data = json.loads(res['content'][0]['text'])
                top = (data.get('top') or [{}])[0]
                self.results.append({'name': job['name'], 'verdict': data.get('exists_verdict'),
                                  'exists': data.get('exists'),
                                  'group_id': top.get('id'), 'text': top.get('text'),
                                  'prob': top.get('probability')})
            except Exception as e:
                self.results.append({'name': job['name'], 'error': repr(e)})
        self.p.terminate()


def main():
    jobs_path, out_path = sys.argv[1], sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    jobs = json.load(open(jobs_path))
    done = set()
    if os.path.exists(out_path):
        done = {x['name'] for x in json.load(open(out_path))}
    jobs = [j for j in jobs if j['name'] not in done]
    print(f'todo {len(jobs)}')

    q, res = queue.Queue(), []
    for j in jobs:
        q.put(j)
    for _ in range(workers):
        q.put(None)
    ws = [W(q, res) for _ in range(workers)]
    for w in ws:
        w.start()
    for w in ws:
        w.join()
        if len(res) % 200 == 0:
            print(len(res), flush=True)
    prev = json.load(open(out_path)) if os.path.exists(out_path) else []
    json.dump(prev + res, open(out_path, 'w'), indent=1)
    print('DONE', len(res))


if __name__ == '__main__':
    main()
