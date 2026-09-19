import { readFileSync } from 'node:fs';
import { gunzipSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

// Validate provenance before applying research. This does not verify the claims.
const [inputPath, ...resultPaths] = process.argv.slice(2);
if (!inputPath || !resultPaths.length) {
  throw new Error('Usage: node validate-research-batch.mjs input.json result.json [...]');
}
const read = path => JSON.parse(readFileSync(path, 'utf8'));
const basePath = fileURLToPath(new URL('../research/directory-base.json.gz', import.meta.url));
const base = new Map(JSON.parse(gunzipSync(readFileSync(basePath))).companies.map(c => [c.id, c]));
const input = read(inputPath);
const expected = new Map();
for (const row of input) {
  assert(!expected.has(row.id), `Duplicate input ID: ${row.id}`);
  assert(base.has(row.id), `Unknown source ID: ${row.id}`);
  assert.deepEqual(row.original_aliases, base.get(row.id).aliases, `Input aliases changed: ${row.id}`);
  assert.equal(row.original_name, base.get(row.id).name, `Input name changed: ${row.id}`);
  expected.set(row.id, row);
}
const seen = new Set();
for (const path of resultPaths) {
  for (const row of read(path)) {
    const id = row.id ?? row.originalID;
    assert(expected.has(id), `Unexpected result ID: ${id}`);
    assert(!seen.has(id), `Duplicate result ID: ${id}`);
    assert.deepEqual(row.original_aliases, expected.get(id).original_aliases, `Result aliases changed or missing: ${id}`);
    if (row.original_name !== undefined) assert.equal(row.original_name, expected.get(id).original_name, `Result source name changed: ${id}`);
    seen.add(id);
  }
}
assert.equal(seen.size, expected.size, `Missing results: ${[...expected.keys()].filter(id => !seen.has(id)).join(', ')}`);
console.log(`Provenance passed for ${seen.size} records. Identity and ownership claims still require source review.`);
