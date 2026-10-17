---
title: "Issue 84 Correction ONE bounded verification"
description: "Independent closure of RV-001 against the correction content for draft PR 382."
ms.date: 2026-10-17
---

## Verdict

RV-001: Closed for the fingerprinted Correction ONE content below.
No remaining RV-001 blocker or introduced regression was found within this
bounded verification. This is not a second full-task Review, full RPI,
publication approval or human/authority acceptance.

## Boundary and content binding

* Branch: `feat/assessment-reconciliation-controls-84`; draft PR #382.
* Comparison base and observed HEAD:
  `a15c7a20d2dafd6b465433399066410f9124a4da`.
* Reviewed only the correction diff in the three named files, with unchanged
  `stock.decision_scope`, `_SyncLock`, `_finish` and snapshot/sync code read
  as necessary integration context.
* Read the original RV-001 historical two-probe evidence and its new disposition
  notice, plus the top Correction ONE implementation evidence. The original
  Review's negative verdict remains historical and has not been rewritten.
* These are SHA256 fingerprints of complete working-tree files, not claims
  that the correction is already committed at HEAD. Rechecked after testing.
  A final head containing these exact bytes is bound by this verdict;
  changed correction bytes require a new applicability determination.

| Reviewed file | SHA256 |
| --- | --- |
| `src/core/src/zava_forward/core/sqlstore.py` | `f7ff72db069200d23e98f861e250cd688762914eac43d66201f4601d198a56b2` |
| `src/core/tests/test_stock_reconciliation.py` | `1c985dfdf153face379e71d041f7cb8c4e68910b4c6a598fc8d222a4d6562ff2` |
| `src/api/tests/test_mssqlstore.py` | `a6b6a3a432c622fc435a3b9daf513869749894d8f2cc489d70c1dab20674081a` |
| `src/core/src/zava_forward/core/stock.py` (unchanged integration context) | `7c441494bb5723a4975345476bfe6e1f75d5e501eb8256719085e682c33077fc` |

## Resolution against the original defect

| Required property | Independent assessment |
| --- | --- |
| Original error survives an actual first recovery SELECT failure | The new test at `src/core/tests/test_stock_reconciliation.py:464` wraps the real connection and raises before the real recovery SELECT completes. All six technical/comparison/terminal query x first-only/persistent subcases passed with exception object identity preserved. This is not the historical discard-successfully-then-raise oracle. |
| No pending success audit or failed write reaches outer context exit | `src/core/src/zava_forward/core/sqlstore.py:601-606` clears pending, touched and all three validation collections before any DB read. Consequently unchanged `_finish` has neither touched-case reloads nor pending success events to process after failed decision recovery. The new test checks durable case body/rowversion/sequence, database sequence, audit and ledger head after the failed operation has exited, and checks later save/reopen behavior. |
| Recovery uncertainty remains visible | Unchanged `stock.py:32-40` annotates the original exception and emits the standard `zava_forward.core.stock` ERROR log. The six-subcase test verifies both; the constructed probe also independently verified both error paths. Recovery failure is not silently treated as a successful reload. |
| No held lock or stale decision context | The new six-subcase test passed zero-depth and cross-thread acquisition checks for both the request lock and DB lock. The existing scope-exit regression also passed. The constructed probe independently verified restoration of the previous empty decision context. |
| Retry and reopen are correct, including persistent faults | Known committed cases, recommendations and shared documents are restored before recovery reads; `_seq=-1` requires the next lock entry to retry database synchronization. Persistent-fault detail reads fail visibly, not as successful stale reads; clearing the fault allows detail/reopen equality and a legitimate subsequent technical action. |
| Real transactional refusal cannot be replaced by eager recovery | `sqlstore.py:574-578` rolls back and defers discard only when a stock decision owns cleanup. The real-save test at `test_stock_reconciliation.py:580` injects GateError and ConflictError inside transactional validation, with an actual persistent recovery SELECT fault. Both original objects survive; staged writes/events are empty and durable state is unchanged. |
| Canonical ordering does not break relevant existing consumers | The independent 91-test run below passed, including SQL-store and bulk-edit/change-provenance/form-staging regressions. An additional constructed probe checked recommendation and shared-document restoration before a persistent recovery read failure and their absence from a later save. |
| Scope remains bounded | No generic `_SyncLock`/`_finish` change. The two API additions alias the exact canonical new tests in the existing opt-in SQL Server class. No source-stock authority, signoff-role or deterministic-policy changes occur in this correction diff. |

## Commands and results actually executed

All test execution was offline against constructed fixtures. Existing installed
distributions and `.venv` were used. Python's test fixture directory was set to
the repository working directory; fixtures cleaned themselves up.

### Focused regression command

Run from the repository root, exactly:

```bash
PYTHONPATH=src/core/tests .venv/bin/python - <<'PY'
import os
import tempfile
import unittest
tempfile.tempdir = os.getcwd()
names = [
 'test_stock_reconciliation.StockReconciliation.test_sql_early_and_persistent_recovery_reads_cannot_flush_failed_work',
 'test_stock_reconciliation.StockReconciliation.test_sql_transaction_refusal_keeps_original_error_when_reload_fails',
 'test_stock_reconciliation.StockReconciliation.test_sql_recovery_fault_preserves_original_failure',
 'test_stock_reconciliation.StockReconciliation.test_sql_decision_scope_restored_on_every_exit',
 'test_sqlstore', 'test_bulk_edits', 'test_change_provenance', 'test_form_staging',
]
result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromNames(names))
raise SystemExit(not result.wasSuccessful())
PY
```

Result: 91 tests in 21.091 seconds, OK, zero skips. The historical inadequate
recovery test remains present and passed, but is not the basis for closing
the early/persistent recovery defect.

### Independent constructed snapshot probe

Run from the repository root, exactly:

```bash
PYTHONPATH=src/core/tests .venv/bin/python - <<'PY'
import copy
import os
import tempfile
from unittest.mock import patch
from test_stock_reconciliation import StockReconciliation
from zava_forward.core.store import GateError

tempfile.tempdir = os.getcwd()
for error_type in (OSError, GateError):
    case = StockReconciliation()
    case.setUp()
    try:
        store = case.stores()[-1]
        case.tech(store, 'rc1', 'design_submit', note='Constructed committed design')
        store.data['recommendations'].append(dict(id='RV001', user='sam', note='committed'))
        store.data['governance'] = dict(marker='committed')
        store.save()
        before = case.durable_state(store)
        recs = copy.deepcopy(store.data['recommendations'])
        shared = copy.deepcopy(store.data['governance'])
        db = store.db
        original = error_type(['Constructed refusal']) if error_type is GateError else error_type('Constructed precommit error')
        class ReadFailure:
            armed = False
            def execute(self, sql, args=()):
                if self.armed and sql.startswith('SELECT rowversion, body FROM cases'):
                    raise OSError('Constructed actual first recovery SELECT outage')
                return db.execute(sql, args)
            def __getattr__(self, name):
                return getattr(db, name)
        fault = ReadFailure()
        def refuse():
            store.data['recommendations'][-1]['note'] = 'must not persist'
            store.data['recommendations'].append(dict(id='RV001-FAILED', user='sam'))
            store.data['governance']['marker'] = 'must not persist'
            fault.armed = True
            raise original
        with patch.object(store, 'db', fault), patch.object(store, '_validate_safety_clear', side_effect=refuse), case.assertLogs('zava_forward.core.stock', level='ERROR') as logs:
            try:
                case.tech(store, 'rc1', 'design_change', note='Constructed failed design', affects=['design'])
            except Exception as caught:
                assert caught is original, 'original error identity'
            else:
                raise AssertionError('Failed operation returned success')
            assert 'SQL recovery failed' in ' '.join(logs.output), 'standard error log'
            assert original.__notes__, 'original error recovery note'
            assert store.local.pending == [] and store.local.touched == set(), 'disarmed writes'
            assert store.local.safety_clear == set() and store.local.resident_clear == [] and store.local.stock_clear == set(), 'disarmed validations'
            assert store.local.stock_decision is None and store.lock.depth == 0, 'context exit'
            assert store._seq == -1, 'retry required'
            assert store.data['recommendations'] == recs, 'cached recommendation restore'
            assert store.data['governance'] == shared, 'cached shared restore'
            assert case.durable_state(store) == before, 'durable failure state'
        store.save()
        reopened = case.reopen(store)
        after = case.durable_state(reopened)
        assert (after[0], after[2], after[3]) == (before[0], before[2], before[3]), 'no delayed case/audit write'
        assert after[1] == before[1] + 1, 'existing explicit no-op save sequence increment'
        assert reopened.data['recommendations'] == recs, 'no delayed recommendation write'
        assert reopened.data['governance'] == shared, 'no delayed shared write'
        assert store.detail('ZF-3') == reopened.detail('ZF-3'), 'next read/reopen equality'
        print(error_type.__name__ + ': persistent actual recovery SELECT fault, snapshot restore and no delayed case/rec/shared/audit write PASS')
    finally:
        case.doCleanups()
PY
```

Result: OSError and GateError probes both PASS. Actual save/rollback, discard,
outer exit and database reopen are used; the fault precedes recovery SELECT
completion. A prior version of this same probe failed its final whole-tuple
equality assertion after an explicitly requested plain `save()`. Inspection
confirmed existing `save()` always increments meta sequence, even with no case
changes. The corrected oracle above requires unchanged case rowversion/body/seq,
audit/head, recommendation and shared state, while explicitly allowing exactly
that existing meta increment. It passed without source changes. The failed
initial probe is not counted as passing evidence or an introduced defect.

### Content and whitespace checks

```bash
sha256sum src/core/src/zava_forward/core/sqlstore.py src/core/tests/test_stock_reconciliation.py src/api/tests/test_mssqlstore.py src/core/src/zava_forward/core/stock.py
git --no-pager diff --check HEAD -- src/core/src/zava_forward/core/sqlstore.py src/core/tests/test_stock_reconciliation.py src/api/tests/test_mssqlstore.py
```

Fingerprints matched on both reads; correction diff whitespace check passed.

## Supplied evidence and limitations

* The Correction ONE ledger supplies fail-before evidence for the six new
  early/persistent subcases and two transaction-refusal subcases; subsequent
  102 focused core, 69 discard-consumer and 72 targeted API tests (one existing
  browser skip), core/API Ruff/format/mypy passes, and ten actual cached-image
  task-local SQL Server passes including the new tests.
* Those supplied runs were read, not independently rerun or promoted to fresh
  evidence here. No SQL Server/container command was executed by this
  verification. The recorded removal of the task-owned container and
  preservation of the other task's container are supplied execution evidence.
* No full suites, cloud, AI/provider calls, private datasets, broad audits,
  agents, full RPI/review activation, architecture demands or new policy
  decisions were undertaken. No new lint/type/browser/accessibility acceptance
  is claimed beyond the supplied evidence.
* Closure concerns known precommit failures and the specified actual recovery
  SELECT faults. It does not establish lost commit acknowledgement guarantees,
  rollback after unknown commit outcome, every possible database/rollback or
  process-crash failure, or JSON cross-file crash atomicity.
* No professional competence, resident consent, source authority, policy,
  legal/compliance, human approval or deployment acceptance is granted.
  Previously recorded genuine residuals remain outside this correction.
* Only this verification record is authored. Original review, source,
  plan, documentation and lifecycle state remain untouched by this invocation.
  No commit, push, merge or acceptance-state mutation was performed.

Bounded verification complete. RV-001 Closed; no blocker in the assessed
correction. Stop after this one verification.
