# Issue 81 SQL main integration research, 2026-11-09

Refs #81 only. Task `81-sql-main-integration`, parent `81-forward-preparation`. Research disposition: executed (fresh fetch and hydration; earlier research reused where cited).

## Evidence

* Candidate HEAD `067d1b380fbf6676d11a9453f703ac30c0c29bdb`, tree `330c12e4b35f77277765c61bd16d25689d47b9fe`, branch `fix/demo-recovery-81-1109`, worktree clean. PR #1240 head `6ef6dc368ae3f8739095f740aa1e68634bd52922` (OPEN) is an ancestor; no remote `fix/demo-recovery-81-1109`.
* Fetched `origin/main` `8d6f029cac004506953f36606862168bbe9d9412`: PR #1308 squash (MERGED, `gh pr view 1308`). It is the tip, so it contains the prior `9f9aacc8` merge base.
* Issue #81 (OPEN, epic) acceptance criteria, all unticked: (1) #440 stabilization checkpoint complete, merged children alone insufficient; (2) all child features closed or deferred; (3) no controlled progression with unresolved safety evidence in exercise scenarios; (4) no work started without valid resident agreement or authorised exception in exercise scenarios. PR #1240 carries one APPROVED review and a rubric comment (77/100).
* PR #1308 diff vs candidate: 312 files (mostly tracking evidence). Source overlap predicted by a discarded dry merge: auto-merge of `src/core/README.md` and `store.py`; one real conflict in `src/core/tests/test_resident_decisions.py` (main reworks it, 446 line delta). The dry merge was aborted before any commit; no result is retained.
* Main adds `sqlguard.py` and a SQL manifest guard: real-SQL tests require a task manifest naming an owned container (see `src/core/tests/sqlguard.py`, `test_priority_order.py`).
* Shared rules: heavy lock `/tmp/ama-rpi-heavy.lock`, one nonqueued `flock -n` admission, one owned container; busy means independent light work and a resume return, not queueing, waiver or cloud fallback. Docker/images/caches are not pruned.

## Correction-cycle budget

Repository default: five TOTAL scoped review-correction cycles per issue (owner 2026-11-09), no reset. Original evidence: this lane's recovery and forward-preparation records declare none consumed or reset; earlier #81 history is in the parent records (alignment, realign-r2, merge reviews) and is not re-counted or reset here. No new confirmed defect exists yet; a defect found by integration or SQL checks needs a scoped budget decision rather than blind source expansion.

## Planning readiness

Ready. Conflict intent to preserve: main's priority ordering and SQL bootstrap serialisation plus manifest guard; this branch's resident-decision, gate and hold semantics and cutover evidence.
