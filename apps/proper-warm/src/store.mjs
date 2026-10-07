import { DatabaseSync } from 'node:sqlite';
import { createHash } from 'node:crypto';
import { mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { AppError, caseView, lifecycle, mutate, roles, workflows, validateEnvelope, validateRole } from './domain.mjs';
import { fixtureVersion, schemaVersion, seedCases } from './seed.mjs';

const canonical = value => Array.isArray(value) ? value.map(canonical)
  : value !== null && typeof value === 'object'
    ? Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])])) : value;
export const requestHash = (id, actor, envelope) => createHash('sha256')
  .update(JSON.stringify(canonical({ id, actor, action: envelope.action,
    expectedVersion: envelope.expectedVersion, payload: envelope.payload }))).digest('hex');

export function createStore({ dbPath, threshold = 5, fault = () => {}, log = record => console.error(JSON.stringify(record)) }) {
  if (!dbPath || !Number.isSafeInteger(threshold) || threshold < 0) throw new Error('Valid database path and immutable nonnegative threshold required.');
  if (dbPath !== ':memory:') mkdirSync(dirname(dbPath), { recursive: true });
  const db = new DatabaseSync(dbPath);
  let closed = false;
  const transaction = operation => {
    let started = false;
    try {
      db.exec('BEGIN IMMEDIATE');
      started = true;
      const result = operation();
      db.exec('COMMIT');
      return result;
    } catch (error) {
      if (started) {
        try { db.exec('ROLLBACK'); } catch { log({ level: 'error', event: 'rollback_failed' }); }
      }
      if (error instanceof AppError) throw error;
      log({ level: 'error', event: 'store_transaction_failed', code: String(error.code ?? 'STORE_FAILURE') });
      throw new AppError(503, 'STORE_UNAVAILABLE', 'Store operation failed; nothing is reported as committed. Retry the same intent/key after readiness recovers.');
    }
  };
  try {
    db.exec('PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;');
    const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").all().map(row => row.name);
    if (!tables.length) {
      transaction(() => {
        db.exec(`
          CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
          CREATE TABLE cases(id TEXT PRIMARY KEY, version INTEGER NOT NULL CHECK(version>0), json TEXT NOT NULL);
          CREATE TABLE events(case_id TEXT NOT NULL REFERENCES cases(id), sequence INTEGER NOT NULL, actor TEXT NOT NULL,
            action TEXT NOT NULL, timestamp TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(case_id,sequence));
          CREATE TABLE idempotency(case_id TEXT NOT NULL REFERENCES cases(id), key TEXT NOT NULL, actor TEXT NOT NULL,
            request_hash TEXT NOT NULL, response TEXT NOT NULL, PRIMARY KEY(case_id,key));
        `);
        const marker = db.prepare('INSERT INTO metadata(key,value) VALUES(?,?)');
        for (const [key, value] of [['schema_version', schemaVersion], ['fixture_version', fixtureVersion], ['no_access_threshold', String(threshold)]]) marker.run(key, value);
        const insertCase = db.prepare('INSERT INTO cases(id,version,json) VALUES(?,?,?)');
        const insertEvent = db.prepare('INSERT INTO events(case_id,sequence,actor,action,timestamp,payload) VALUES(?,?,?,?,?,?)');
        for (const home of seedCases(threshold)) {
          insertCase.run(home.id, home.version, JSON.stringify(home));
          insertEvent.run(home.id, 1, 'system', 'seed_constructed_fixture', '2026-10-07T00:00:00Z', JSON.stringify({ source: `EX-FIXTURE-${home.id}`, fixtureVersion, synthetic: true }));
        }
        fault('after-seed');
      });
    } else {
      if (tables.sort().join(',') !== 'cases,events,idempotency,metadata') throw new Error('Incompatible store tables; refusing reset.');
      const marker = db.prepare('SELECT value FROM metadata WHERE key=?');
      for (const [key, expected] of [['schema_version', schemaVersion], ['fixture_version', fixtureVersion], ['no_access_threshold', String(threshold)]]) {
        if (marker.get(key)?.value !== expected) throw new Error(`Incompatible ${key}; refusing reset.`);
      }
    }
    if (db.prepare('PRAGMA quick_check').get().quick_check !== 'ok') throw new Error('Store integrity check failed.');
    const saved = db.prepare('SELECT id,version,json FROM cases').all();
    if (!saved.length) throw new Error('Initialized store has no fixtures; refusing silent reseed.');
    for (const row of saved) {
      const home = JSON.parse(row.json);
      if (home.id !== row.id || home.version !== row.version || home.facts?.noAccess?.threshold !== threshold
        || !lifecycle.includes(home.stage) || !roles.includes(home.owner)
        || !workflows.some(workflow => workflow.id === home.workflow)
        || typeof home.homeId !== 'string' || typeof home.buildingId !== 'string' || typeof home.schemeId !== 'string'
        || !home.facts?.hazard || !home.facts?.assessment || !home.facts?.package || !home.facts?.conflict
        || !home.facts?.grants || !home.facts?.invoice || !home.residentUpdate
        || !Array.isArray(home.evidence) || !Array.isArray(home.tasks) || !Array.isArray(home.appointments)) throw new Error('Case/schema mismatch; refusing reset.');
    }
    db.prepare('SELECT case_id,sequence,actor,action,timestamp,payload FROM events LIMIT 1').all();
    db.prepare('SELECT case_id,key,actor,request_hash,response FROM idempotency LIMIT 1').all();
  } catch (error) {
    db.close();
    throw error;
  }

  const getCase = db.prepare('SELECT json FROM cases WHERE id=?');
  const getEvents = db.prepare('SELECT sequence,actor,action,timestamp,payload FROM events WHERE case_id=? ORDER BY sequence');
  const replay = db.prepare('SELECT actor,request_hash,response FROM idempotency WHERE case_id=? AND key=?');
  const putCase = db.prepare('UPDATE cases SET version=?,json=? WHERE id=?');
  const addEvent = db.prepare('INSERT INTO events(case_id,sequence,actor,action,timestamp,payload) VALUES(?,?,?,?,?,?)');
  const addReplay = db.prepare('INSERT INTO idempotency(case_id,key,actor,request_hash,response) VALUES(?,?,?,?,?)');
  const nextSequence = db.prepare('SELECT COALESCE(MAX(sequence),0)+1 AS next FROM events WHERE case_id=?');
  const load = id => {
    const row = getCase.get(id);
    if (!row) throw new AppError(404, 'NOT_FOUND', 'Synthetic case not found.');
    return JSON.parse(row.json);
  };
  const events = id => getEvents.all(id).map(row => ({ ...row, payload: JSON.parse(row.payload) }));
  const detail = (id, role = 'viewer') => {
    validateRole(role);
    return caseView(load(id), role, events(id));
  };
  return {
    dbPath,
    detail,
    list(role = 'viewer') {
      validateRole(role);
      return db.prepare('SELECT id FROM cases ORDER BY id').all().map(row => detail(row.id, role));
    },
    execute(id, role, envelope) {
      validateEnvelope(envelope, role);
      const hash = requestHash(id, role, envelope);
      return transaction(() => {
        // Replay precedes the latest-version check, even after unrelated subsequent writes.
        const previous = replay.get(id, envelope.idempotencyKey);
        if (previous) {
          if (previous.actor !== role || previous.request_hash !== hash) throw new AppError(409, 'IDEMPOTENCY_CONFLICT', 'Idempotency key belongs to a different actor or intent.');
          return { ...JSON.parse(previous.response), replayed: true };
        }
        const home = load(id);
        if (home.version !== envelope.expectedVersion) throw new AppError(409, 'VERSION_CONFLICT', 'Reload current case before a new intent.', home.owner,
          { expectedVersion: envelope.expectedVersion, actualVersion: home.version });
        const timestamp = new Date().toISOString();
        mutate(home, envelope.action, envelope.payload, role, timestamp);
        home.version++;
        putCase.run(home.version, JSON.stringify(home), id);
        fault('after-case-write');
        const auditPayload = envelope.action === 'send_handoff'
          ? { ...envelope.payload, handoffId: home.handoff.id } : envelope.payload;
        addEvent.run(id, nextSequence.get(id).next, role, envelope.action, timestamp, JSON.stringify(auditPayload));
        fault('before-replay-insert');
        const response = { case: caseView(home, role, events(id)), replayed: false };
        addReplay.run(id, envelope.idempotencyKey, role, hash, JSON.stringify(response));
        fault('before-commit');
        return response;
      });
    },
    fallback(id, role, mode) {
      validateRole(role);
      return transaction(() => {
        const home = load(id);
        const existing = home.tasks.find(task => task.kind === 'assistant_manual_review' && task.status === 'open');
        if (existing) return existing;
        const timestamp = new Date().toISOString();
        const task = { id: `EX-MANUAL-${id}`, kind: 'assistant_manual_review', owner: home.owner,
          message: 'Simulator unavailable. Review case evidence manually; no decision has been made.', status: 'open', createdAt: timestamp };
        home.tasks.push(task);
        home.version++;
        putCase.run(home.version, JSON.stringify(home), id);
        fault('after-case-write');
        addEvent.run(id, nextSequence.get(id).next, role, 'assistant_fallback', timestamp, JSON.stringify({ mode, taskId: task.id, owner: task.owner }));
        fault('before-commit');
        return task;
      });
    },
    readiness() {
      try {
        db.exec('BEGIN IMMEDIATE');
        db.prepare("UPDATE metadata SET value=value WHERE key='schema_version'").run();
        db.exec('ROLLBACK');
        return true;
      } catch {
        try { db.exec('ROLLBACK'); } catch { /* Closed/unavailable database is already fail-closed. */ }
        return false;
      }
    },
    close() { if (!closed) { db.close(); closed = true; } },
  };
}
