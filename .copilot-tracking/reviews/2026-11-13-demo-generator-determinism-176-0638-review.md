<!-- markdownlint-disable-file -->
# Review: #176 generator determinism evidence

* Date: 2026-11-13. Reviewed commit `5408957385829c78677ed5270738ebe4ba5ee679` (parent main `33c261a639b768e06bbd7fe0bd8840d71e3f05bd`). Single independent read-only review (rubber-duck agent), executed once; no tests rerun by the reviewer.
* Original outcome: non-conformant (documentation accuracy), preserved.

## Findings as returned

* Blocking: live_readings was understated as value-level; the test compares lists of serialized `body()` bytes. Research overclaimed that the audit replays every in-repo generator; it registers eight.
* Non-blocking: SQL "unused" wording contradicted the disclosed discarded discovery run; plan still listed whole-module `test_stock_fabric`; backfill shard attribution blurred test (patched shard size) and audit (3 homes, default shard size).
* Confirmed by reviewer: counts and exit codes match logs; commit contains only tracking artifacts; document form and control fixture headers lack `generator_revision`; control fixtures have no replay; live readings have no manifest; scenarios do have one; final test selections bounded and constructed/fictional.

## Routing

Corrections to the changes, research and plan text were applied after the review in the follow-on commit (documentation only, no new execution evidence). No second Review was run, per the one-pass rule; the corrected wording is root's to verify. Matrix and dispositions in the changes artifact are authoritative.

## Unperformed

Reviewer test reruns, hosted CI, full suite, private-input validation, original stock register.
