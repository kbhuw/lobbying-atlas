import {existsSync, readFileSync, writeFileSync} from 'node:fs';
import {gunzipSync, gzipSync} from 'node:zlib';

// Researchers may edit the ignored JSON mirror. Clean checkouts use the
// compressed source, keeping the complete evidence ledger below upload limits.
export function readReviewedProfiles({sync = false} = {}) {
  const plain = 'research/reviewed-2026.json';
  const compressed = `${plain}.gz`;
  const bytes = existsSync(plain)
    ? readFileSync(plain)
    : gunzipSync(readFileSync(compressed));
  const profiles = JSON.parse(bytes);
  if (sync) writeFileSync(compressed, gzipSync(bytes, {level: 9}));
  return profiles;
}
