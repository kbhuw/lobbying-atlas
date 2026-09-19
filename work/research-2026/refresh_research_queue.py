"""Reconcile current profiles with saved retrievals and explicit follow-up notes.

This produces a work queue only; it never promotes identities or ownership.
"""
import collections
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parent
profiles = json.loads((root / 'reviewed.json').read_text())
attempts = collections.defaultdict(list)
followups = collections.defaultdict(list)
for path in sorted(root.glob('jev-batch-*/fetch-results.json')):
    for row in json.loads(path.read_text()):
        attempts[row['id']].append(dict(row, batch=path.parent.name))
for path in sorted(root.glob('jev-batch-*/pending.json')):
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        for key, value in data.items():
            if key in profiles:
                followups[key].append({'source': str(path), 'note': value})
for path in sorted(root.glob('jev-batch-*/source-quality-issues.json')):
    for row in json.loads(path.read_text()):
        followups[row['id']].append({'source': str(path), 'note': row['issue']})
queue = []
for key, profile in profiles.items():
    if profile.get('review_outcome') == 'confirmed':
        continue
    history = attempts[key]
    readable = [x for x in history if x.get('text_chars', 0) > 300 and not x.get('error')]
    task = ('resolve_specific_evidence_gap' if followups[key] else
            'review_saved_page' if readable else
            'alternate_source_needed' if history else 'source_research_needed')
    queue.append({'id': key, 'name': profile['name'],
                  'review_outcome': profile.get('review_outcome'),
                  'website': profile.get('website', ''),
                  'next_action': task, 'followups': followups[key],
                  'saved_pages': [x['path'] for x in readable],
                  'retrieval_attempts': len(history),
                  'logo_candidates': [a for x in readable for a in x.get('logo_candidates', [])]})
destination = root / 'jev-queue'
destination.mkdir(exist_ok=True)
(destination / 'current-work-queue.json').write_text(json.dumps(queue, indent=2, ensure_ascii=False) + '\n')
fields = ['id', 'name', 'review_outcome', 'website', 'next_action', 'retrieval_attempts']
with (destination / 'current-work-queue.csv').open('w', newline='') as output:
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(queue)
assert len(queue) == sum(p.get('review_outcome') != 'confirmed' for p in profiles.values())
print(json.dumps({'incomplete': len(queue), 'next_actions': dict(collections.Counter(x['next_action'] for x in queue))}))

# Track remaining fields even when identity work is already confirmed.
field_queue = []
for key, profile in profiles.items():
    gaps = []
    if profile.get('review_outcome') != 'confirmed': gaps.append('identity')
    if not profile.get('website') or profile.get('website_status') != 'verified': gaps.append('website')
    if not profile.get('logo_url') or profile.get('logo_kind') != 'logo' or profile.get('logo_status') != 'official_site_asset': gaps.append('official_full_logo')
    if profile.get('ownership', 'Unknown').strip().lower() in ('unknown', '', 'unverified'): gaps.append('ownership')
    if gaps: field_queue.append({'id': key, 'name': profile['name'], 'missing_fields': gaps})
field_counts = dict(collections.Counter(gap for row in field_queue for gap in row['missing_fields']))
(destination / 'field-completeness-queue.json').write_text(json.dumps({
    'scope': '2026 filing-name profiles, not deduplicated organizations',
    'total': len(profiles), 'profiles_with_any_gap': len(field_queue),
    'missing_counts': field_counts,
    'definition': 'Field presence/status audit only; does not revalidate populated fields.',
    'items': field_queue}, ensure_ascii=False, indent=2) + '\n')
