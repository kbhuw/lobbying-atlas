"""Validate exact quoted text and provenance; never infer entity identity."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('inputs', type=Path)
parser.add_argument('results', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
inputs = json.loads(args.inputs.read_text())
results = json.loads(args.results.read_text())
by_id = {row['id']: row for row in inputs}
result_ids = [row['id'] for row in results]
assert len(by_id) == len(inputs), 'Duplicate input IDs'
assert len(result_ids) == len(set(result_ids)), 'Duplicate result IDs'
assert set(result_ids) == set(by_id), 'Missing or unexpected result IDs'
accepted, rejected = [], []
for row in results:
    source = by_id[row['id']]
    for passage in row['passages']:
        reasons = []
        quote = passage.get('quote')
        if not isinstance(quote, str) or not quote.strip() or quote not in source.get('website_text', ''):
            reasons.append('Quote is not an exact nonempty substring of supplied text')
        if not source.get('final_url') or passage.get('source_url') != source['final_url']:
            reasons.append('Source URL differs from supplied page URL')
        if passage.get('topic') not in {'identity', 'activity', 'ownership'}:
            reasons.append('Unsupported topic')
        item = {'id': row['id'], **passage}
        if reasons:
            rejected.append({**item, 'reasons': reasons})
        else:
            accepted.append({**item, 'status': 'verbatim_only_needs_identity_and_claim_review'})
report = {'scope': 'Exact quotation and URL checks only. Not verification of entity identity, ownership, or truth.',
          'entries': len(results), 'accepted': accepted, 'rejected': rejected}
args.output.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'entries': len(results), 'accepted_passages': len(accepted), 'rejected_passages': len(rejected)}))
