import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { writeFileSync, readFileSync } from 'node:fs';
import { config, lifecycle, commands, filterCases, portfolio, blockers } from '../src/domain.mjs';
import { createStore, requestHash } from '../src/store.mjs';
import { fixture, ownedFile, intent, execute, happyJourney } from './helpers.mjs';

const is = (code, status) => error => error.code === code && (!status || error.status === status);
const home = 'EX-HOME-900';

test('nine constructed workflows, paired homes and precise case/config shapes', t => {
  const store = fixture(t);
  const cases = store.list();
  assert.equal(cases.length, 9);
  assert.deepEqual(new Set(cases.map(item => item.workflow)), new Set(config.workflows.map(item => item.id)));
  assert.deepEqual(Object.keys(store.detail(home)).sort(), [
    'id', 'homeId', 'buildingId', 'schemeId', 'workflow', 'stage', 'version', 'owner', 'blockers',
    'evidence', 'facts', 'handoff', 'residentUpdate', 'tasks', 'appointments', 'allowedActions', 'events',
  ].sort());
  assert.equal(store.detail('EX-HOME-208').buildingId, store.detail('EX-HOME-317').buildingId);
  assert.equal(store.detail('EX-HOME-208').facts.packageId, store.detail('EX-HOME-317').facts.packageId);
  assert.equal(config.roles.length, 11);
  assert.equal(config.commands.length, 22);
  assert.deepEqual(Object.keys(config).sort(), ['roles', 'workflows', 'lifecycle', 'commands', 'banner'].sort());
});

test('happy lifecycle requires independently sourced approvals and a separate handover', t => {
  const store = fixture(t);
  assert.deepEqual(happyJourney(store), lifecycle);
  const completed = store.detail(home);
  assert.equal(completed.stage, 'handed_over');
  assert.equal(completed.blockers.length, 0);
  assert.equal(completed.events.length, completed.version);
  assert.ok(completed.events.every(event => event.actor === 'system' || event.payload.source.startsWith('EX-')));
  assert.equal(completed.facts.grants.received, null);
  assert.throws(() => execute(store, home, 'programme_manager', 'advance'), is('GATE_BLOCKED', 422));
});

test('authority and closed payload/envelope reject actor or owner injection', t => {
  const store = fixture(t);
  for (const spec of commands) {
    if (!spec.roles.includes('viewer')) {
      assert.throws(() => store.execute(home, 'viewer', { action: spec.action, expectedVersion: 1,
        idempotencyKey: 'EX-KEY', payload: {} }), is('FORBIDDEN', 403));
    }
  }
  assert.throws(() => execute(store, home, 'contractor', 'record_quality', { outcome: 'accepted', evidenceId: 'EX-Q', designVersion: 1 }), is('FORBIDDEN'));
  assert.throws(() => execute(store, home, 'assessor', 'submit_assessment', { evidenceId: 'EX-A', owner: 'finance' }), is('INVALID_PAYLOAD', 400));
  const body = intent(store, home, 'assessor', 'submit_assessment', { evidenceId: 'EX-A' });
  assert.throws(() => store.execute(home, 'assessor', { ...body, role: 'coordinator' }), is('INVALID_PAYLOAD'));
  assert.throws(() => store.execute(home, 'made_up', body), is('FORBIDDEN'));
  assert.throws(() => execute(store, home, 'assessor', 'submit_assessment', { evidenceId: 'EX-A' }, { reason: '' }), is('INVALID_PAYLOAD'));
  assert.deepEqual(store.detail(home, 'viewer').allowedActions, []);
  assert.ok(store.detail(home, 'programme_manager').allowedActions.includes('advance'));
});

test('assessment submission never self-approves and exact blocker owner is visible', t => {
  const store = fixture(t);
  execute(store, home, 'assessor', 'submit_assessment', { evidenceId: 'EX-A' });
  assert.throws(() => execute(store, home, 'programme_manager', 'advance'), error =>
    error.code === 'GATE_BLOCKED' && error.owner === 'coordinator' && error.details.some(item => item.code === 'ASSESSMENT_APPROVAL'));
  assert.throws(() => execute(store, home, 'coordinator', 'approve_assessment', { evidenceId: 'EX-WRONG' }), is('GATE_BLOCKED'));
  execute(store, home, 'coordinator', 'approve_assessment', { evidenceId: 'EX-A' });
  execute(store, home, 'programme_manager', 'advance');
  assert.equal(store.detail(home).stage, 'assessed');
});

test('retry replays original snapshot before version check with canonical payload keys', t => {
  const store = fixture(t);
  const body = intent(store, home, 'assessor', 'submit_assessment', { evidenceId: 'EX-A' });
  const first = store.execute(home, 'assessor', body);
  execute(store, home, 'coordinator', 'approve_assessment', { evidenceId: 'EX-A' });
  const reordered = { ...body, payload: { source: body.payload.source, reason: body.payload.reason, evidenceId: 'EX-A' } };
  const replay = store.execute(home, 'assessor', reordered);
  assert.equal(replay.replayed, true);
  assert.deepEqual(replay.case, first.case);
  assert.ok(store.detail(home).version > replay.case.version);
  assert.throws(() => store.execute(home, 'assessor', { ...body, expectedVersion: store.detail(home).version }), is('IDEMPOTENCY_CONFLICT', 409));
  assert.throws(() => store.execute(home, 'assessor', { ...body, payload: { ...body.payload, evidenceId: 'EX-DIFF' } }), is('IDEMPOTENCY_CONFLICT'));
  assert.throws(() => store.execute(home, 'assessor', { ...body, idempotencyKey: 'EX-FRESH' }), is('VERSION_CONFLICT', 409));
  assert.equal(requestHash(home, 'assessor', body), requestHash(home, 'assessor', reordered));
});

test('same key is bound to actor even on shared role command', t => {
  const store = fixture(t);
  const id = 'EX-HOME-863';
  const body = intent(store, id, 'coordinator', 'send_handoff', { destination: 'finance' });
  execute(store, id, 'resident_officer', 'return_handoff', { handoffId: 'EX-HANDOFF-863' });
  body.expectedVersion = store.detail(id).version;
  store.execute(id, 'coordinator', body);
  assert.throws(() => store.execute(id, 'finance', body), is('IDEMPOTENCY_CONFLICT'));
});

test('injected interrupted writes roll back case/event/replay and survive reopen', () => {
  for (const failurePoint of ['after-case-write', 'before-replay-insert', 'before-commit']) {
    const file = ownedFile('rollback');
    let fail = false;
    let store = createStore({ dbPath: file.dbPath, log: () => {}, fault: point => { if (fail && point === failurePoint) throw new Error('Injected failure'); } });
    const baseline = store.detail(home);
    const body = intent(store, home, 'assessor', 'submit_assessment', { evidenceId: 'EX-A' });
    try {
      fail = true;
      assert.throws(() => store.execute(home, 'assessor', body), is('STORE_UNAVAILABLE', 503));
      store.close();
      store = createStore({ dbPath: file.dbPath, log: () => {} });
      assert.deepEqual(store.detail(home), baseline);
      const result = store.execute(home, 'assessor', body);
      assert.equal(result.replayed, false);
      assert.equal(result.case.version, baseline.version + 1);
      assert.equal(store.execute(home, 'assessor', body).replayed, true);
    } finally { store.close(); file.cleanup(); }
  }
});

test('file restart preserves exact state including quotes without SQL interpolation', () => {
  const file = ownedFile('restart');
  let store = createStore({ dbPath: file.dbPath, log: () => {} });
  try {
    const value = "O'Brien'); DROP TABLE cases; --";
    const body = intent(store, 'EX-HOME-646', 'data_owner', 'resolve_conflict', { value });
    store.execute('EX-HOME-646', 'data_owner', body);
    const before = store.detail('EX-HOME-646');
    store.close();
    store = createStore({ dbPath: file.dbPath, log: () => {} });
    assert.deepEqual(store.detail('EX-HOME-646'), before);
    assert.equal(store.detail('EX-HOME-646').facts.conflict.value, value);
    assert.equal(store.list().length, 9);
    assert.equal(store.execute('EX-HOME-646', 'data_owner', body).replayed, true);
  } finally { store.close(); file.cleanup(); }
});

test('incompatible, corrupted and initialized-empty stores fail rather than reset', () => {
  const corrupt = ownedFile('corrupt');
  try {
    writeFileSync(corrupt.dbPath, 'not a sqlite database');
    assert.throws(() => createStore({ dbPath: corrupt.dbPath }));
    assert.equal(readFileSync(corrupt.dbPath, 'utf8'), 'not a sqlite database');
  } finally { corrupt.cleanup(); }
  for (const mutation of [
    "UPDATE metadata SET value='wrong' WHERE key='schema_version'",
    "UPDATE cases SET json=json_set(json,'$.stage','not-a-stage') WHERE id='EX-HOME-900'",
    'DELETE FROM events; DELETE FROM cases',
    'CREATE TABLE foreign_data(id INTEGER)',
  ]) {
    const file = ownedFile('incompatible');
    const store = createStore({ dbPath: file.dbPath, log: () => {} });
    store.close();
    const db = new DatabaseSync(file.dbPath);
    db.exec(mutation);
    db.close();
    try { assert.throws(() => createStore({ dbPath: file.dbPath, log: () => {} })); }
    finally { file.cleanup(); }
  }
});

test('atomic seed failure does not leave a partial fixture marker', () => {
  const file = ownedFile('seed-failure');
  try {
    assert.throws(() => createStore({ dbPath: file.dbPath, log: () => {}, fault: point => { if (point === 'after-seed') throw new Error('failure'); } }), is('STORE_UNAVAILABLE'));
    const db = new DatabaseSync(file.dbPath);
    assert.equal(db.prepare("SELECT COUNT(*) AS count FROM sqlite_master WHERE type='table'").get().count, 0);
    db.close();
    const store = createStore({ dbPath: file.dbPath, log: () => {} });
    assert.equal(store.list().length, 9);
    store.close();
  } finally { file.cleanup(); }
});

test('resident withdrawal at completion is recorded and invalidates release/acceptance', t => {
  const store = fixture(t);
  happyJourney(store);
  const before = store.detail(home);
  const result = execute(store, home, 'resident_officer', 'record_decision', { decision: 'withdrawn', measure: 'insulation', designVersion: 1 });
  assert.equal(result.stage, 'designed');
  assert.equal(result.facts.release, null);
  assert.equal(result.facts.quality, null);
  assert.equal(result.facts.handover, null);
  assert.deepEqual(result.facts.installation, before.facts.installation);
  assert.deepEqual(result.residentUpdate, before.residentUpdate);
  assert.ok(result.tasks.some(task => task.kind === 'resident_reassessment'));
  assert.throws(() => execute(store, home, 'programme_manager', 'advance'), is('GATE_BLOCKED'));
});

test('shared building never propagates consent, hold, capacity or evidence', t => {
  const store = fixture(t);
  const untouched = store.detail('EX-HOME-317');
  execute(store, 'EX-HOME-208', 'resident_officer', 'record_decision', { decision: 'declined', measure: 'insulation', designVersion: 1 });
  assert.deepEqual(store.detail('EX-HOME-317'), untouched);
  assert.equal(store.detail('EX-HOME-208').facts.decision.decision, 'declined');
  assert.equal(untouched.facts.decision.decision, 'accepted');
});

test('replacement needs return; return preserves history/package/invoice/update and v1 cannot cover v2', t => {
  const store = fixture(t);
  happyJourney(store);
  assert.throws(() => execute(store, home, 'coordinator', 'approve_design', { designVersion: 2 }), is('GATE_BLOCKED'));
  assert.throws(() => execute(store, home, 'assessor', 'submit_assessment', { evidenceId: 'EX-NEW' }), is('GATE_BLOCKED'));
  const before = store.detail(home);
  const returned = execute(store, home, 'coordinator', 'return_case', { target: 'assessed' });
  assert.deepEqual(returned.facts.assessment, before.facts.assessment);
  assert.deepEqual(returned.facts.package, before.facts.package);
  assert.deepEqual(returned.facts.invoice, before.facts.invoice);
  assert.deepEqual(returned.residentUpdate, before.residentUpdate);
  assert.deepEqual(returned.evidence, before.evidence);
  for (const key of ['design', 'decision', 'capacity', 'release', 'installation', 'quality', 'handover']) assert.equal(returned.facts[key], null);
  execute(store, home, 'coordinator', 'approve_design', { designVersion: 2 });
  execute(store, home, 'programme_manager', 'advance');
  assert.throws(() => execute(store, home, 'resident_officer', 'record_decision', { decision: 'accepted', measure: 'insulation', designVersion: 1 }), is('GATE_BLOCKED'));
  assert.throws(() => execute(store, home, 'resident_officer', 'record_decision', { decision: 'accepted', measure: 'heating', designVersion: 2 }), is('GATE_BLOCKED'));
});

test('quality return at completion reverses handover and new evidence is required', t => {
  const store = fixture(t);
  happyJourney(store);
  const before = store.detail(home);
  const returned = execute(store, home, 'quality_reviewer', 'record_quality', { outcome: 'returned', evidenceId: 'EX-RETURNED', designVersion: 1 });
  assert.equal(returned.stage, 'installed');
  assert.equal(returned.facts.handover, null);
  assert.equal(returned.facts.quality.outcome, 'returned');
  assert.throws(() => execute(store, home, 'programme_manager', 'advance'), is('GATE_BLOCKED'));
  assert.throws(() => execute(store, home, 'quality_reviewer', 'record_quality', { outcome: 'accepted', evidenceId: 'EX-RETURNED', designVersion: 1 }), is('GATE_BLOCKED'));
  assert.throws(() => execute(store, home, 'quality_reviewer', 'record_quality', { outcome: 'accepted', evidenceId: 'EX-Q2', designVersion: 2 }), is('GATE_BLOCKED'));
  execute(store, home, 'quality_reviewer', 'record_quality', { outcome: 'accepted', evidenceId: 'EX-Q2', designVersion: 1 });
  execute(store, home, 'programme_manager', 'advance');
  assert.equal(store.detail(home).stage, 'quality_accepted');
  assert.equal(store.detail(home).facts.handover, null);
  assert.deepEqual(store.detail(home).residentUpdate, before.residentUpdate);
  assert.ok(store.detail(home).tasks.some(task => task.kind === 'reinspection' && task.status === 'resolved'));
});

test('accepted quality replacement invalidates completed handover until independently reaccepted', t => {
  const store = fixture(t);
  happyJourney(store);
  const before = store.detail(home);
  const completedCount = () => portfolio(store.list(), {}, '2026-10-10T12:00:00Z')
    .metrics.find(metric => metric.id === 'handed_over').numerator;
  assert.equal(completedCount(), 1);
  const body = intent(store, home, 'quality_reviewer', 'record_quality', {
    outcome: 'accepted', evidenceId: 'EX-QUALITY-REPLACEMENT', designVersion: 1,
  });
  const result = store.execute(home, 'quality_reviewer', body).case;
  assert.equal(result.stage, 'quality_accepted');
  assert.equal(result.facts.quality.outcome, 'accepted');
  assert.equal(result.facts.handover, null);
  assert.ok(result.blockers.some(blocker => blocker.code === 'HANDOVER_ACCEPTANCE'));
  assert.equal(completedCount(), 0);
  assert.deepEqual(result.facts.invoice, before.facts.invoice);
  assert.deepEqual(result.residentUpdate, before.residentUpdate);
  assert.ok(before.evidence.every(item => result.evidence.some(saved => saved.id === item.id)));
  assert.equal(result.events.length, before.events.length + 1);
  assert.equal(store.execute(home, 'quality_reviewer', body).replayed, true);
  assert.equal(store.detail(home).events.length, result.events.length);
  assert.throws(() => execute(store, home, 'programme_manager', 'advance'), is('GATE_BLOCKED'));
  execute(store, home, 'quality_reviewer', 'accept_handover', { evidenceId: 'EX-HANDOVER-REACCEPTED' });
  assert.equal(completedCount(), 0);
  execute(store, home, 'programme_manager', 'advance');
  assert.equal(store.detail(home).stage, 'handed_over');
  assert.equal(completedCount(), 1);
});

test('return targets enforce target-specific authority', t => {
  const store = fixture(t);
  assert.throws(() => execute(store, 'EX-HOME-422', 'coordinator', 'return_case', { target: 'installed' }), is('FORBIDDEN'));
  assert.throws(() => execute(store, 'EX-HOME-422', 'quality_reviewer', 'return_case', { target: 'assessed' }), is('FORBIDDEN'));
  execute(store, 'EX-HOME-422', 'quality_reviewer', 'return_case', { target: 'installed' });
  assert.equal(store.detail('EX-HOME-422').facts.quality, null);
});

test('package approvals, capacity version and explicit release remain distinct', t => {
  const store = fixture(t);
  const id = 'EX-HOME-317';
  assert.throws(() => execute(store, id, 'programme_manager', 'advance'), error => error.details.some(item => item.code === 'CAPACITY_COMMITMENT'));
  assert.throws(() => execute(store, id, 'contract_manager', 'commit_capacity', { slots: 1, packageVersion: 2 }), is('GATE_BLOCKED'));
  execute(store, id, 'contract_manager', 'commit_capacity', { slots: 1, packageVersion: 1 });
  assert.throws(() => execute(store, id, 'programme_manager', 'advance'), error => error.details.some(item => item.code === 'WORK_RELEASE'));
  execute(store, id, 'programme_manager', 'release_work', { packageVersion: 1 });
  execute(store, id, 'programme_manager', 'advance');
  assert.throws(() => execute(store, id, 'contractor', 'record_installation', { evidenceId: 'EX-I', designVersion: 2 }), is('GATE_BLOCKED'));
});

test('continuing predicates are checked, unknown never bypasses each edge', t => {
  const store = fixture(t);
  happyJourney(store);
  const completed = store.detail(home);
  for (const [key, change, code] of [
    ['conflict', { resolved: false }, 'DATA_CONFLICT'],
    ['assessment', { submitted: true, approved: false }, 'ASSESSMENT_APPROVAL'],
    ['design', null, 'DESIGN_APPROVAL'],
    ['decision', { decision: 'withdrawn' }, 'RESIDENT_DECISION'],
    ['package', { version: 1, budgetApproved: null, fundingConfirmed: true, contractApproved: true }, 'PACKAGE_APPROVAL'],
    ['capacity', { slots: 1, packageVersion: 999 }, 'CAPACITY_COMMITMENT'],
    ['release', null, 'WORK_RELEASE'],
    ['installation', { evidenceId: 'EX-I', designVersion: 999 }, 'INSTALLATION_EVIDENCE'],
    ['quality', { outcome: 'returned', designVersion: 1 }, 'QUALITY_ACCEPTANCE'],
    ['handover', null, 'HANDOVER_ACCEPTANCE'],
    ['invoice', { matched: false }, 'INVOICE_MATCH'],
  ]) {
    const altered = structuredClone(completed);
    altered.facts[key] = change;
    assert.ok(blockers(altered, 'handed_over').some(item => item.code === code), key);
  }
});

test('hazard acknowledgment never clears hold, referral or separate clock', t => {
  const store = fixture(t);
  const id = 'EX-HOME-531';
  const baseline = store.detail(id);
  execute(store, id, 'safety_officer', 'acknowledge_referral', { referralId: 'EX-REFERRAL-531' });
  const after = store.detail(id);
  assert.equal(after.facts.hazard.hold, true);
  assert.equal(after.facts.hazard.referralId, baseline.facts.hazard.referralId);
  assert.equal(after.facts.hazard.externalClock, baseline.facts.hazard.externalClock);
  assert.throws(() => execute(store, id, 'programme_manager', 'advance'), error =>
    error.owner === 'safety_officer' && error.details.some(item => item.code === 'SAFETY_HOLD'));
  assert.throws(() => execute(store, id, 'safety_officer', 'acknowledge_referral', { referralId: 'EX-REFERRAL-531', hold: false }), is('INVALID_PAYLOAD'));
});

test('strict 5/6 threshold, event exclusions, appointment identity, no reset, referral continuity', t => {
  const store = fixture(t);
  const id = 'EX-HOME-531';
  const add = (appointmentId, fields = {}) => execute(store, id, 'resident_officer', 'record_appointment', {
    appointmentId, confirmed: true, verified: true, outcome: 'resident_no_access', ...fields,
  });
  for (const outcome of ['provider_no_show', 'cancelled', 'rescheduled', 'kept']) add(`EX-${outcome}`, { outcome });
  add('EX-UNCONFIRMED', { confirmed: false });
  add('EX-UNVERIFIED', { verified: false });
  assert.equal(store.detail(id).facts.noAccess.count, 0);
  for (let index = 1; index <= 5; index++) add(`EX-APPOINTMENT-${index}`);
  assert.equal(store.detail(id).facts.noAccess.count, 5);
  assert.equal(store.detail(id).tasks.filter(task => task.kind === 'no_access_investigation').length, 0);
  add('EX-APPOINTMENT-6');
  add('EX-APPOINTMENT-7');
  assert.equal(store.detail(id).tasks.filter(task => task.kind === 'no_access_investigation' && task.owner === 'resident_officer').length, 1);
  assert.throws(() => add('EX-APPOINTMENT-6'), is('APPOINTMENT_CONFLICT'));
  assert.equal(store.detail(id).facts.noAccess.count, 7);
  assert.equal(store.detail(id).facts.decision, null);
  assert.equal(store.detail(id).facts.hazard.hold, true);
  execute(store, id, 'safety_officer', 'acknowledge_referral', { referralId: 'EX-REFERRAL-531' });
  assert.equal(store.detail(id).stage, 'candidate');
});

test('configured no-access threshold is immutable across restart', () => {
  const file = ownedFile('threshold');
  try {
    const store = createStore({ dbPath: file.dbPath, threshold: 1, log: () => {} });
    assert.equal(store.detail(home).facts.noAccess.threshold, 1);
    store.close();
    assert.throws(() => createStore({ dbPath: file.dbPath, threshold: 2, log: () => {} }));
  } finally { file.cleanup(); }
});

test('handoff send/receipt/accept/return retain update owner and enforce active identity', t => {
  const store = fixture(t);
  const id = 'EX-HOME-863';
  const baseline = store.detail(id);
  assert.throws(() => execute(store, id, 'finance', 'receive_handoff', { handoffId: 'EX-HANDOFF-863' }), is('FORBIDDEN'));
  assert.throws(() => execute(store, id, 'resident_officer', 'accept_handoff', { handoffId: 'EX-HANDOFF-863' }), is('GATE_BLOCKED'));
  assert.throws(() => execute(store, id, 'resident_officer', 'receive_handoff', { handoffId: 'EX-WRONG' }), is('GATE_BLOCKED'));
  execute(store, id, 'resident_officer', 'receive_handoff', { handoffId: 'EX-HANDOFF-863' });
  assert.equal(store.detail(id).owner, 'coordinator');
  execute(store, id, 'resident_officer', 'accept_handoff', { handoffId: 'EX-HANDOFF-863' });
  assert.equal(store.detail(id).owner, 'resident_officer');
  assert.deepEqual(store.detail(id).residentUpdate, baseline.residentUpdate);
  assert.throws(() => execute(store, id, 'coordinator', 'send_handoff', { destination: 'finance' }), is('FORBIDDEN'));
  const sent = execute(store, id, 'resident_officer', 'send_handoff', { destination: 'finance' });
  assert.equal(sent.owner, 'resident_officer');
  assert.match(sent.handoff.id, /^EX-HANDOFF-/);
  const returned = execute(store, id, 'finance', 'return_handoff', { handoffId: sent.handoff.id });
  assert.equal(returned.owner, 'resident_officer');
  assert.equal(returned.handoff.status, 'returned');
  assert.equal(returned.residentUpdate.owner, 'resident_officer');
});

test('grant opportunity/award/claim/receipt have separate ordered sourced amounts', t => {
  const store = fixture(t);
  assert.throws(() => execute(store, home, 'finance', 'record_grant', { state: 'received', amount: 50 }), is('GATE_BLOCKED'));
  execute(store, home, 'finance', 'record_grant', { state: 'opportunity', amount: 7500 });
  assert.equal(store.detail(home).facts.grants.awarded, null);
  assert.throws(() => execute(store, home, 'finance', 'record_grant', { state: 'awarded', amount: 8000 }), is('GATE_BLOCKED'));
  execute(store, home, 'finance', 'record_grant', { state: 'awarded', amount: 7000 });
  execute(store, home, 'finance', 'record_grant', { state: 'claimed', amount: 6000 });
  assert.equal(store.detail(home).facts.grants.received, null);
  execute(store, home, 'finance', 'record_grant', { state: 'received', amount: 5500 });
  assert.deepEqual(Object.values(store.detail(home).facts.grants).map(item => item.amount), [7500, 7000, 6000, 5500]);
  assert.throws(() => execute(store, home, 'finance', 'record_grant', { state: 'opportunity', amount: 9000 }), is('GATE_BLOCKED'));
});

test('filtered portfolio denominator and exact drilldown cohort reconcile', t => {
  const store = fixture(t);
  const all = store.list();
  const scope = { workflow: 'hazards', q: '531' };
  const filtered = filterCases(all, scope.workflow, scope.q);
  const report = portfolio(filtered, scope, '2026-10-10T12:00:00Z');
  assert.equal(filtered.length, 1);
  for (const metric of report.metrics) {
    assert.equal(metric.denominator, filtered.length);
    assert.equal(metric.numerator, metric.caseIds.length);
    assert.ok(metric.caseIds.every(id => filtered.some(item => item.id === id)));
  }
  assert.deepEqual(report.metrics.find(item => item.id === 'safety_holds').caseIds, ['EX-HOME-531']);
  assert.equal(filterCases(all, '', 'EX-BUILDING-PAIR').length, 2);
  assert.equal(filterCases(all, '', 'CoOrDiNaToR').length, 2);
  assert.throws(() => filterCases(all, 'typo'), is('INVALID_FILTER', 400));
  const empty = portfolio([], {}, new Date().toISOString());
  assert.ok(empty.metrics.every(item => item.denominator === 0 && item.numerator === 0));
});
