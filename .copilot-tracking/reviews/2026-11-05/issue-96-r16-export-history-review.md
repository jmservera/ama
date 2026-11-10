---
title: Issue 96 r16 export review-history Review
description: Canonical rpi-review record for the history-in-Held-export increment, written after implementation
ms.date: 2026-11-05
---

## Provenance and chronology

This Review was run in a later turn (after 23:52Z on 2026-11-05) with the rpi-review skill. It was NOT run at the time of the r16 implementation (about 23:31Z). The "Self-review" section in the r16 changes record is author narrative only and is preserved unchanged; it is not a canonical Review.

## Boundary

* Branch `feat/form-export-review-history-96`, head `2c1e460acb9e44011c41bc26dc5d7c14e9ce49ac`, tree `b1d796d4bfbb1e3715521cfa6334b78c26325a9b`, clean including ignored files (checked at review start).
* Target `feat/finance-integration-93` at `0472fd5d5625bb610b5ac65ad177026953802830`; main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (last guard, not re-fetched).
* Diff vs target: 3 files, 63 insertions, 1 deletion (`form_export.py` +2, `test_form_export.py` +54, `src/core/README.md` +7/-1).
* Compared: r16 research, plan/details, changes record, r15 paused records, ninth checkpoint (pinned governance object `1faadaa3`), both owner answers.

## Execution and outcome

* Execution: Complete for the read-only static review plus the evidence below. No new test run (source unchanged since the observed runs).
* Outcome: Conformant for the bounded increment within light-tier evidence. This is NOT a whole-RPI, issue, FULL-tier or publication Pass.

## Evidence consumed

Author-observed results from this session's actual tool output (not the root's re-read of the log):

* RED against an unchanged-source `git archive` copy, import path proved as `/tmp/g96-r16-red2/zava_forward/core/form_export.py`: exit 1, `Ran 9 tests`, 3 errors, all in the two new tests (`test_form_export`). A first RED attempt failed on a bad `cp` path before any test ran. The root separately reports the errors as KeyError; the author output shows only the test names and counts.
* GREEN: `test_form_dependencies test_form_review test_form_export test_form_staging`, exit 0, `Ran 59 tests`, OK (19.530s), import path proved from this worktree.
* Ruff check 0, Ruff format check 0, mypy 0 (267 source files); caches external, bytecode disabled.
* Incident retained: an accidental `rm -f /dev/null` failed with permission denied and removed nothing.
* Not run: full gate, SQL Server, browser, Docker, scanners.

## Requirement comparison

| Requirement | Evidence | Result |
| --- | --- | --- |
| Owner answer 1: old copies Invalid, regenerate; no backfill or rewrite | `history` in `BODY_KEYS`; missing key hits the existing KeyError path; legacy and recomputed-digest copy tested Invalid with the regenerate action | Met |
| Owner answer 2: full history, synthetic only | Fixtures are synthetic; README states synthetic-only scope; no real-data path | Met for scope; not a privacy approval |
| Reuse `_report` detached history and visibility preflight | Body uses `report["history"]`, which `_report` deep-copies; preflight unchanged, no new reads | Met |
| Order, detached values, stable export, new event changes digest | Test covers order, mutation isolation, repeat equality, digest change, older copy Stale | Met |
| Held, unreviewed, Not submitted, Not assessed, no authority | Untouched; existing tests still pass | Met |
| Integrity: reorder and removal Invalid | Tested | Met |

## Findings

* RV-001 (Low, residual work): no new negative-actor, foreign-case or unavailable-historical-evidence test for the history path. The paths are unchanged and covered by existing tests, but history exposure (reviewer email, reasons) is the new disclosed content. Destination: distinct follow-up test hardening, or `rpi-implement` if the coordinator wants it before publication.
* RV-002 (Low, evidence): the "edit history event content without updating the digest" case is covered only through reorder and removal, not an in-place field edit. The digest is over canonical JSON of the whole body, so the risk is low. Destination: optional follow-up test.
* RV-003 (Process, retained): the original Review was missing at implementation time; this record fills it prospectively without rewriting history. The changes record lacks a pointer to this Review because it must not be edited. No action.
* RV-004 (Residual, gate): FULL gate on fresh images and current main, independent exact-head assessment, published review, and DPO, Finance, Legal and real-data approvals remain pending. #185 holds the heavy lane. Destination: coordinator.

No Critical, High or Medium findings. No source or plan gap requiring correction was found.

## Residual limits

C1, C5 and C6 stay unchecked; whole #96 and parent #93 are unproven. Receipt `07ae` does not cover this head. A commit of this record changes the head, so the later FULL gate must run on the final head.
