# Issue 444 lineage integration review

Date: 2026-10-25. Executed once by an independent read-only code-review agent on merge commit 2049b3b2 (origin/main 36996d70 into a3e527fd). The original 2026-10-24 Review is preserved unchanged.

## Outcome

Conformant. Findings: none. Follow-ups: none required.

## Verified by the reviewer

* No change to staff server.py, auth.py, identity.py, projection.py or store.py relative to origin/main.
* docs/reference/log.md: against origin/main only the 6-line #444 entry is added; no main entry lost. The reviewer did not open the ms.date and rewrapped-entry hunks of the first-parent diff; the 6-line comparison against main covers them.
* README auto-merges keep both sides.
* Main's resident_decisions Entra changes touch staff identity paths only; authority_for is unchanged; the resident boundary files are identical to the candidate.
* Original 2026-10-24 issue444 artifacts unchanged.

## Not covered by this review

Tests were not run by the reviewer (full core 1274 and api 1027 OK by the author). The complete local gate and exact-head browser check follow this review.
