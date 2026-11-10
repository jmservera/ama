---
title: Ranking archive ancestor durability 1258 correction 1 plan
description: Plan to remove the writable-parent cutoff and honor an archive that is itself a mount point
ms.date: 2026-11-08
---

Tier FULL for final publication. This correction runs LIGHT only: bounded synthetic unit tests, one worker, no SQL, browser, Docker, scanner or gate runner. Base `f548b65f4aa31eb92a2cc9cb801130e422daed7f`. Research: [c1 research](../research/2026-11-08-ranking-archive-ancestor-durability-1258-c1-research.md). Details are inline. Earlier plans, critiques and reviews stay as dated history and are not regraded.

* [x] C1.1 Add failing-first tests in `src/core/tests/test_ranking_publication.py` (class `AncestorDurabilityTests`) and run them on the unfixed install, keeping raw output: failed-ancestor then permission-change retry (non-root chmod fixture; restore in `finally`), mocked denied access for a middle and a top ancestor (stands in for another creator or privileged run), archive-itself-mount with a faulting host parent, required ancestor open failure reported.
* [x] C1.2 Fix `_ancestors()` and the docstrings: no `os.access` cutoff; empty chain when the resolved archive is a mount point; otherwise parents nearest first through the first mount point or the root.
* [x] C1.3 Update the two stale tests that asserted the cutoff: the mount-ancestor test is renamed, and the non-writable test now asserts the ancestor is synced through a read-only handle. Drop the redundant mocked-root test (the mocked denied-access test replaces it).
* [x] C1.4 Run paired green: Core `test_ranking_publication` and `test_ranking_publication_runner`, API `test_ranking_publication_wiring` (23), ruff and mypy on the module, import-origin proof from a non-editable out-of-tree install in the scratch venv `/home/azureuser/.local/share/ama/gates/g1258-c1-light-1108`.
* [x] C1.5 Dispositions for readiness L1, M1 and L2 by a dated correction state and notes, without editing the historical plans, reviews or ticks.
* [x] C1.6 Changes and one authored Review for this correction; commit with the repository-local privacy-safe identity. No push, PR, issue or board change.
* [ ] C1.7 Final FULL stays pending. Proposed external output `/home/azureuser/.local/share/ama/gates/g1258-c1-full` (new, short; validate at admission; any failure is retained and the retry uses a new path). Command at admission: `python3 tools/rpi-checks.py --all --jobs 2 --lock-timeout 0 --base <current origin/main> --out <that path> < /dev/null`, then `--verify-receipt` with the current base. No tracked edit after the passing receipt.

## Decisions

* D3 revised (supersedes the original D3 writable-chain rule; original text stays as history): the chain depends only on the filesystem boundary, never on current permissions.
* D5 unchanged: steady-state publication issues extra directory syncs; one more can appear for a deeper chain. R4 stays open.
* Out of scope: store, runner logic, API production code, #1259 path-health fallback, policies, thresholds, infra, cloud.
* Mounts are not created; the mount cases are mocked and named as such.

## Critique dispositions

Filled in from the [c1 critique](2026-11-08-ranking-archive-ancestor-durability-1258-c1-critique.md).
