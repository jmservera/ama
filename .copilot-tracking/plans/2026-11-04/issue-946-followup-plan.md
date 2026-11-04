<!-- markdownlint-disable-file -->
# Plan: issue 946 error message

Details: [../../details/2026-11-04/issue-946-followup-details.md](../../details/2026-11-04/issue-946-followup-details.md)
Research: [../../research/2026-11-04/issue-946-followup-research.md](../../research/2026-11-04/issue-946-followup-research.md)

## Phases

* [x] Phase 1: split the receiver condition into released and not-referred checks with accurate messages (`src/core/src/zava_forward/core/workflows.py`).
* [x] Phase 2: regression test asserting both messages (`src/core/tests/test_hazard_referral.py`).
* [x] Phase 3: focused test, ruff, mypy; log entry.

## Critique (single pass)

* Verdict: proceed. Risk: other tests matching the old text; a repository search found none. The released check is first, so a released legacy record with no referral now reports the released state, which is the more accurate message.
* Human approval, resident consent and safety release boundaries are unchanged (text-only change).
