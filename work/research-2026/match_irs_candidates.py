"""Collect exact-name IRS candidates. Candidates are not reviewed entity matches."""
import csv, json, pathlib, re, sys
root = pathlib.Path('work/research-2026')
batch = int(sys.argv[1])
rows = json.loads((root / f'general-round{batch}-input.json').read_text())
normalize = lambda name: re.sub(r'[^A-Z0-9]', '', name.upper())
index = {}
for i, row in enumerate(rows):
    names = [row['name']] + [a for a in row.get('aliases', []) if isinstance(a, str)]
    for name in names:
        key = normalize(name)
        for variant in {key, key + 'INC', key[:-3] if key.endswith('INC') else key}:
            if variant:
                index.setdefault(variant, set()).add(i)
candidates = {}
for source in sorted(pathlib.Path('work/organization-research/irs').glob('eo*.csv')):
    with source.open(newline='') as handle:
        for record in csv.DictReader(handle):
            for i in index.get(normalize(record.get('NAME', '')), ()):
                item = {k: record.get(k, '') for k in ['EIN', 'NAME', 'STREET', 'CITY', 'STATE', 'ZIP', 'SUBSECTION', 'STATUS']}
                item['source_url'] = 'https://www.irs.gov/pub/irs-soi/' + source.name
                candidates.setdefault(str(i), []).append(item)
dest = root / f'round{batch}-irs-candidates.json'
dest.write_text(json.dumps(candidates, indent=2) + '\n')
print(f'{len(candidates)} of {len(rows)} entries have IRS name candidates; review exact entity and chapter before use.')
