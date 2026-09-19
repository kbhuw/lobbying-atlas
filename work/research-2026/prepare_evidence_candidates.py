"""Build a small, verbatim source index for Spark to select, never rewrite."""
import argparse
import hashlib
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('input', type=Path, help='Array containing id, final_url and website_text')
parser.add_argument('output', type=Path)
args = parser.parse_args()
rows = json.loads(args.input.read_text())
assert len({row['id'] for row in rows}) == len(rows), 'Duplicate IDs'
keywords = re.compile(r'\b(privately held|publicly traded|employee.owned|family.owned|wholly.owned|subsidiar\w*|nonprofit|non.profit|501\s*\(|headquartered|registered office|manufactur\w*|develop\w*|provid\w*|operat\w*)', re.I)
out = []
for row in rows:
    text = row.get('website_text') or ''
    spans = []
    if text and row.get('final_url'):
        ranges = [(max(0, match.start()-100), min(len(text), match.end()+260)) for match in keywords.finditer(text)]
        ranges.insert(0, (0, min(360, len(text))))
        for start, end in ranges:
            if any(abs(start - old['start']) < 150 for old in spans):
                continue
            quote = text[start:end]
            spans.append({'candidate_id': f"{row['id']}:{start}:{end}", 'start': start, 'end': end, 'text': quote})
            if len(spans) >= 12:
                break
    out.append({'id': row['id'], 'filed_name': row.get('filed_name'), 'source_url': row.get('final_url'),
                'source_sha256': hashlib.sha256(text.encode()).hexdigest(), 'candidates': spans})
args.output.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'entries': len(out), 'candidate_spans': sum(len(row['candidates']) for row in out),
                  'characters': sum(len(c['text']) for row in out for c in row['candidates'])}))
