---
title: Resident demo authority extension changes
description: Implementation and validation evidence for issue 521
ms.date: 2026-10-28
---

## Execution Boundary

Task 521, full source-only plan in scope. P01-T01 active.
Research executed; plan Ready after direct PC-001/002/003 dispositions.
Original critique Revise retained. No Azure, az, secrets or .env access.
Live apply pending exact owner confirmation. Full gate/publication blocked by
required az preflight; no substitute receipt or protection change permitted.

## Changes and Validation

P01-T01: updated packaged JSON to 2027-02-01T00:00:00Z. Existing runtime,
Bicep and secret/deploy aliases share it. SQL renderer substitutes the policy
into both fresh-table and checked transactional existing-constraint migration.
No row renewal, grants, resource, role or network/minimum change.

P01-T02: updated core config and infra secret/deploy boundary checks. Added
five methods: core old-cutoff admission, SQL rendering, SQL legacy/reapply,
SQL rollback and real-loopback HTTP/session boundary. No removals; within
eight-method maximum. Independent inference cutoff unchanged.

P02-T01: updated infra/API guides, index and append-only knowledge log.
Historical renewal retained, new prospective #521 section documents rotation,
unchanged Modify refusal, explicit SQL row approvals, conditional January
USD15.50 plus USD10 reserve and USD700 all-in cost gate. Live apply Pending.

## Validation Admission Blocker

Before any heavy run, `lslocks --noheadings --output PID,COMMAND,PATH`
reported PID 3991262 (`python3`) holding `/tmp/ama-rpi-heavy.lock`.
`ps -p 3991262 -o pid=,comm=` confirmed it exists. No foreign output was
inspected, no process interrupted, no waiting/duplicate heavy run started,
and no lock polling/retry is authorized absent a later coordination event.

`python3 -c 'from zava_forward.core import resident_showcase; ...'` failed
with ModuleNotFoundError before setup. Namespace pip installation and the
dependent planned core/API/infra suites, SQL/browser tests and lint/types
are therefore Blocked by heavy admission, not passed or replaced by mocks.
Ruff/mypy are also absent in the current interpreter. No uv used.

Full publication gate is independently Blocked: tools/rpi-checks.py preflight
invokes `az bicep version`, prohibited even offline by caller. Do not run
--all, fabricate a receipt or push to obtain hosted checks.
Lightweight static and tool-only checks may proceed independently.

## P02-T02 Actual Lightweight Results

* `git diff --check`: exit 0.
* AST parse of all changed Python, JSON parse and cost arithmetic: exit 0.
* Initial all-file line-length probe failed on pre-existing renderer line 51;
  narrowed to added lines to avoid unrelated formatting changes. The next
  added-line probe found one new SQL-test line >100 columns; wrapped before
  Review. Final added-line/link probe recorded below.
* `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools
  -p test_check_demo_feedback.py -q`: exit 1, import failed because the
  zava_forward namespace is absent. The chained climate test did not run.
* `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tools python3 -m unittest -q
  test_rpi_checks.GateTests.test_missing_tools_and_dependencies_block
  test_rpi_checks.GateTests.test_unexpected_skip_blocks_but_declared_discovery_skip_is_recorded
  test_rpi_checks.GateTests.test_base_movement_invalidates
  test_rpi_checks.GateTests.test_dirty_tracked_untracked_and_ignored_inputs_block
  test_rpi_checks.GateTests.test_sql_dependency_manifests_select_the_real_consumer
  test_climate_paired_blocker`: exit 0, 8 tests, 1.347 seconds, no skips.
  Printed missing-tool errors are expected fixtures inside the passing
  refusal contract test, not a full-gate execution.

Source identity: initial HEAD/base
413ccaf253fce4566e855bae9d0a924b2a82b506; branch
chore/resident-authority-extension-521; Python 3.12.3, pip 26.2.1.
No compiled Bicep, runtime package, browser or real-SQL result is claimed.

## Implementation Handoff

P01 and P02-T01 authored. P02-T02 remains Blocked for required package/
heavy validation; this explicitly incomplete candidate is ready for original
independent Review assessment, not acceptance/publication. No source changes
are planned after that one Review. Route findings to later work, retain
original outcomes, commit source/evidence, and leave gated push/PR pending.

## Parent Closeout After Original Review

Final changed-file AST/JSON, added Python line lengths, added relative-link
targets and `git diff --check` all passed (exit 0). These are lightweight
static checks, not Ruff/mypy, runtime or SQL substitutes.
Original independent Review executed once: Complete / Residual work,
acceptance withheld. RV-001 High routes missing validation to later
rpi-implement; RV-002 High retains publication follow-up; RV-003 Medium
retains owner-approved live renewal/funding follow-up. No source defect was
established and no source changes or repeated Review followed the assessment.

Commit source and dated evidence locally on the named topic branch using
the authenticated GitHub noreply identity. Full gate, current-base receipt
verification, independent exact-head publication assessment, push and PR
remain blocked; none is claimed completed. Eventual PR must use Refs #521
only because the live acceptance criterion remains pending.
