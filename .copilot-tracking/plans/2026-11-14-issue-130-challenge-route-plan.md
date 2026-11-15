---
title: Issue 130 challenge route plan
ms.date: 2026-11-14
---

## Plan

* [x] Add `HazardRouted` (route `independent_hazard_intake`, issue #85, no queue item) and apply to `nomination_record`, `nomination_correct`, `challenge_open` via optional `hazard_concern`.
* [x] Extend `nomination_correct` with optional `raised_by` and `representative_ref`; a representative needs confirmed, in-date "Communicate" authority.
* [x] Retain `challenged_review` (reviewer, outcome) and `re_review` (`automatic_acceptance: False`, `automatic_sanction: False`, dependent review versions) on each correction.
* [x] Expose the same flags in `nomination_follow_up`.
* [x] Add three focused tests in `test_resident_decisions.py` (JSON and SQL variants inherit).

## Critique

One pass: optional fields keep the strict closed-field contract and existing UI payloads valid. Accepted.
