---
title: Issue 222 approval binding phase details
ms.date: 2026-11-03
---

## Phase 1

Files: `src/core/src/zava_forward/core/cohort_eval.py`. Add `manifest_digest(manifest)` over the manifest without `approval`, `approve(manifest, approval)` stamping the digest, and require `cohorts_owner`, `lawful_fields_owner`, `thresholds_owner` and a matching digest.

## Phase 2

Files: `src/core/tests/cohort_eval_fixture.py`, `src/core/tests/test_cohort_eval.py`, `src/agents/src/zava_forward/agents/cohort_ranking_eval.py`, `src/agents/tests/test_cohort_ranking_eval.py`. Re-approve after mutating a manifest in tests.

## Phase 3

`src/agents/README.md` approval note. Run focused cohort tests, ruff and mypy only.
