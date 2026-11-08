---
title: Research, issue 153 document-control retention and hold refusals
ms.date: 2026-11-06
---

* Task: issue153-doc-control-refusals. Branch `fix/document-control-wording-153`, base `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, declared child target `test/ux-evidence-149`.
* Disposition: executed (fresh source reading; prior 153 research reused for the glossary).
* Criteria are data: content standard and AI disclaimer ticked; whole-core-flow audit, reason/owner/next-action errors and named human resident-wording review unticked. This slice proves none of them.

## Source finding

`src/core/src/zava_forward/core/doc_controls.py`, `approve_retention_deletion`:

* Line 292 `PermissionError("A legal hold blocks deletion on this case.")` states a reason but not what a legal hold is, who can act or what to do.
* Line 298 `ValueError("This document is not past its retention trigger.")` uses unexplained "retention trigger". The predicate is `trig is None or trig + years > today`, so it covers two cases: no trigger date recorded, or the period has not ended.
* `content-standard.md` (slice 2 and 3 notes) lists `doc_controls.py` legal-hold wording as unaudited.

## Ownership and permitted actions (evidence)

* `MANAGER_ROLES = ("Retrofit Programme Manager",)`; `_manager` refuses any other role ("Only a programme manager can ..."). Listing (`retention_due`), approving a deletion, placing a hold and releasing a hold all use `_manager`, so the actor who sees the refusal is always already a programme manager.
* `release_legal_hold` records a release (audit `legal_hold_released`) for a programme manager. The code evidences that a programme manager records a release; it does not evidence any criteria for when a release is allowed.
* Hold label in `place_legal_hold`: "a real hold needs the Legal delegate's decision". Module docstring: periods are synthetic placeholders; "the DPO and Legal set the real periods" (PR-003, OD-14); a named manager approves each deletion; a hold blocks it.
* The retention list (`retention_due`) shows trigger and due date per record; `GET /api/retention` is the API route (`src/api/README.md`).
* Trigger source: `_trigger` uses the explicit `retention_trigger` or, for a closed case, `stage_since`. Retention runs from case closing, not upload.
* PRD DH-003: a retention job lists, owner approval is required, a hold blocks deletion.

## Missing decision (reported, not guessed)

Who decides that a real legal hold may end, and on what evidence, is not recorded. Only the Legal delegate's role in placing a hold is evidenced. Copy therefore tells the programme manager the hold stays until released, that a real hold needs the Legal delegate's decision (existing label), and that a programme manager records the release in the system. It does not say Legal approves release or grant any permission.

## Adjacent, out of scope

* `resident_decisions.py:705` has the identical legal-hold text. The assignment excludes that file (issues 86 and 144 overlap). `approve_retention_deletion` forwards resident-record deletions there, so that path keeps the old wording until a later slice.
* No other consumer asserts the old strings (grep of repository). API passes `PermissionError` and `ValueError` text through unchanged.

## Planning Readiness

Ready. Wording only; exception types, predicates, audit event (`retention_delete_blocked_legal_hold` is written before the raise), stored statuses and deletion behaviour stay unchanged. No web file is needed.
