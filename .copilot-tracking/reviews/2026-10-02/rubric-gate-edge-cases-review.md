<!-- markdownlint-disable-file -->

# Plan, Changes and Review: rubric-gate-edge-cases

* Task ID: 2026-10-02-rubric-gate-edge-cases (child of 2026-10-02-rubric-gate-status-correctness)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-gate-hardening-review.md (RH-003, RH-008, RH-009)

## Plan and changes

* [x] RH-003 prepare.py: on non-PR events every current file of a changed artifact may be cited, so main-side edits hidden by a stale squash range stay citable. Push runs are report-only, so the looser evidence rule cannot change the baseline.
* [x] RH-008 gate.py `clean_text` also neutralises `www.` links, `GH-123` references and 7 to 40 character hex strings (commit SHAs), staying idempotent.
* [x] RH-009 workflow push uses `GITHUB_SERVER_URL` for the host and `core.hooksPath=/dev/null` so a planted hook cannot see the token; lock recompiled.
* [x] Tests: extended cleaning test (www, GH-, SHA, idempotence); stale-squash push test.
* Critique: not dispatched (stated fixes).

## Validation

* 51 passed, 1 skipped (symlink), minimal pytest stub. `gh aw compile rubric-score`: 0 warnings.

## Review (one pass, inline)

* Outcome: Conformant. RH-003, RH-008, RH-009 closed.
* Note: long decimal numbers (7+ digits) also get a zero-width space; visual only.
* All known review findings are now closed. Remaining owner items: real pytest run (RS-002), first live run, forced calibration run, required check.
