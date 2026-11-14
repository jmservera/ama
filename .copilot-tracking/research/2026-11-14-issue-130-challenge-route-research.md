---
title: Issue 130 challenge route research
ms.date: 2026-11-14
---

## Scope

Issue #130: remaining criteria on challenge/correction retention, dependent re-review without automatic outcomes, and hazard routing to #85.

## Findings

* `src/core/.../challenges.py` (generic register) already retains reviewer, outcome and evidence and flags hazard referral; unchanged.
* `resident_decisions.py` nomination actions: `nomination_correct` retained the competing account but not who raised it, the challenged review or an explicit re-review block; `nomination_follow_up` lacked `automatic_acceptance`/`automatic_sanction`.
* Hazard concern was refused only in `nomination_record` with a plain `ValueError`; `nomination_correct` and `challenge_open` had no hazard path.
* Representative authority is stored in `representative_authorities` (status, tasks, dates).
* Editable install points at the main checkout; tests need `PYTHONPATH=src:tests:../agents/src` from `src/core`.

## Planning readiness

Ready. Evidence boundary: constructed fixtures only; OD-41/OD-42 and actual human authorization remain open.
