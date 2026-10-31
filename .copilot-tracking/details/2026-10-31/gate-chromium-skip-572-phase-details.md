---
title: Chromium skip gate phase details
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 572
* Task slug: gate-chromium-skip-572
* Related plan: .copilot-tracking/plans/2026-10-31/gate-chromium-skip-572-plan.md
* Evidence: .copilot-tracking/research/2026-10-31/gate-chromium-skip-572-research.md, C1-C7.

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Bounded recognition | Complete | P01-T01, P01-T02 |
| P02 | Validation | Complete | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Bounded recognition

Preserve the existing owned browser-stage dispatch, which already supplies the
chat opt-in flag after installation. Do not move installation into discovery or
duplicate browser execution. No workflows or browser behavior changes.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Enumerate reasons and preserve chat scope

Add `opt-in local Chromium` and
`Chromium is installed by the later browser-check step` to EXPECTED_SKIP_REASONS.
Refactor the parser predicate so membership never bypasses the existing
CHAT_PANEL_DISCOVERY_SKIP exact test/group restriction. Integration rejection
remains independent of membership and permits only existing SQL_NOT_APPLICABLE.
Completion evidence: unchanged chat negative tests and new asset positive/negative tests.
Dependencies: one final-candidate critique; no unresolved design choice.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Parser, receipt and documentation regressions

Change existing chat assertion from non-membership to membership; retain all
existing rejection cases and dispatch/receipt regressions. Add at most two test
methods, using a real verbose test ID and mixed pass/skip summary for asset
discovery. Assert exact tests/executed/skips output; reject prefix/suffix/case
variants, unknown reasons, integration mode and inconsistent skip totals.
Exercise project-api receipt recomputation with the new asset reason and reject
tampered skip evidence, following the existing chat receipt fixture pattern.
Update src/README.md near the local gate discovery contract, stating that
recognition is not execution and dedicated integration skips still block.
Dependencies: P01-T01. No test removals, generated targets or semantic claims.

<!-- rpi:phase id=P02 -->
## P02: Validation and handoff

Only requested focused commands run. Full gate and actual Chromium/MSSQL
execution are explicitly excluded, not replaced by synthetic successes.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run checks and reconcile evidence

Run under `flock -w 600 /tmp/ama-rpi-heavy.lock`:

```bash
python3 -m unittest discover -s tools -p test_rpi_checks.py
ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 tools/rpi-checks.py tools/test_rpi_checks.py
ruff format --isolated --line-length 100 --check tools/rpi-checks.py tools/test_rpi_checks.py
mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py
```

Restore missing dependencies with pip only after an actual failure. Keep logs
in the external session workspace and record results in changes evidence.
Confirm the pinned workflow hash is unchanged, reconcile plan markers/details
and changes, then hand off for exactly one independent Review. Commit locally
after review evidence is recorded; do not push or claim publication readiness.

Completion evidence: all four requested commands passed on 2026-10-31 under
the shared lock, including 37 unit tests, two already formatted files and strict
mypy with no issues. Changes record owns the original result summary and limits.
