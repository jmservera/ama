---
title: Issue 1258 ranking archive ancestor durability evidence
description: Per-criterion evidence that main already syncs new archive ancestors before confirming publication
ms.date: 2026-11-18
---

Scope: demo evidence for #1258 on `origin/main` baf24bf5b (2026-11-18). The change is delivered by PR #1328
(`cd687abad`, merged 2026-11-09). This run changed no source. Live Azure is not relevant: the contract is a
local filesystem sync order, and the issue itself bars claiming real crash or live filesystem behaviour from mocks.

## Evidence

* `src/core/src/zava_forward/core/ranking_publication.py` `_confirmed` syncs the archive directory and every
  parent found by `_walk` (mount-id bounded) after the link, on every confirmation including a retry. Any
  `OSError` becomes `DurabilityUnconfirmedError` with the record kept.
* `PYTHONPATH=tests python3 -m unittest test_ranking_publication test_ranking_publication_runner -q` in `src/core` (the `tests.` module form fails with `ModuleNotFoundError: dataset`):
  110 tests, OK (2026-11-18).
* The same `test_ranking_publication` module run against the pre-fix source (`cd687abad^`) fails, including
  `test_new_nested_ancestors_are_synced_after_link_deepest_first` and
  `test_ancestor_sync_failure_after_link_is_unconfirmed_and_keeps_the_record`, so the tests detect the old behaviour. Observed; raw output not retained.
* `python3 -m mypy` in `src/core`: no issues in 396 source files. Observed; raw output not retained.

## Criteria

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Sync new ancestor entries before confirming, keep first-run behaviour | Proven (offline) | `_confirmed` plus nested-ancestor test expecting `file, link, archive, b, a, root`. Mock-order proof only. |
| 2 Post-link sync failure keeps the record, `committed_unconfirmed` | Proven (offline) | `test_ancestor_sync_failure_after_link_is_unconfirmed_and_keeps_the_record`; runner result at `test_ranking_publication_runner.py`. |
| 3 Syscall-order regression, fails before fix | Proven (offline) | Tests at `test_ranking_publication.py:320-345`; failures against `cd687abad^` listed above. |
| 4 Retry, private stage, audit, path-free errors, original date intact | Proven (offline) | 110 passing tests in the two modules. |
| 5 Original RPI, FULL receipt, independent exact-head review, hosted checks | Unproven | Process and human gates. No source changed here, so no FULL receipt applies; the owner and hosted CI hold the rest. Real crash proof is not claimable from mocks. |

An owner disposition on the mount-topology precondition (PC-002) stays open and is not resolved here.
