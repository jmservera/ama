# Issue 185 plan, round 2 (2026-11-03)

* [x] P1 `rotate()` in `device_identity.py`: precheck run state, issue all new credentials, revoke old, verify only new remain.
* [x] P2 Failure handling: failed or uncertain issue revokes anything beyond the old set and keeps old credentials; errors are fixed codes with no chained secrets.
* [x] P3 Tests with in-memory fakes (`RotationTests`).
* [x] P4 ruff, format, mypy, focused unit tests; commit, push, PR (Refs #185).

Critique (single pass): compatible; live adapters, DPS and cross-process locking stay out of scope. Verdict: proceed. Details: see P1-P4 above.
