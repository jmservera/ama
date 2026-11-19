---
title: Issue 120 research, DPIA-gated staff time capture
date: 2026-11-17
---

# Research: issue 120

Disposition: executed. Base origin/main eb51af5c. Tier FOCUSED, docs/design only. Planning Readiness: Ready.

## Opening state

* C1 and C2 are ticked (PR 408). C3 (staff notice approved, enabling audited) is unmet: code and audit exist (PR 1104), but the human notice approval, consultation and administrator ratification do not. No agent can tick C3.

## Measurements

* Baseline: from `src/api` with worktree `PYTHONPATH` (the installed editable packages point at the main checkout, so the default import path tested the wrong tree), `unittest tests.test_timecapture tests.test_timecapture_copy` ran 38 tests, OK, 5 skipped (browser opt-in), 18.3 s.
* Drift reproduced by reading `src/api/src/zava_forward/api/timecapture.py` against ADR 0002 decision 7 (`docs/adrs/0002-pilot-readiness-architecture.md`, lines 988-1006):
  * ADR names only a DPIA id, a notice version and a consultation reference. The code also requires `ZF_TIME_NOTICE_APPROVED` and a `ZF_TIME_NOTICE_VERSION` equal to the current notice version.
  * ADR says enabling is an audited administrator action. The code requires a request by one manager and enabling by a manager in a different role, void if a reference or the notice version changes.
  * ADR omits the per-person, per-version notice acknowledgement that gates recording.
  * ADR says retention is its own value set from the DPIA. The code keeps the tables in the shared SQL store and sets no retention value; it is an open DPIA input.
* The decision 7 status row (line 1086) and `src/api/README.md` already describe the built controls; only the decision text is stale.

## Out of scope

Core mssqlstore and chat grounding (1818, 1641), code changes, live capture, human approvals.
