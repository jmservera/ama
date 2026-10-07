import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { config } from '../src/domain.mjs';
import { seedCases } from '../src/seed.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
test('versioned manifest maps all fixed workflows to real fixtures/actions/endpoints/test oracles', () => {
  const manifest = JSON.parse(readFileSync(resolve(appRoot, 'manifest.json'), 'utf8'));
  assert.equal(manifest.version, 'poc-1');
  assert.equal(manifest.workflows.length, 9);
  assert.deepEqual(manifest.workflows.map(item => item.id), config.workflows.map(item => item.id));
  const cases = seedCases();
  for (const workflow of manifest.workflows) {
    assert.ok(cases.some(home => home.id === workflow.fixture && home.workflow === workflow.id));
    assert.ok(workflow.actions.every(action => config.commands.some(command => command.action === action)));
    assert.ok(workflow.expectedEndpoints.includes(`GET /api/cases?workflow=${workflow.id}`));
    assert.equal(workflow.coverage, 'partial');
    for (const reference of workflow.tests) {
      const [path, name] = reference.split(': ');
      const absolute = resolve(appRoot, ...path.split('/'));
      assert.ok(existsSync(absolute), path);
      if (name) assert.ok(readFileSync(absolute, 'utf8').includes(name), reference);
    }
  }
  assert.deepEqual(manifest.pairedHomes.homes, ['EX-HOME-208', 'EX-HOME-317']);
  assert.ok(manifest.prdCoverage.deferred.some(item => item.includes('Claimable')));
  assert.equal(manifest.assistant.externalCalls, 0);
});
