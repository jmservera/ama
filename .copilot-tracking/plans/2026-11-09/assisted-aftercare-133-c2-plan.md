# Plan: assisted aftercare 133 corrective cycle C2 (Refs #133)

Task `assisted-aftercare-133-c2`, correction cycle 2 of 5 total (1 prior, 3 remain after C2). Details: `.copilot-tracking/details/2026-11-09/assisted-aftercare-133-c2-details.md`.

## Scope

Fix all four Medium independent Functional findings in Stage A dedicated modules only. No shared hook, no merge or rebase, no push.

## Phases

* [ ] P1 Red regressions first (core): replay after next_update passes (and no duplicate mutation, changed payload still 409), flagged and over-long sensor context refused with the document unchanged and no echo, valid descriptive context still accepted and never dismisses a concern or remedy.
* [ ] P2 Core fix: stable validation first, idempotency lookup inside the transaction, then time validation for new records only; sensor-context guard before persistence.
* [ ] P3 Red regressions (node): real service-contract fixtures generated in Python; unresolved fraction (with zero and Unknown denominators); unconfirmed save outcome wording and request-id retention; definite refusals kept separate.
* [ ] P4 Screen fix in `aftercare.js`.
* [ ] P5 Run affected core aftercare/intake/consumer tests, node screen test, ruff check and format, mypy, `node --check`, `git diff --check`; record raw logs.
* [ ] P6 Docs (README sentence, log entry), changes artifact, one Review by the same independent reviewer path, handoff, commit, clean tree.

## Success

All four findings fixed with tests that fail before and pass after; counters and original qualifications preserved; hook contract unchanged; C1-C6 stay unmet.
