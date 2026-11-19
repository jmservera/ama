---
title: Changes for issue 138 r5
ms.date: 2026-11-18
---

## Changes

* `infra/tests/test_pipeline.py`: added `test_plan_rejects_unsupported_entry_among_valid_changes`.
* `infra/scripts/pipeline.py`: unchanged; it already rejects `Unsupported`.
* Evidence: `docs/reference/research/issue-138-live-r5-2026-11-18.md` and its folder.

## Validation (tier FULL by classification; full gate not run per brief)

* `python3 -m unittest tests.test_pipeline` in `infra`: 33 tests OK.
* Mutation (allow `Unsupported`): 2 failures, then reverted.
* `ruff format --isolated --line-length 100 --check`: clean. `ruff check`: 13 findings, identical to the
  baseline before the change (pre-existing, none introduced).
* mypy per `src/<project>`: not applicable (no `src/` change). No web files changed.
* Not run: `rpi-checks.py --all`, hosted CI, push.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| OIDC per environment | Unproven (0 federated credentials, no environments) |
| what-if on PRs, result attached | Unproven (no runner, gate unset, never attached) |
| Approval per environment | Unproven (0 protection rules, 0 deploy runs) |
| Versioned image built, pushed, referenced | Unproven (no pipeline run) |
| Post-deployment checks fail on unhealthy | Partly proven (unit tests only this run) |
| No secret in logs or repository | Partly proven (r4 scan, not re-run) |
