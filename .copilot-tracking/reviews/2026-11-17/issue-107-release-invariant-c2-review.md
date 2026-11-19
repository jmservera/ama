---
title: Issue 107 release-invariant classifier correction review
description: One post-implementation review of the C2 correction; earlier reviews preserved
ms.date: 2026-11-17
---

## Execution

Executed once: an independent read-only code-review agent over the working diff plus the implementer's own check of the diff against the plan, critique dispositions and finding text. Earlier reviews (original db7ad, C1, independent C1 functional report) are unchanged.

## Outcome

Conformant for the bounded correction; the single High finding is resolved at code and fake-test level. Not publishable. Open material findings: none.

## Finding disposition

* Active MUTATED row after the supported mismatch worker: now VIOLATED (test `test_active_mutated_row_after_the_mismatch_worker_is_a_violation`; failing before, passing after).
* Restoration only in `after_remaining` or `after_larger` for either capability: now VIOLATED (subTests, failing before, passing after).
* Unreadable, malformed, lost or unbound release state: INSUFFICIENT; violation preserved beside it.
* Pre-worker active `after_mutation` row: not audited; fixture now carries it and ACCEPTED holds.
* Mismatched-row blame requires a completed supported execute and re-invoke, so an unrun worker is a gap, not a false violation.

## Gaps not closed here

* No actual Docker, SQL or old-image execution; the SQLite self-test and fakes are not old-image evidence and the old image's behavior is still unobserved (positive control pending).
* Full local gate and receipt not run (shared heavy lock held elsewhere); no independent exact-head review, hosted CI or human approval yet.
* Strict mypy reports two `no-untyped-call` on unchanged `config` import lines and unrelated errors elsewhere in this venv (missing playwright stubs); baseline for those lines was not separately measured.
* Human, model, serving and live gates of the issue are unchanged and unmet.

FULL / ACTUAL OLD-IMAGE SQL EVIDENCE MISSING, NOT PUBLISHABLE.
