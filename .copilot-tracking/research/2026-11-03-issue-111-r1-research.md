---
title: Issue 111 round 1 research
ms.date: 2026-11-03
---

Disposition: executed. Planning Readiness: Ready.

## Delivered so far (merged PRs and code)

* #505, #588 and #631/#635/#699/#700: labelled exercise scenario pack, comparator `synthetic/sensor_scenarios.analyse` and consumer-contract tests. They are standalone and do not produce `SENSOR_REVIEW_DUE`.
* #110 consumer: `sensor_consumer.SensorConsumer.observed_series` returns retained canonical rows.
* No `sensor_analysis`, no `SENSOR_REVIEW_DUE` code anywhere in `src/` (grep, 2026-11-03).
* Issue comments: closure audit 2026-10-31 records all three criteria unmet; owner readiness comment offers a bounded read-only, non-emitting exercise slice with zero task, ranking, property, contact and AI writes. The owner has not confirmed it, so the slice stays read-only and proposes nothing by default.

## Constraints from sources

* PRD AC-067: outputs versioned, reproducible from retained readings, labelled by sufficiency; only an approved rule creates `SENSOR_REVIEW_DUE`; insufficient or declined data never lowers priority; no raw readings or device IDs in AI prompts, map clusters, logs.
* PRD AC-068 and research plan: R1 open, R2 competent sign-off and R3 miss/false-alert limits open, so every threshold stays an exercise value.
* ADR 0003 decision 6: approved signal only; stale or missing is INSUFFICIENT.

## Smallest coherent slice (slice 1 of a stack)

Pure `sensor_analysis` module over canonical rows: versioned `derive_signal`, `review_task_candidate` gated by named `RuleApproval`. Not SQL, infrastructure, deployment or security-sensitive (no store access), so the focused tier applies.

## Later slices (not delivered)

1. Store read wiring (`observed_series`) and scheduled run with persisted signal records (SQL: gate needed).
2. Task creation in the condition-assessment queue, behind owner-approved rule (human approval).
3. Accessible list mirroring map status text; AI comparator use (manual path and AI-unavailable behaviour required).
4. R1 to R3 completion and R2 reviewer sign-off.
