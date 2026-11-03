# Plan: issue 220 protection and overdue slice, 2026-11-03

* [x] Add PROTECTION constant and `protection` key in `ChallengeRegister.view`.
* [x] Add read-only `overdue(today)`.
* [x] Tests in `src/core/tests/test_challenges.py`; update `src/core/README.md`.
* Critique: executed once (self); compatible, read-only additions, no state fields. Verdict: proceed.
* Stacked next slices: store persistence and API/UI wiring (#130); human acceptance of criterion 5.
