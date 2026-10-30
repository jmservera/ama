---
title: Resident showcase batch selection changes
description: Implementation and command evidence for the PR 590 correction
ms.date: 2026-10-30
---

## Scope and Status

Task 521-pr590-batch-selection; full plan P01. Refs #521, PR 590.
Implementation complete. Source boundary: one test file, no production changes.
No Azure access, push, deployment or issue closure.

## Plan and Critique

Plan: .copilot-tracking/plans/2026-10-30/resident-showcase-batch-selection-plan.md.
Details: .copilot-tracking/details/2026-10-30/resident-showcase-batch-selection-phase-details.md.
One independent critique: original Revise preserved; PC-001 applied with an
explicit executable negative oracle; PC-002 rejected because its claimed path
prohibition is absent from parent instructions and conflicts with the user's lock.
No second critique, material divergence or unresolved user decision.

## Baseline and Prerequisites

Working directory src/core. Initial system commands:
`python3 -m unittest discover -s tests -p test_resident_showcase_sql.py -q`
failed import with ModuleNotFoundError: zava_forward (exit 1).
`ruff check tests/test_resident_showcase_sql.py` failed: command not found (127).
No installation: the existing pinned external venv is usable.

Baseline commands from src/core, all exit 0:

```bash
/tmp/ama-521-validation-20261030/venv/bin/python -m unittest discover -s tests -p test_resident_showcase_sql.py -q
/tmp/ama-521-validation-20261030/venv/bin/ruff check tests/test_resident_showcase_sql.py
/tmp/ama-521-validation-20261030/venv/bin/ruff format --check tests/test_resident_showcase_sql.py
```

Baseline: 38 tests, 11 executed and 27 skipped (opt-in loopback SQL Server).
Ruff check passed; one file already formatted. No heavy run or lock needed.

## P01-T01: Source Changes

Added private typed `_view_batch()` with exact marker selection and single-match
unpacking. Both rebuild and cleanup now call it. Full-file inspection found no
other fixed-index renderer selections. Two always-run RenderTests cover every
view position plus absent/ambiguous matches. The existing empty-table query now
requires sensor_home_id HOME-A together with `[]`, rejecting the NULL fallback
while retaining genuinely empty tables and all reader assertions.
P01-T01 complete; no tests removed, no generated or production target changed.

## P01-T02: Validation

Final commands from src/core, all exit 0:

```bash
env -u ZF_TEST_MSSQL /tmp/ama-521-validation-20261030/venv/bin/python -m unittest discover -s tests -p test_resident_showcase_sql.py -v
/tmp/ama-521-validation-20261030/venv/bin/ruff check tests/test_resident_showcase_sql.py
/tmp/ama-521-validation-20261030/venv/bin/ruff format --check tests/test_resident_showcase_sql.py
```

40 discovered, 13 executed and passing, 27 skipped with reason
`opt-in loopback SQL Server`. Ruff: All checks passed; one file already formatted.
The refusal-test stderr (`--apply needs --create-principal or --client-id...`)
is expected; no apply, CLI login, connection or Azure command occurred.
`git diff --check` from repository root also passed, exit 0.
Only one changed Python file exists, and both Ruff commands cover it.

### Executable negative experiment

This exact in-memory experiment was run from src/core, exit 0. SQL fixture
methods and query results were mocked; no database was accessed. The actual
affected test method was called directly so class-level SQL skip handling could
not produce a false pass.

```bash
env -u ZF_TEST_MSSQL PYTHONPATH=tests /tmp/ama-521-validation-20261030/venv/bin/python - <<'PY'
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch
import test_resident_showcase_sql as t

method = 'test_empty_sensor_tables_preserve_valid_empty_history'
case = t.SqlBoundaryTests(method)
case.add_case = Mock()
case.q = Mock()
row = SimpleNamespace(sensors=())
case.reader = SimpleNamespace(list_rows=lambda: [row], fetch_case=lambda _: row)
case.as_user = Mock(return_value=[('HOME-A', '[]')])
view = t._view_batch()
getattr(case, method)()
assert case.q.call_args.args == (view,)
print('PASS: actual empty-table test method, simulated projected HOME-A/[]')
[migration] = [batch for batch in t.script.render(t.USER) if 'DROP CONSTRAINT' in batch]
with patch.object(t, '_view_batch', return_value=migration):
    case.as_user.return_value = [(None, '[]')]
    try:
        getattr(case, method)()
    except AssertionError as error:
        assert 'HOME-A' in str(error), str(error)
        print('EXPECTED FAILURE: wrong migration batch / NULL fallback rejected by actual method')
    else:
        raise AssertionError('The wrong-batch fallback incorrectly passed')
case.as_user.return_value = [('HOME-A', '[]')]
getattr(case, method)()
assert case.q.call_args.args == (view,)
print('PASS: restored actual method with simulated projection')
with patch.object(t, '_view_batch', side_effect=lambda: t.script.render(t.USER)[2]):
    suite = unittest.TestSuite([t.RenderTests('test_view_batch_selection_is_independent_of_batch_order')])
    result = unittest.TestResult()
    suite.run(result)
    assert result.failures and not result.errors, (result.failures, result.errors)
    print(f'EXPECTED FAILURE: old index selector rejected ({len(result.failures)} relocation subtests)')
result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(t.RenderTests))
assert result.wasSuccessful()
print('PASS: restored RenderTests; all mutations were in-memory patches')
PY
```

Results: projected baseline pass; wrong migration/NULL fallback expected
AssertionError; restored actual method pass; old-index helper rejected by six
relocation subtests; restored eight RenderTests pass. Mutations never touched
source files. PC-001's failure oracle was exercised without hiding behind skips.
Final file discovery and Ruff commands above ran in parallel with this separate
process; all mutations were process-local mocks.

No heavy runs were performed, so no heavy lock was taken. Real SQL and complete
local publication gate were not run or claimed. P01-T02 complete.

## Amendments, Divergences and Follow-Up

None beyond critique dispositions above. No publication claim or full-gate
receipt: the user requested a small local-only test correction, not publication.
Independent Review executed once: Complete / Conformant, no findings, recorded at
.copilot-tracking/reviews/logs/2026-10-30/resident-showcase-batch-selection-review.md.
This parent closeout does not modify the original Review or rerun it.

Implementation handoff: plan markers/details, evidence and limits reconciled.
No unfinished implementation, material divergence or source follow-up.
Local commit includes this original evidence and the independent Review.
No push is authorized or performed; no whole-issue acceptance is claimed.
