---
title: "Research: #79 tie-break, policy-version and read-only archive regression"
ms.date: 2026-11-14
task_id: 79-tiebreak-version-audit-0016
---

## Scope

Issue #79 (priority ranking recalculation and archive), regression slice only. Branch `test/demo-79-tiebreak-version-audit-0016`. Tier: Focused. PR #1585 (infra and orchestrator retention) is not overlapped: this slice adds two new test files under `src/core/tests` and `src/api/tests` and edits no production file.

## Evidence

* `src/core/src/zava_forward/core/ranking.py`: `_rule_keys` appends `case_id` as the final key when the policy does not list it, so every tie on safety, support, waiting days and stage resolves by case id string order. `rank` stamps `policy_version` on each entry; `snapshot` stamps `policy_id`, `policy_version`, `policy_hash`, `as_of` and a content `snapshot_hash`. The module reads no clock.
* UPRN: no ranking input, case field or fixture carries a UPRN (`grep -i uprn` over `src` finds none in ranking, dataset or store). The only deterministic identity tie-break is the case id. The slice therefore asserts the case-id tie-break for cases that share one home address (the nearest stand-in for a shared property) and records the UPRN gap rather than inventing a field.
* `src/core/src/zava_forward/core/ranking_publication.py`: `verify` reads every archived record and returns `count`, `problems`, `latest`. It checks snapshot hash, file name, registry policy version and hash. It writes nothing for an existing folder; an absent folder is empty.
* `src/core/src/zava_forward/core/store.py`: `ranking_publication_status` wraps `verify`, is manager only and must not create the archive folder.
* Existing coverage: `test_ranking_policy.py` (golden order, shuffled reruns, old policy version rerun), `test_ranking_publication*.py` (publish and verify). Gaps: no explicit tie-order across input permutations with fully equal keys, no per-entry version stamp check across versions, no byte-level zero-mutation check of `verify` and the status endpoint over an archived record, and no registry mismatch case that leaves the archive unmodified.

## Planning readiness

Ready. Disposition: executed. No contradictions found between sources and code. Acceptance criteria "same data and policy give same order" and "versioned policy" are already ticked; this slice adds regression evidence and does not claim the unmet owner sign-off or scheduling criteria, so the PR must use `Refs #79`.
