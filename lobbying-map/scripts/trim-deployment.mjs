import { existsSync, rmSync } from 'node:fs';

// Historical indexes remain in public/data for research and validation.
// The application loads directory-v3; deploy that index and every report shard.
if (!existsSync('dist/client/data/directory-v3.json.gz')) throw new Error('Current directory build missing');
for (const name of ['index.json.gz', 'directory-v2.json.gz']) {
  rmSync(`dist/client/data/${name}`, { force: true });
}
console.log('Deployment keeps the current directory and all report shards.');
