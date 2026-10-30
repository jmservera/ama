<!-- markdownlint-disable-file -->

# Changes: fictional-form-review-97-b6-rubric

| Field | Value |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-10-23/fictional-form-review-97-b6-rubric-plan.md |
| Date | 2026-10-23 |
| Base | f1e2d830f17558efd868919de1973ea7244a8841 |
| Pre-commit HEAD | c158ab1e4cee06a60719e0bf3ce7acfa3758da80 (rebased from a74652aa) |

## Summary

No deliverable, score, fixture, runtime or workflow content changed. B6 is not fixed: it is a mismatch inside bot-generated .github/rubric/scores/latest.json and no supported deterministic local correction exists. This cycle adds tracking artifacts only.

## Phase Evidence

* P01 done: branch rebased onto fresh origin/main f1e2d830 without conflicts; 9 commits ahead, origin/main is an ancestor. git diff a74652aa HEAD for latest.json is empty, so no hand edit was made.
* P02 done: B6 findings, options and gate plan recorded here and in the review.

## Deviations

* Ordering: the rebase and an initial rubric-script pytest run happened before the plan was written. Disclosed per critique PC-001; not backfilled.
* The rebase rewrote published SHAs. Publication requires owner-authorized force-with-lease, or alternatively resetting to a74652aa and merging origin/main without rewriting history (PC-002). Remote PR424 head remains a74652aa; no push was made.

## Unresolved B6 and Options

* Cause: bot commit a74652aa rewrote the B6 rationale but re-emitted baseline evidence (pitch brief and src/api/README.md lines 2555-2561). gate.py checks evidence only when a score changes and never relates rationale to evidence.
* Option a: one automatic rescore after a source push. Supported but not guaranteed (model-nondeterministic; tracking-only pushes may be path-ignored; the paid run and push are outside this run). If B6 mismatches again, stop and escalate.
* Option b: drop the bot commits and let the workflow regenerate; needs force-with-lease and owner approval.
* Option c: accept as a recorded residual with the adverse review retained.
* Option d: follow-up issue to add a rationale-versus-evidence check to gate.py.

## Validation

* python3 -m pytest -p no:cacheprovider .github/rubric/scripts -q: 21 failed, 324 passed, 7 skipped (unrelated, scripts unchanged from main, cause not investigated). tools/rpi-checks.py has no rubric reference by text search.
* Focused form-review tests were passed earlier in the session on unchanged sources; not re-run as no source changed.

## Complete-Gate Plan (not run)

* After PR 441 releases /tmp/ama-rpi-heavy.lock and the tracking commit exists: fetch origin main, then python3 tools/rpi-checks.py --all --base <fresh origin/main> --out <new external directory> --lock-timeout 0, then --verify-receipt <receipt.json> --base <current origin/main>.
* A later commit, base move, rebase or dirty input invalidates the receipt; a lock timeout is a blocker. Previous receipts (1c5888f2 and earlier) are historical.
