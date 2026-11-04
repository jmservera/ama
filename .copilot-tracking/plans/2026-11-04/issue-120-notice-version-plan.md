<!-- markdownlint-disable-file -->
# Plan: bind time-capture notice approval to the notice version (Refs #120)

Details: [../../details/2026-11-04/issue-120-notice-version-details.md](../../details/2026-11-04/issue-120-notice-version-details.md)
Research: [../../research/2026-11-04/issue-120-notice-version-research.md](../../research/2026-11-04/issue-120-notice-version-research.md)

## Slices (stacked, only slice 1 delivered here)

* [x] Slice 1: `ZF_TIME_NOTICE_VERSION` must equal `NOTICE_VERSION` for the notice to count as approved (code, tests, README).
* [ ] Slice 2 (later, needs human decision): replace the draft notice wording after DPO/legal/consultation approval and record the version and reference in the enabling audit detail.
* [ ] Slice 3 (human/Azure): actual DPIA, consultation, staff notice approval and administrator ratification in the target environment.

## Gates

* Critique: one self-critique recorded in the review file; no conflict with confirmed decisions.
* Validation tier: focused (no security control weakening, SQL, infrastructure or deployment change). Complete gate not run; coordinator runs gates.
