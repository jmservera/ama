---
title: Employee acceptance gate bootstrap details
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

Task 570-gate-bootstrap, employee-identity-check-570-gate-bootstrap.

<!-- rpi:phase id=P01 -->
## P01: Bootstrap and validate

<!-- rpi:task id=P01-T01 -->
### P01-T01: Bootstrap

In shared chromium helper only, catch BrowserError from launch; the exact
existing missing-executable condition records approved discovery skip and
every other error is reraised. No raw exception output from the maintained
runner. CLI run result must pass, testsRun equal three, skipped empty.
Never change admission or map observer bodies or gate skip allowlist.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Evidence

Actual existing absent-browser reproduction is three launch errors.
After fix, module is successful with three explicitly recorded discovery
skips, but CLI exits one with those same three skips; installed browser CLI
executes three with zero skips. Inject a non-missing launch BrowserError and
prove no skip fallback. Run whole owning module, Ruff/format/mypy/tool tests.
Guide distinguishes allowed discovery from mandatory execution. No methods
added/removed; normal regression semantics remain unchanged.
One independent child Review; prior correction Review is not repeated.
Commit dated originals and redo clean complete gate at fetched current base,
then receipt verification/exact-head assessment before authorized push/PR.
