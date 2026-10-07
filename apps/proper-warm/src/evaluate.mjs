import { randomUUID } from 'node:crypto';
import { mkdirSync, rmSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createStore } from './store.mjs';
import { evaluateSimulator } from './evaluation.mjs';

const directory = resolve(dirname(fileURLToPath(import.meta.url)), '..', '.test-data');
mkdirSync(directory, { recursive: true });
const dbPath = resolve(directory, `evaluation-${process.pid}-${randomUUID()}.db`);
let store;
try {
  store = createStore({ dbPath });
  console.log(JSON.stringify(evaluateSimulator(store), null, 2));
} catch (error) {
  console.error(JSON.stringify({ mode: 'simulator', passed: false, error: error.message }));
  process.exitCode = 1;
} finally {
  store?.close();
  for (const suffix of ['', '-wal', '-shm', '-journal']) rmSync(dbPath + suffix, { force: true });
}
