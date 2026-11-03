---
title: Issue 111 round 1 details
ms.date: 2026-11-03
---

## Design

* `derive_signal(home_id, rows, window, as_of, consent, policy)`: order of checks is declined, consent not confirmed, no readings or stale, then the exercise comparator. Sufficiency is one of SUFFICIENT, INSUFFICIENT, STALE, DECLINED; outcome is NO_EXERCISE_SIGNAL, REVIEW_CANDIDATE or INSUFFICIENT. `priority_effect` is always NONE.
* `input_digest`: SHA-256 over the home's rows, canonical and order independent, so a result can be re-derived from retained readings.
* `review_task_candidate`: returns a PROPOSED `SENSOR_REVIEW_DUE` candidate for the condition-assessment queue only when the rule approval matches `RULE_ID` and the policy version and the signal is SUFFICIENT and REVIEW_CANDIDATE. Task key is a deterministic hash for idempotent later creation.
* Plain-language summary states it is not a finding of damp or mould.

## Out of scope

Persistence, scheduling, task creation, ranking, UI, AI use, new thresholds.

## Validation

Focused unit tests only (see changes file).
