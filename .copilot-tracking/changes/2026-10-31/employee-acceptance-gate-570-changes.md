---
title: Employee acceptance browser gate changes for 570
description: Original implementation evidence for the mandatory acceptance CLI
ms.date: 2026-10-31
---

## Metadata

Task ID: 570-employee-acceptance-gate. Slug: employee-acceptance-gate-570.
Plan: .copilot-tracking/plans/2026-10-31/employee-acceptance-gate-570-plan.md.
Details: .copilot-tracking/details/2026-10-31/employee-acceptance-gate-570-phase-details.md.
Date: 2026-10-31.

## Execution Status

Complete, full implementation plan. P01, P01-T01, P01-T02 and P02-T01 complete;
P02 validation/Review handoff complete. No remaining implementation markers.
Independent critique Complete/Pass, no findings.
Write scope: runner, owning tests, direct docs/index/log and original evidence.

## Validation Intent

Requested tools unittest discovery, owning Ruff/format/mypy and diff review.
No new dependencies. No application/private data, credentials or cloud access.

## Amendments and Divergences

No material divergences. The existing full-receipt suite cardinality assertion
is updated from nine to ten for the newly mandatory suite; this is directly
coupled fixture maintenance within P01-T02, not new coverage or scope.
P02 wording now explicitly marks validation and preparation of independent
Review, not the still-pending lifecycle Review itself. Intent, criteria,
dependencies and original critique remain unchanged.

## Completed Work

### P01-T01: Mandatory command and bounded suite results

tools/rpi-checks.py now dispatches the exact employee CLI immediately after
Chromium installation and requires it in the trusted receipt matrix. Shared
module/path constants keep both identities aligned. Both parsers use optional
expected_count=3 to exclude all skips, including SQL non-applicability, from
this suite. Existing chat-panel/discovery/SQL defaults are unchanged.

### P01-T02: Regression coverage and direct guides

Three new tools test methods cover default/no-extra dispatch and ordering,
receipt identity/flags/exit/count/skip mutations, and runtime count/skip failures.
Both existing receipt builders now supply three-test success; the full fixture
also asserts one CLI in its default matrix. Gate guide and knowledge index/log
record the exact paths and synthetic evidence limits.

## Validation Record

Initial requested run: 42 tests, one directly coupled fixture assertion failure
(expected nine mandatory suites; now ten). Initial Ruff check: one 101-character
test method signature, shortened. Both corrections applied before rerun.

Requested command rerun:
`python3 -m unittest discover -s tools -p 'test_rpi_checks.py' -q`,
exit 0, 42 tests / zero outer suite skips, 13.647 seconds. External session log:
/home/azureuser/.copilot/session-state/3b4d4815-0956-4fd4-bd2b-c4e7dc1e71d5/files/employee-acceptance-gate-unit-final.log.
Fixture-generated negative outputs are intentional tests, not gate acceptance.

Owning isolated Ruff check passed. Format check initially identified two
formatter-only changes; existing formatter applied to the two owning files.
Post-format Ruff and strict mypy passed (two source files).
Git diff whitespace check passed.

Regression sensitivity: loaded original HEAD:tools/rpi-checks.py as inert
source into the test process and ran the new default dispatch test.
Exactly one assertion failure, no errors: missing CLI, 0 != 1. Wrapper exit 0
asserted that exact expected failure. This proves the test detects the omission,
not merely that the amended gate's synthetic success fixture passes.

## Pre-Review Reconciliation

Plan/details markers, changes, validation and handoff reconciled.
Ready for one independent post-implementation Review; no implementation blockers.
No live employee, hosted CI or human approval inferred. Publication evidence separate.
