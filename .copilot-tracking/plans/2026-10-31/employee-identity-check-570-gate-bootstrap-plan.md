---
title: Employee acceptance gate bootstrap plan
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

Task 570-gate-bootstrap, employee-identity-check-570-gate-bootstrap.
Parent completed employee-identity-check-570-correction. Automatic.

## Executive Summary

Narrowly reuse existing missing-Chromium discovery handling, while requiring
all three actual Chromium executions in CLI and integration extras. This fixes
fresh full-gate sequencing without changing runtime admission/render behavior,
the gate matrix or browser prerequisite requirements. Original Reviews retained.

## Sources

Bootstrap research C1-C6; owner complete-gate/no-bypass requirement; owning
browser asset test and gate's existing discovery/integration distinction.

## User Decisions and Requirements

* Complete the current-base gate with actual required validation before push/PR.
* No skip-based passing receipt, cloud fallback, secret or Azure changes; pip only.
* Preserve original correction findings/Reviews and unmet live criterion.

## Goals

Make general discovery compatible with fresh browser setup; missing Chromium
must still fail required CLI/extras. No success-shaped skip fallback.

## Scope and Non-Goals

Only owning acceptance test's launch bootstrap, runner CLI result reduction,
API owning guide and dated new child evidence. No BINDING/observer edits,
gate-tool/matrix/CI modifications, browser installation, new test module or
method, private identity/credential/sign-in handling.

## Functional Requirements

Use existing narrow BrowserError "Executable doesn't exist" handling with
exact approved reason "Chromium is installed by the later browser-check step".
All other launch errors propagate. Record allowed discovery skips explicitly.
CLI success requires wasSuccessful, exactly three testsRun and zero skipped.
Integration extras already reject any skips; do not change that contract.

## Non-Functional Requirements

Keep required Chromium installs/execution under gate ownership.
No writes into a running gate/output, no reused historical receipt.
Any new commit/base requires new clean complete gate and exact-head assessment.

## Acceptance Criteria

* Absent-browser module discovery records three known skips rather than errors.
* Same absent-browser CLI fails nonzero (never counted as executed acceptance).
* Installed-browser module and CLI execute/pass all three Chromium methods.
* Non-missing launch failure propagates, not skipped; identity/render source
  hashes stay unchanged apart from CLI reduction.
* Ruff/mypy/gate-tool tests pass; one independent child Review and fresh full
  gate/receipt/current-base assessment precede publication.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Bootstrap and validate

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Narrow discovery skip and strict CLI execution

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate missing/present/error paths and document distinction

## Locked Test Ownership

Owning test module src/api/tests/test_employee_acceptance_check.py.
Exact removals none; maximum additions zero methods. Canonical runner/test/
guide, no generated targets. Semantic coverage: actual missing-browser
reproduction and strict CLI exit, actual installed browser; regression:
unchanged original admission/map tests. Validate with same installed pip venv,
unittest module, CLI, absent PLAYWRIGHT_BROWSERS_PATH CLI/module, narrow injected
non-missing BrowserError, Ruff/format/mypy, tools/test_rpi_checks.py.
Complete gate retains all three original explicit Chromium extra selectors.

## Critique Disposition

Exactly one independent critique Complete / Pass, zero findings; original
artifact retained at .copilot-tracking/reviews/plans/2026-10-31/employee-identity-check-570-gate-bootstrap-plan-critique.md.
Implementation readiness Ready; no direct revision or user decision needed.

## Follow-Up Items

Independent identity/live criterion and hosted/owner approvals remain outside
local bootstrap completion. Prior aa531930 full-gate attempt is historical
and unchanged; no assumed success.

## Handoff

Parent applies one critique disposition before Implement. Changes:
.copilot-tracking/changes/2026-10-31/employee-identity-check-570-gate-bootstrap-changes.md.
