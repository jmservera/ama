---
title: Details, issue 153 document-control retention and hold refusals
ms.date: 2026-11-06
---

## Revision after critique (2026-11-06)

The two quoted messages below are the pre-critique draft and are superseded by the dispositions in `challenges/2026-11-06/issue153-document-control-refusals-critique.md`. Final copy:

* Hold: "A legal hold is in place on this case (its documents must be kept for a legal reason), so nothing was deleted. Keep the documents. This system only records the hold; a real hold needs the Legal delegate's decision, and a programme manager can record its release once the hold has ended."
* Not due: "This document is not due for deletion, so nothing was deleted. Its retention period (demonstration values, not an approved schedule) counts from the date the case closed or a recorded retention start date, and that date is missing or the period has not ended. Keep the document and check the case closing date or retention start date."
* Test additions: both not-due branches (no trigger, future trigger), document and blob retained, audit chain, exact due-day deletion succeeds. Docs scope: only these two refusals are marked audited.

## Draft copy (superseded; ASCII, no new authority)

Hold refusal (`PermissionError`, `doc_controls.py` near line 292):

> A legal hold stops deletion on this case: its documents must be kept for a legal reason, so nothing was deleted. Keep the documents. The hold stays until a programme manager releases it, and a real hold needs the Legal delegate's decision.

Not-due refusal (`ValueError`, near line 298):

> This document is not due for deletion, so nothing was deleted. Its retention period (how long it must be kept) runs from the case closing or a recorded retention trigger date, and either that date is missing or the period has not ended. Check the due date in the retention list; a programme manager can view it.

Notes:

* Both messages keep the reason, the owner (programme manager, already the only actor; Legal delegate for a real hold) and the next action.
* "Retention trigger" is explained, not removed; "legal hold" keeps its legal meaning.
* The not-due text covers both predicate branches (no trigger recorded, period not ended).
* Synthetic-placeholder periods are already labelled in the retention list label; the copy does not state a period.

## Code and tests

* `doc_controls.py`: two string literals only. The audit call before the first raise, the types, the predicates and `_remove_document` are untouched.
* `test_document_controls.py`: new test using the existing `make()` store helper and `SAM`/`PAM` fixtures. Case 1: place hold, approve, assert `PermissionError` text contains "kept for a legal reason", "nothing was deleted", "programme manager", "Legal delegate"; document count unchanged; audit action `retention_delete_blocked_legal_hold` present once; `verify_audit()` true. Case 2: not-due document raises `ValueError` with "retention period", "retention list", document remains, no `retention_deleted` audit.
* `test_content_standard.py`: lexical guard reading `doc_controls.py` literals: no bare "retention trigger." refusal and no bare legal-hold refusal; both required phrases present.

## Docs

* `content-standard.md`: add slice 4 note; remove `doc_controls.py` legal-hold wording from unaudited list in a new sentence (earlier slice text is preserved as history).
* `docs/reference/log.md`: append entry. Index unchanged unless its content-standard summary needs it.

## Constraints and risks

* Do not touch `resident_decisions.py:705` (identical old text remains on resident-record path; recorded as follow-up).
* Release authority is an open decision; copy must not claim Legal approves release.
