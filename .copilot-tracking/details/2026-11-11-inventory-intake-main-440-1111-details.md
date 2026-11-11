---
title: Inventory and staff intake current-main checkpoint details (Refs 440, 131, 132, 1362)
ms.date: 2026-11-11
task_id: 440-inventory-intake-main-1111
---

## Commands (from the worktree root unless stated; `V=/tmp/ama-440-inventory-venv-1111`)

| Id | Command | Pass criterion |
| --- | --- | --- |
| P1 | `python3 -m venv $V`; `$V/bin/python -m pip install -e src/core -e src/agents -e src/api`; module-origin print for `zava_forward.core`, `.agents`, `.api` and `checks` | exit 0; every origin under this worktree |
| O1 | `cd src/core && PYTHONPATH=tests $V/bin/python -m unittest tests.test_resident_decisions -k inventory -v` | exit 0; JSON and SQLite inventory cases ok; MSSQL opt-in cases counted as skipped, not passed |
| O2 | `cd src/core && PYTHONPATH=tests $V/bin/python -m unittest tests.test_resident_decisions.JsonResidentDecisions.test_resident_acceptance_never_clears_technical_or_hazard_gates tests.test_resident_decisions.JsonResidentDecisions.test_quality_dependencies_are_scoped_and_unknown_evidence_cannot_release -v` | exit 0 |
| O3 | `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests $V/bin/python -m unittest tests.test_resident_api -k inventory -v` | exit 0; skips counted |
| O4 | `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests $V/bin/python -m unittest tests.test_staff_intake_api -v` | exit 0; MSSQL class skips counted |
| O5 | `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests $V/bin/python -m unittest tests.test_role_endpoint_inventory tests.test_content_standard -v` | exit 0 |
| O6a | `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests $V/bin/python -m unittest tests.test_atlas_tensions_checker -v` without `ZF_BROWSER_TESTS`; it imports Playwright, a declared dev dependency (`playwright==1.64.0`), so an import failure is recorded and only then restored into the private venv | exit 0; browser skips not accepted as evidence |
| O6b | `cd src/api && ZF_BROWSER_TESTS=1 ZF_BROWSER_SCRATCH=/tmp/z440inv PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests flock -n /tmp/ama-rpi-heavy.lock timeout 900 $V/bin/python -m unittest tests.test_atlas_tensions_checker -v` | run only if the lock is free and memory allows; otherwise blocked |
| O7 | `cd src/api && ... -m unittest tests.test_staff_intake_browser` | not run: needs `ZF_STAFF_INTAKE_BROWSER=1` and pinned `ZF_AXE_PATH`; absent, not installed; recorded blocked |
| D1 | `git diff --check`; relative link and anchor review of the touched documents | exit 0; no broken link |

`PYTHONPATH` carries only the existing test-helper directories documented in `src/README.md`; it is not a source workaround and the origin print in P1 proves the source packages come from the editable installs.

## Environment rules

No `ZF_DATA`, `.env`, credential, provider, Azure or production variable. `HOME/.zava-forward` is checked absent before and after. No global or shared install. Raw output goes outside the repository. Counts are taken from the actual unittest summary lines: run, skipped, failures and errors.

## Trace table to fill

Requirement (document-qualified) to decision to code to test to observation to class (local observed, Azure observed, implemented unverified, deferred, blocked, unknown) to remaining owner. Rows: BRD FR-015 and AC-021 (tenure); PRD FR-015 with AC-018 and AC-038 (hazard, a separate requirement that the household hold does not satisfy); BRD FR-016 and FR-017 context; PRD FR-016 and FR-017 (partial); ADR 0007 (proposed); issue 131 and 132 criteria as stated, not ticked; the combined QA guard row is classified implemented but unverified at combined level unless an existing selector proves it.

## Reporting rules

State sample limits: caller-declared inventory, constructed synthetic cases, one JSON staff intake class, SQLite as a store double and not MSSQL. State no new defect or necessary refactor unless a failure reproduces. Original RPI marker and authoring qualifications of the merged PRs stay historical; a local witness exit 0 is not strict chronology attestation.
