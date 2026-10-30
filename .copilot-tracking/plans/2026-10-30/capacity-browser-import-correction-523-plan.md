---
title: Capacity browser import correction plan
description: Correction cycle 1 for PR 577, Refs 523
ms.date: 2026-10-30
---

## Task Metadata

Task ID: 523-correction-1. Readiness: validated and reviewed; local commit pending.

## Executive Summary

The reported missing-Playwright discovery failure is reproduced. Defer browser
operations to harness execution, preserve typed annotations, and test scanner
behavior without a browser dependency. No UI, data, dependency or workflow
change is needed. The correction ends with one independent Review and a local
commit, not publication.

### What You May Not Know

The regression executes the scanner assertions with Playwright denied even in a
dev environment that has Playwright installed. This correction does not replace
the inherited publication gates or owner live verification.

## Sources

`.copilot-tracking/research/2026-10-30/capacity-browser-import-correction-523-research.md`,
API project configuration and existing regulatory import-blocker tests.

## User Decisions and Requirements

* Continue `fix/capacity-work-orders-page-523`, PR #577, Refs #523 only.
* Reproduce the report before fixing; use postponed/type-only browser imports
  and browser-independent mocks; add a regression that fails before the fix.
* Execute Research, Plan, Implement and Review with dated tracking artifacts.
* Run full API unit discovery using the exact supplied PYTHONPATH, Ruff check,
  Ruff format check and mypy. Serialize heavy checks with the supplied flock.
* No Azure, sign-in, secrets, uv or push. Commit locally with Copilot trailer.

## Goals

Restore documented browser-free discovery without weakening scanner assertions.

## Scope and Non-Goals

Only capacity harness, its test module, a related README clarification and dated
correction evidence. No UI or application behavior change. Preserve prior
adverse evidence. Full exact-head publication gates remain coordinator-owned.

## Functional Requirements

Harness import and scanner tests must not import Playwright. Browser execution
must import actual APIs and fail explicitly if unavailable.

## Non-Functional Requirements

Keep strict type checking, scanner pin and fail-closed violation checks.
Use existing regression prior art and installed validation tools.

## Acceptance Criteria

* AC1: Fresh-process Playwright blocker reproduces baseline failure.
* AC2: With that blocker, all capacity scanner tests execute and pass, without
  recursive subprocess launching or skips.
* AC3: Browser execution without Playwright fails before starting local server.
* AC4: Requested full discovery, lint, formatting and typing pass.
* AC5: One independent critique and Review are preserved; local commit has
  privacy-safe identity and requested trailer; no push.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct imports and preserve regression coverage

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add isolated browser-free discovery/execution regression; prove red.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Defer operations, retain type-only annotations, replace Page specs.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Clarify README's browser-free contract for capacity.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and review

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run targeted regression and all requested API checks under flock.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile changes/details and obtain one independent Review.

<!-- rpi:task id=P02-T03 -->
#### [ ] P02-T03: Commit locally with required identity and trailer; do not push.

## Test Ownership and Coverage Lock

Canonical test owner: `src/api/tests/test_capacity_browser_check.py`; no generated
targets, no removals, maximum two new tests. Preserve four existing scanner/pin
tests. One fresh subprocess imports the harness/test module with all Playwright
imports denied and runs exactly the four existing scanner tests (not itself).
An additional assertion in that subprocess calls `check` and asserts missing Playwright
before store access, proving execution remains explicit and side-effect-free.
Use `Mock(spec=["evaluate"])`, not a runtime Page. Semantic scanner results stay
covered by existing tests; new tests cover only the dependency boundary.

## Evidence and Dependencies

Research: `research/2026-10-30/capacity-browser-import-correction-523-research.md`.
The existing capacity environment contains pinned Ruff/mypy/Playwright but the
first full run exposed missing Azure SDK packages and incomplete source metadata.
After that actual missing-dependency result, restore current core, agents and
API dev distributions into a new dedicated correction venv with pip. No manifest
change or skip is needed. Commands run from `src/api` using the exact caller
PYTHONPATH and that environment's executables. Full local publication gate is
not requested: no push is authorized.

## Critique Disposition

One independent critique executed, original verdict Revise, PC-001 High.
PC-001 is rejected as inapplicable to the parent execution environment: its
claimed prohibition on `/tmp` operations is not an active parent restriction,
and conflicts with the caller's explicit shared-lock requirement. The parent
will retain the exact requested `flock -w 600 /tmp/ama-rpi-heavy.lock` protocol,
not choose another lock or run unlocked. Actual lock acquisition and outcomes
will be recorded with validation. No user decision or second critique is needed.
Implementation has since acquired that exact shared lock successfully, confirming
the parent disposition. Restored-environment validation passed: 1377 discovered
tests (318 opt-in skips), Ruff, format and mypy. No further critique was run.

## Follow-Up Items

Inherited complete exact-head publication and owner live-verification gates
remain unmet; this bounded correction does not satisfy all issue criteria.

## Handoff

Changes record:
`.copilot-tracking/changes/2026-10-30/capacity-browser-import-correction-523-changes.md`.
P01, P02-T01 and P02-T02 are complete. One independent Review executed Complete /
Conformant, with no source defects and RV-001 retaining inherited publication/live
residuals. P02-T03 remains the authorized local commit. No further source change,
critique or Review is required.
