---
title: Research for issue 219 material-change invalidation of RAI release records
ms.date: 2026-11-01
---

## Task

Issue #219 (parent #218, depends on #105). Task slug `rai-release-invalidation-219`. Mode: automatic.

## Evidence

* `src/core/src/zava_forward/core/rai_release.py`: pure contract validation and `select`; `CHANGE_TRIGGERS` lists the seven material-change triggers. Bound-version mismatch denies dispatch.
* `src/core/src/zava_forward/core/assistant_release.py`: `assessment`, `admission`, `record` (supersession revokes the prior active record), `change` (suspend or revoke with event).
* `src/core/tests/test_rai_release.py`: five passing tests (contract, expiry, bound versions, reference digest).
* Merged PR #315 delivered criteria 1, 2, 3 and 5 (OQ-017 gap stated through `AUTHORITY_GAP`). Issue comment of 2026-10-27 lists the remaining gaps.

## Gap against acceptance criteria

* Criterion 4: a changed model, prompt, policy, data, permission, evidence or intended use only denies at selection. The record stays `active` and no event records which trigger invalidated it. Dependent records are not explicitly invalidated.
* Criterion 5 (named holders): unresolved human decision (OQ-017); the gap stays stated, not invented.
* Criterion 3 real-evidence approval is a human gate; only constructed fixtures are possible here.

## Decision

Add `rai_release.changed_triggers` (pure mapping from bound-key mismatch to the seven triggers) and `assistant_release.invalidate_changed`, which revokes active records of a single-binding registered task whose binding changed and records an event naming the triggers. Legacy per-deployment tasks are excluded because several deployments legitimately hold separate records.

Planning Readiness: Ready.
