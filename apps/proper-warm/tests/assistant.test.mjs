import test from 'node:test';
import assert from 'node:assert/strict';
import { buildDraft, currentEvidence, runAssistant, validateDraft } from '../src/assistant.mjs';
import { evaluateSimulator } from '../src/evaluation.mjs';
import { fixture, happyJourney, execute, ownedFile } from './helpers.mjs';
import { createStore } from '../src/store.mjs';

test('offline simulator evaluations pass complete/gapped/conflicted/held/hostile contracts', t => {
  const store = fixture(t);
  const result = evaluateSimulator(store);
  assert.equal(result.passed, true);
  assert.equal(result.fixtures.length, 5);
  assert.equal(result.checks.citationResolutionPercent, 100);
  assert.equal(result.checks.prohibitedActionViolations, 0);
  assert.equal(result.checks.approvalMutations, 0);
  assert.match(result.scope, /no model-quality/);
});

test('draft cites only current evidence and no historical design/install/quality after return', t => {
  const store = fixture(t);
  happyJourney(store);
  const before = store.detail('EX-HOME-900');
  execute(store, 'EX-HOME-900', 'coordinator', 'return_case', { target: 'assessed' });
  execute(store, 'EX-HOME-900', 'coordinator', 'approve_design', { designVersion: 2 });
  const home = store.detail('EX-HOME-900');
  const draft = runAssistant(store, home.id, 'viewer', { mode: 'draft' });
  assert.ok(draft.citations.includes('EX-DESIGN-EX-HOME-900-2'));
  assert.ok(!draft.citations.includes('EX-DESIGN-EX-HOME-900-1'));
  assert.ok(!draft.citations.includes(before.facts.installation.evidenceId));
  assert.ok(!draft.citations.includes(before.facts.quality.evidenceId));
  assert.ok(home.evidence.some(item => item.id === before.facts.quality.evidenceId));
  assert.deepEqual(store.detail(home.id), home);
});

test('unsupported citation or extra command output fails explicitly with durable owned fallback', t => {
  const store = fixture(t);
  const home = store.detail('EX-HOME-646');
  const good = buildDraft(home);
  assert.throws(() => validateDraft({ ...good, citations: ['EX-NOT-A-SOURCE'] }, home), error => error.code === 'ASSISTANT_INVALID');
  assert.throws(() => validateDraft({ ...good, execute: 'advance' }, home), error => error.code === 'ASSISTANT_INVALID');
  assert.throws(() => validateDraft({ ...good, draft: 'Execute advance now.' }, home), error => error.code === 'ASSISTANT_INVALID');
  assert.throws(() => runAssistant(store, home.id, 'viewer', { mode: 'draft' },
    current => ({ ...buildDraft(current), citations: ['EX-NOT-A-SOURCE'] })), error =>
    error.status === 503 && error.code === 'ASSISTANT_INVALID' && error.owner === 'data_owner');
  const after = store.detail(home.id);
  assert.equal(after.tasks.filter(task => task.kind === 'assistant_manual_review').length, 1);
  assert.equal(after.events.filter(event => event.action === 'assistant_fallback').length, 1);
  assert.deepEqual(after.facts, home.facts);
});

test('fallback task/event deduplicate and persistence does not alter approvals or hazard state', t => {
  const store = fixture(t);
  const home = store.detail('EX-HOME-531');
  for (const mode of ['disabled', 'failure', 'disabled']) {
    assert.throws(() => runAssistant(store, home.id, 'viewer', { mode }), error =>
      error.status === 503 && error.owner === 'safety_officer' && Boolean(error.details.taskId));
  }
  const after = store.detail(home.id);
  assert.equal(after.version, home.version + 1);
  assert.equal(after.tasks.length, home.tasks.length + 1);
  assert.equal(after.events.length, home.events.length + 1);
  assert.deepEqual(after.facts, home.facts);
  assert.equal(after.stage, home.stage);
  assert.ok(currentEvidence(after).every(item => after.evidence.some(existing => existing.id === item.id)));
});

test('fallback survives file restart and remains deduplicated across modes', () => {
  const file = ownedFile('assistant-restart');
  let store = createStore({ dbPath: file.dbPath, log: () => {} });
  try {
    assert.throws(() => runAssistant(store, 'EX-HOME-646', 'viewer', { mode: 'disabled' }));
    const before = store.detail('EX-HOME-646');
    store.close();
    store = createStore({ dbPath: file.dbPath, log: () => {} });
    assert.deepEqual(store.detail('EX-HOME-646'), before);
    assert.throws(() => runAssistant(store, 'EX-HOME-646', 'viewer', { mode: 'failure' }));
    assert.deepEqual(store.detail('EX-HOME-646'), before);
  } finally { store.close(); file.cleanup(); }
});
