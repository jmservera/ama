---
title: Case journey checklist findings later implementation
description: Routed RV-001 and RV-002 changes and tests, not repeated Review
ms.date: 2026-10-28
---

## Invocation

Full later findings plan P01; first dependency-ready task P01-T01.
Original independent Review remains Complete / Not accepted, unchanged.
Existing user seven-root-fix instruction covers these narrowly coupled
implementation defects. No new design or authority decision.

## Execution and Validation

P01-T01/T02 complete. No new critique or Review.
No remote writes or prohibited gate execution.

## P01-T01 Root Repairs

RV-001: the shared field-entry boundary now deduplicates semantic keys with
actual-control precedence in either DOM order. Every measure paint removes and
reconstructs that checklist's recovery block, so a now-live identity has no stale
recovery copy left to overwrite it. Missing measure/version snapshots remain in
the session cache.

RV-002: quality cleanup uses precisely measure, scope revision, submitter,
source and current checklist inputs. Read-only recovery is not represented in
the request and is never marked submitted. Explicit discard remains distinct.
No journey, approval, endpoint, domain or schema change.

## P01-T02 Actual Validation

Same external evidence root as the correction changes artifact.
Final source/test/guide diff against d3fbba58:
SHA-256 `20b79ed6e234cfc904e040ab5505dbe87068dc23cb8049cade63a20420cd0ea3`.

* Four modified JavaScript files pass node --check.
* From src/api, repository .venv `ruff check .` and `ruff format --check .`
  pass; 48 formatted files. All newly added Python lines separately checked
  at <=100 columns.
* `../../.venv/bin/python -m mypy`: success, 94 source files.
* `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m
  unittest test_case_journey test_design_system test_content_standard
  test_handoff_api test_ui_support -q`: exit 0, 41 tests, no skips,
  10.140 seconds (`findings-unit.log`). New Node-backed unit verifies that live
  identity wins over stale recovery in either DOM order.
* Same interpreter/PYTHONPATH, `-m checks.case_journey_browser_check --axe
  <evidence-root>/axe-4.10.3.min.js --out <evidence-root>/journey-10`:
  exit 0, 147 assertions, Chromium 156.0.8078.4, pinned/hash-verified
  axe 4.10.3, 38 scans, zero violations/page errors. Exact later transitions
  pass: A -> B -> refresh -> A -> edit -> refresh; save B while A recovery is
  present; save current checklist while prior-version recovery is present;
  both recoveries remain dirty through another refresh.
* Same interpreter/PYTHONPATH, `-m checks.assistants_browser_check`: exit 0,
  30 checks (`assistants-03.log`). Overlap/source-verification and original
  approval/route/timeout checks still pass.

Browsers admitted 2026-10-28T21:58:21Z using the same nonblocking shared flock,
15-second retries and 2400-second deadline; lock released after suites finish.
Only quality success is intercepted in the added cleanup checks, explicitly to
exercise client payload/cleanup ownership. It is not actual quality acceptance
or a domain approval claim. Existing real synthetic upload/handoff/document and
assistant operations remain. No billable model, Azure or retained data access.

## Original Outcome and Publication Boundary

Original Review remains Complete / Not accepted at its original eight-file
diff. RV-001/RV-002 have later implementation and regression evidence here, not
independently verified closure. Do not edit that Review or run it again.
Original broader API results (1158/314 skips; affected 212/51 skips) remain
historical; latest directly affected final checks are the 41 no-skip tests above.

Fresh fetch: origin/main now 1dde6a908c20358dbb3067dcdd674e5ad0bd246d.
Topic upstream remains d3fbba58, zero ahead/behind before this local commit.
Initial required pull --ff-only already reported up to date; no new bot commit
requires another pull. No merge, rebase or force operation.
P01-T03 local commit pending. Full gate invokes prohibited az; no receipt,
current-main/exact-head independent acceptance, push or thread resolution.
