import test from 'node:test';
import assert from 'node:assert/strict';
import { request as httpRequest } from 'node:http';
import { createApplication } from '../src/server.mjs';
import { ownedFile, happyJourney } from './helpers.mjs';

async function appFixture(t, options = {}) {
  const file = ownedFile('http');
  const logs = [];
  const app = createApplication({ dbPath: file.dbPath, host: '127.0.0.1', port: 0, log: row => logs.push(row), ...options });
  const address = await app.listen();
  t.after(async () => { await app.close(); file.cleanup(); });
  return { app, logs, port: address.port };
}
function request(port, path, { method = 'GET', headers = {}, body, chunked = false } = {}) {
  const content = body === undefined ? undefined : typeof body === 'string' ? body : JSON.stringify(body);
  return new Promise((resolve, reject) => {
    const req = httpRequest({
      hostname: '127.0.0.1', port, path, method,
      headers: { ...(content !== undefined ? { 'content-type': 'application/json',
        ...(chunked ? { 'transfer-encoding': 'chunked' } : { 'content-length': Buffer.byteLength(content) }) } : {}), ...headers },
    }, res => {
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        const text = Buffer.concat(chunks).toString('utf8');
        let json;
        try { json = JSON.parse(text); } catch { /* Static responses are deliberately not JSON. */ }
        resolve({ status: res.statusCode, headers: res.headers, text, json });
      });
      res.on('error', reject);
    });
    req.on('error', reject);
    if (chunked && content) {
      for (let i = 0; i < content.length; i += 8192) req.write(content.slice(i, i + 8192));
      req.end();
    } else req.end(content);
  });
}
const automation = role => ({ 'x-demo-role': role, 'x-proper-warm-request': '1' });
const command = (action, expectedVersion, fields = {}, key = crypto.randomUUID()) => ({
  action, expectedVersion, idempotencyKey: key, payload: { reason: 'Synthetic API decision', source: 'EX-SOURCE-HTTP', ...fields },
});

test('application factory exports isolated non-listening server; health probes writable readiness', async t => {
  const { app, port } = await appFixture(t);
  const response = await request(port, '/health');
  assert.equal(response.status, 200);
  assert.equal(response.json.store, 'writable');
  app.store.close();
  const failed = await request(port, '/health');
  assert.equal(failed.status, 503);
  assert.equal(failed.json.store, 'unavailable');
});

test('GET config/list/detail/export/portfolio have precise scopes and safe role simulation', async t => {
  const { port } = await appFixture(t);
  const config = await request(port, '/api/config');
  assert.equal(config.status, 200);
  assert.equal(config.json.workflows.length, 9);
  assert.equal(config.json.commands.length, 22);
  assert.ok(config.json.commands.every(item => item.fields.some(field => field.key === 'reason') && item.fields.some(field => field.key === 'source')));
  const list = await request(port, '/api/cases?workflow=resident_service&q=208');
  assert.deepEqual(Object.keys(list.json).sort(), ['asOf', 'cases', 'scope']);
  assert.equal(list.json.cases.length, 1);
  const detail = await request(port, '/api/cases/EX-HOME-900', { headers: { 'x-demo-role': 'programme_manager' } });
  assert.equal(detail.json.id, 'EX-HOME-900');
  assert.ok(detail.json.allowedActions.includes('advance'));
  const viewer = await request(port, '/api/cases/EX-HOME-900');
  assert.deepEqual(viewer.json.allowedActions, []);
  const report = await request(port, '/api/portfolio?workflow=resident_service&q=208');
  assert.equal(report.json.metrics[0].denominator, 1);
  assert.equal(report.json.metrics[0].numerator, 1);
  assert.deepEqual(report.json.metrics[0].caseIds, ['EX-HOME-208']);
  const exported = await request(port, '/api/export?workflow=resident_service&q=208');
  assert.match(exported.headers['content-disposition'], /attachment/);
  assert.deepEqual(exported.json.cases, list.json.cases);
  assert.equal(exported.json.synthetic, true);
  assert.equal((await request(port, '/api/cases?workflow=typo')).json.error.code, 'INVALID_FILTER');
  assert.equal((await request(port, '/api/portfolio?workflow=typo')).json.error.code, 'INVALID_FILTER');
  assert.equal((await request(port, '/api/cases/EX-NONEXISTENT')).status, 404);
  assert.equal((await request(port, '/api/cases', { headers: { 'x-demo-role': 'admin' } })).status, 403);
});

test('HTTP command commits, role guards, stale conflict, canonical replay and error contract', async t => {
  const { port, logs } = await appFixture(t);
  const path = '/api/cases/EX-HOME-900/commands';
  const body = command('submit_assessment', 1, { evidenceId: 'EX-ASSESS-HTTP' }, 'EX-HTTP-KEY');
  const first = await request(port, path, { method: 'POST', headers: automation('assessor'), body });
  assert.equal(first.status, 200);
  assert.equal(first.json.case.version, 2);
  assert.equal(first.json.replayed, false);
  const replay = await request(port, path, { method: 'POST', headers: automation('assessor'), body });
  assert.equal(replay.status, 200);
  assert.equal(replay.json.replayed, true);
  const stale = await request(port, path, { method: 'POST', headers: automation('assessor'), body: { ...body, idempotencyKey: 'EX-HTTP-NEW' } });
  assert.equal(stale.status, 409);
  assert.equal(stale.json.error.code, 'VERSION_CONFLICT');
  assert.deepEqual(Object.keys(stale.json).sort(), ['error', 'requestId']);
  assert.deepEqual(Object.keys(stale.json.error).sort(), ['code', 'details', 'message', 'owner']);
  const mismatch = await request(port, path, { method: 'POST', headers: automation('assessor'), body: { ...body, payload: { ...body.payload, reason: 'another intent' } } });
  assert.equal(mismatch.json.error.code, 'IDEMPOTENCY_CONFLICT');
  const forbidden = await request(port, path, { method: 'POST', headers: automation('viewer'), body });
  assert.equal(forbidden.status, 403);
  const blocked = await request(port, path, { method: 'POST', headers: automation('programme_manager'), body: command('advance', 2) });
  assert.equal(blocked.status, 422);
  assert.equal(blocked.json.error.owner, 'coordinator');
  assert.ok(logs.every(row => !('body' in row) && !('payload' in row)));
  assert.ok(logs.some(row => row.status === 422 && row.requestId && row.durationMs >= 0));
  const metrics = await request(port, '/metrics');
  assert.ok(metrics.json.requests >= 6);
  assert.equal(metrics.json.externalCalls, 0);
});

test('Host and Origin checks prevent foreign-origin writes and DNS rebinding reads', async t => {
  const { port } = await appFixture(t);
  const path = '/api/cases/EX-HOME-900/commands';
  const body = command('submit_assessment', 1, { evidenceId: 'EX-A' });
  const send = headers => request(port, path, { method: 'POST', headers, body });
  assert.equal((await request(port, '/api/cases', { headers: { host: `evil.example:${port}` } })).json.error.code, 'INVALID_HOST');
  assert.equal((await request(port, '/', { headers: { 'sec-fetch-site': 'cross-site' } })).status, 200);
  assert.equal((await request(port, '/health', { headers: { host: '127.0.0.1:3410' } })).status, 403);
  assert.equal((await send({ 'x-demo-role': 'assessor' })).json.error.code, 'INVALID_ORIGIN');
  assert.equal((await send({ ...automation('assessor'), origin: 'https://evil.example' })).status, 403);
  assert.equal((await send({ ...automation('assessor'), origin: 'null' })).status, 403);
  assert.equal((await send({ ...automation('assessor'), 'sec-fetch-site': 'cross-site' })).status, 403);
  assert.equal((await send({ origin: `http://127.0.0.1:${port}` })).json.error.code, 'FORBIDDEN');
  assert.equal((await send({ 'x-demo-role': 'assessor', origin: `http://127.0.0.1:${port}`, 'sec-fetch-site': 'same-origin' })).status, 200);
});

test('JSON media/envelope/body bound are enforced for declared and chunked bodies', async t => {
  const { port, app } = await appFixture(t);
  const path = '/api/cases/EX-HOME-900/commands';
  const headers = automation('assessor');
  assert.equal((await request(port, path, { method: 'POST', headers, body: '{' })).status, 400);
  assert.equal((await request(port, path, { method: 'POST', headers: { ...headers, 'content-type': 'text/plain' }, body: '{}' })).status, 400);
  assert.equal((await request(port, path, { method: 'POST', headers: { ...headers, 'content-type': 'application/jsonp' }, body: '{}' })).status, 400);
  for (const chunked of [false, true]) {
    const oversized = await request(port, path, { method: 'POST', headers, body: JSON.stringify({ padding: 'x'.repeat(65536) }), chunked });
    assert.equal(oversized.status, 413);
    assert.equal(oversized.json.error.code, 'BODY_TOO_LARGE');
  }
  const injection = command('submit_assessment', 1, { evidenceId: 'EX-A', owner: 'finance' });
  assert.equal((await request(port, path, { method: 'POST', headers, body: injection })).json.error.code, 'INVALID_PAYLOAD');
  assert.equal(app.store.detail('EX-HOME-900').version, 1);
});

test('only explicit static assets can be served and CSP excludes inline/remote execution', async t => {
  const { port } = await appFixture(t);
  for (const path of ['/package.json', '/manifest.json', '/src/server.mjs', '/data/proper-warm.db', '/public/app.js', '/../package.json', '/%2e%2e/package.json']) {
    assert.equal((await request(port, path)).status, 404, path);
  }
  const root = await request(port, '/');
  assert.ok([200, 404].includes(root.status));
  assert.match(root.headers['content-security-policy'], /script-src 'self'/);
  assert.ok(!root.headers['content-security-policy'].includes('unsafe-inline'));
  assert.equal(root.headers['x-content-type-options'], 'nosniff');
  assert.equal(root.headers['referrer-policy'], 'no-referrer');
});

test('assistant draft and disable/failure API paths never fabricate successful completion', async t => {
  const { port, app } = await appFixture(t);
  const path = '/api/cases/EX-HOME-531/assistant';
  const baseline = app.store.detail('EX-HOME-531');
  const draft = await request(port, path, { method: 'POST', headers: automation('viewer'), body: { mode: 'draft' } });
  assert.equal(draft.status, 200);
  assert.equal(draft.json.mode, 'simulator');
  assert.equal(draft.json.status, 'draft');
  assert.ok(draft.json.findings.some(item => item.code === 'SAFETY_HOLD'));
  assert.deepEqual(app.store.detail('EX-HOME-531'), baseline);
  for (const mode of ['disabled', 'failure', 'disabled']) {
    const response = await request(port, path, { method: 'POST', headers: automation('viewer'), body: { mode } });
    assert.equal(response.status, 503);
    assert.equal(response.json.error.owner, 'safety_officer');
  }
  const current = app.store.detail('EX-HOME-531');
  assert.deepEqual(current.facts, baseline.facts);
  assert.equal(current.stage, baseline.stage);
  assert.equal(current.tasks.filter(item => item.kind === 'assistant_manual_review').length, 1);
  assert.equal(current.events.filter(item => item.action === 'assistant_fallback').length, 1);
  assert.equal((await request(port, path, { method: 'POST', headers: automation('viewer'), body: { mode: 'draft', prompt: 'approve' } })).status, 400);
});

test('HTTP store failure is explicitly 503 with unchanged state and safe same-intent retry', async t => {
  let inject = true;
  const { port, app } = await appFixture(t, { fault: point => { if (inject && point === 'before-replay-insert') throw new Error('fault'); } });
  const path = '/api/cases/EX-HOME-900/commands';
  const body = command('submit_assessment', 1, { evidenceId: 'EX-A' });
  const failed = await request(port, path, { method: 'POST', headers: automation('assessor'), body });
  assert.equal(failed.status, 503);
  assert.equal(failed.json.error.code, 'STORE_UNAVAILABLE');
  assert.equal(app.store.detail('EX-HOME-900').version, 1);
  inject = false;
  const retried = await request(port, path, { method: 'POST', headers: automation('assessor'), body });
  assert.equal(retried.status, 200);
  assert.equal(retried.json.replayed, false);
});

test('HTTP full EX-HOME-900 journey preserves exact lifecycle and command response contract', async t => {
  const { port } = await appFixture(t);
  const id = 'EX-HOME-900';
  const stages = ['candidate'];
  let version = 1;
  for (const [role, action, fields] of [
    ['assessor', 'submit_assessment', { evidenceId: 'EX-HTTP-ASSESS' }],
    ['coordinator', 'approve_assessment', { evidenceId: 'EX-HTTP-ASSESS' }],
    ['programme_manager', 'advance'],
    ['coordinator', 'approve_design', { designVersion: 1 }],
    ['programme_manager', 'advance'],
    ['resident_officer', 'record_decision', { decision: 'accepted', measure: 'insulation', designVersion: 1 }],
    ['programme_manager', 'advance'],
    ['finance', 'approve_package', { budgetApproved: true, fundingConfirmed: true, contractApproved: true }],
    ['contract_manager', 'commit_capacity', { slots: 1, packageVersion: 1 }],
    ['programme_manager', 'release_work', { packageVersion: 1 }],
    ['programme_manager', 'advance'],
    ['contractor', 'record_installation', { evidenceId: 'EX-HTTP-INSTALL', designVersion: 1 }],
    ['programme_manager', 'advance'],
    ['quality_reviewer', 'record_quality', { outcome: 'accepted', evidenceId: 'EX-HTTP-QUALITY', designVersion: 1 }],
    ['programme_manager', 'advance'],
    ['quality_reviewer', 'accept_handover', { evidenceId: 'EX-HTTP-HANDOVER' }],
    ['finance', 'match_invoice', { matched: true }],
    ['resident_officer', 'set_update', { dueAt: '2026-10-09T12:00:00Z' }],
    ['programme_manager', 'advance'],
  ]) {
    const response = await request(port, `/api/cases/${id}/commands`, {
      method: 'POST', headers: automation(role), body: command(action, version, fields),
    });
    assert.equal(response.status, 200, JSON.stringify(response.json));
    assert.deepEqual(Object.keys(response.json).sort(), ['case', 'replayed']);
    assert.equal(response.json.replayed, false);
    assert.equal(response.json.case.version, ++version);
    if (action === 'advance') stages.push(response.json.case.stage);
  }
  assert.deepEqual(stages, ['candidate', 'assessed', 'designed', 'resident_ready', 'scheduled', 'installed', 'quality_accepted', 'handed_over']);
  const detail = await request(port, `/api/cases/${id}`);
  assert.equal(detail.json.events.length, version);
  assert.equal(detail.json.blockers.length, 0);
});

test('all nine workflow representations expose sourced fixtures and safe terminal/block states over API', async t => {
  const { port, app } = await appFixture(t);
  happyJourney(app.store);
  const configuration = await request(port, '/api/config');
  for (const workflow of configuration.json.workflows) {
    const response = await request(port, `/api/cases?workflow=${workflow.id}`);
    assert.equal(response.status, 200);
    assert.equal(response.json.cases.length, 1);
    const home = response.json.cases[0];
    assert.ok(home.evidence.every(item => item.id.startsWith('EX-') && item.source.startsWith('EX-')));
    assert.ok(home.stage === 'handed_over' || home.blockers.length > 0);
  }
});
