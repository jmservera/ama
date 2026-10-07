import { randomUUID } from 'node:crypto';
import { mkdirSync, rmSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createStore } from '../src/store.mjs';

export const testDirectory = resolve(dirname(fileURLToPath(import.meta.url)), '..', '.test-data');
export function ownedFile(label = 'test') {
  mkdirSync(testDirectory, { recursive: true });
  const dbPath = resolve(testDirectory, `${label}-${process.pid}-${randomUUID()}.db`);
  return {
    dbPath,
    cleanup() {
      for (const suffix of ['', '-wal', '-shm', '-journal']) rmSync(dbPath + suffix, { force: true });
    },
  };
}
export function fixture(t, options = {}) {
  const file = ownedFile();
  const store = createStore({ dbPath: file.dbPath, log: () => {}, ...options });
  t.after(() => { store.close(); file.cleanup(); });
  return store;
}
export function intent(store, id, role, action, fields = {}, overrides = {}) {
  return { action, expectedVersion: store.detail(id).version, idempotencyKey: randomUUID(),
    payload: { ...fields, reason: 'Constructed exercise decision', source: 'EX-SOURCE-TEST', ...overrides } };
}
export function execute(store, id, role, action, fields = {}, overrides = {}) {
  return store.execute(id, role, intent(store, id, role, action, fields, overrides)).case;
}
export function happyJourney(store, id = 'EX-HOME-900') {
  const snapshots = [store.detail(id).stage];
  const act = (role, action, fields) => execute(store, id, role, action, fields);
  const advance = () => { const home = act('programme_manager', 'advance'); snapshots.push(home.stage); };
  act('assessor', 'submit_assessment', { evidenceId: `EX-ASSESS-${id}` });
  act('coordinator', 'approve_assessment', { evidenceId: `EX-ASSESS-${id}` });
  advance();
  act('coordinator', 'approve_design', { designVersion: 1 });
  advance();
  act('resident_officer', 'record_decision', { decision: 'accepted', measure: 'insulation', designVersion: 1 });
  advance();
  act('finance', 'approve_package', { budgetApproved: true, fundingConfirmed: true, contractApproved: true });
  act('contract_manager', 'commit_capacity', { slots: 1, packageVersion: 1 });
  act('programme_manager', 'release_work', { packageVersion: 1 });
  advance();
  act('contractor', 'record_installation', { evidenceId: `EX-INSTALL-${id}`, designVersion: 1 });
  advance();
  act('quality_reviewer', 'record_quality', { outcome: 'accepted', evidenceId: `EX-QUALITY-${id}`, designVersion: 1 });
  advance();
  act('quality_reviewer', 'accept_handover', { evidenceId: `EX-HANDOVER-${id}` });
  act('finance', 'match_invoice', { matched: true });
  act('resident_officer', 'set_update', { dueAt: '2026-10-09T12:00:00Z' });
  advance();
  return snapshots;
}
