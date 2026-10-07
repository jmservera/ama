import assert from 'node:assert/strict';
import { performance } from 'node:perf_hooks';

const base = 'http://127.0.0.1:3410';
async function read(path) {
  const response = await fetch(`${base}${path}`, {
    headers: { 'x-demo-role': 'viewer' },
    signal: AbortSignal.timeout(5000),
  });
  assert.equal(response.status, 200, `${path}: HTTP ${response.status}`);
  return response.json();
}

const health = await read('/health');
const config = await read('/api/config');
const all = await read('/api/cases');
assert.ok(all.cases.length >= 9, 'At least nine constructed scenarios');
assert.equal(config.workflows.length, 9, 'Nine configured workflow views');
const cohorts = [];
for (const workflow of config.workflows) {
  const result = await read(`/api/cases?workflow=${encodeURIComponent(workflow.id)}`);
  assert.ok(result.cases.length > 0, `${workflow.id}: executable fixture required`);
  assert.ok(result.cases.every(item => item.workflow === workflow.id), workflow.id);
  cohorts.push({ workflow: workflow.id, cases: result.cases.length });
}
const filtered = await read('/api/cases?q=EX-HOME-900');
assert.equal(filtered.cases.length, 1);
assert.equal(filtered.cases[0].id, 'EX-HOME-900');
const held = await read('/api/cases/EX-HOME-531');
assert.ok(held.blockers.length > 0, 'Held home exposes its owned blockers');
await read('/api/portfolio');
await read('/api/export');
await read('/metrics');

const latencies = [];
for (let index = 0; index < 100; index += 1) {
  const start = performance.now();
  const result = await read('/api/cases');
  assert.equal(result.cases.length, all.cases.length);
  latencies.push(performance.now() - start);
}
latencies.sort((a, b) => a - b);
const p95 = latencies[Math.ceil(latencies.length * 0.95) - 1];
assert.ok(p95 <= 250, `Local case-list p95 ${p95.toFixed(2)}ms exceeds 250ms`);
console.log(JSON.stringify({
  execution: 'local-container-read-only-smoke',
  synthetic: true,
  cases: all.cases.length,
  cohorts,
  health,
  latency: {
    requests: latencies.length,
    sequential: true,
    p50Ms: Number(latencies[49].toFixed(2)),
    p95Ms: Number(p95.toFixed(2)),
    targetP95Ms: 250,
  },
  limitations: 'Not production load, customer benefits or operational approval evidence.',
}, null, 2));
