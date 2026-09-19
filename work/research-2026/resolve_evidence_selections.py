"""Resolve selected span IDs against unchanged source text. Output is review-only."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
for name in ('input', 'index', 'selections', 'output'):
    parser.add_argument(name, type=Path)
args = parser.parse_args()
inputs = json.loads(args.input.read_text())
index = json.loads(args.index.read_text())
selections = json.loads(args.selections.read_text())
by_id = {row['id']: row for row in inputs}
assert len(by_id) == len(inputs)
assert len(index) == len(by_id) and {row['id'] for row in index} == set(by_id)
assert len(selections) == len(by_id) and {row['id'] for row in selections} == set(by_id)
spans = {}
for row in index:
    source = by_id[row['id']]
    text = source.get('website_text') or ''
    assert hashlib.sha256(text.encode()).hexdigest() == row['source_sha256'], 'Source changed'
    assert row['source_url'] == source.get('final_url'), 'URL changed'
    for candidate in row['candidates']:
        assert candidate['text'] == text[candidate['start']:candidate['end']], 'Span changed'
        assert candidate['candidate_id'] not in spans, 'Duplicate candidate ID'
        spans[candidate['candidate_id']] = (row, candidate)
out = []
for selection in selections:
    selected = selection['candidate_ids']
    assert len(selected) == len(set(selected)), 'Duplicate selection'
    for candidate_id in selected:
        row, candidate = spans[candidate_id]
        assert row['id'] == selection['id'], 'Cross-organization selection'
        out.append({'id': row['id'], 'source_url': row['source_url'], 'quote': candidate['text'],
                    'status': 'verbatim_only_needs_identity_and_claim_review'})
args.output.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'entries': len(selections), 'verbatim_review_passages': len(out)}))
