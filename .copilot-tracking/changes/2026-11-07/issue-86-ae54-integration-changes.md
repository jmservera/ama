---
title: Issue 86 integration of local parent ae54963 changes
description: Changes record for one normal merge (Refs #86)
ms.date: 2026-11-07
---

Scope: Refs #86 only. Prospective records `ae06ed07` preceded the merge.

## Result

* Start `2eda7691…`; planning commit `ae06ed07bc1c6da6e8d00ab0481f3c5f50c2d0e4`.
* One normal merge `4af55e5b634f00719513da4ff39c86d82bdfe236`, tree `a1c8cdc83157f741322cea3dee69fd2dadda5e17`; parents `ae06ed07…` and `ae549635…`. No rebase, force, rewrite or conflict. `origin/main` still `8af3aea6…`, local parent unchanged and clean.
* Incoming delta from the first parent: 45 paths (38 additions, 7 modifications), no mode changes. Non-tracking: `.github/rubric/scores/latest.json`, `docs/reference/{README.md,log.md,resources/ai-tokenomics.md}`, `case_journey_browser_check.py`, `appointments.py`, `test_quality_procurement.py`. Their blobs equal the parent's.
* Blob check: the five corrected complaint paths (README, `complaints_route.py`, `resident_decisions.py`, `store.py`, `test_resident_decisions.py`) are identical to the pre-merge blobs.
* No behaviour change, weakened test or migration.

## Checks (git-archive snapshot of the merged tree, scratch `/mnt/ama-gates/g86-ae54-preparation-1107`)

* Import origin: both modules load from the snapshot.
* `tests.test_resident_decisions`: exit 0, 308 tests, 110 skipped (SQL service and Azure variants skipped, not a pass).
* `tests.test_quality_procurement`: exit 0, 136 tests, no skips.
* Strict mypy: exit 0, 267 files. Ruff check and format check: exit 0.
* A trailing `tail` usage error in my shell wrapper was cosmetic; the check exits are as listed.

## Not done

FULL, SQL, browser, scanner and image runs (not admitted; #107 holds the heavy slot), independent review, hosted CI, human approvals, real receiver acknowledgement. Per-store in-flight registry, point-in-time stale guard and no cross-process proof remain limits.
