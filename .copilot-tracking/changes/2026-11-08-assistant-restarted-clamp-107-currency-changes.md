---
title: Issue 107 restarted clamp currency changes
description: Changes record for the normal merge of main 0f05e9a into the restarted clamp candidate
ms.date: 2026-11-08
ms.topic: reference
---

## Actions

* Committed the [currency plan](../plans/2026-11-08-assistant-restarted-clamp-107-currency-plan.md) and [critique](../plans/2026-11-08-assistant-restarted-clamp-107-currency-critique.md) alone (commit before merge).
* One normal `--no-ff` merge of `origin/main` `0f05e9aae70768def8d1d9c300215f9ee2f11638`, merge commit `37bcbb32a8dd3d7073d27fdd936f0d9ffde785d8`, merge tree `60ae08ccab52abdce4cf3183434806a6de735e00` (incoming: 21 added issue 530 tracking files, no conflict).

## Proofs (Git metadata only)

* Diff against main outside `.copilot-tracking/`: only `src/api/tests/test_assistant_release.py`, 27 added lines, as before.
* Blob ids equal main for `assistants.py`, `assistant_process_worker.py`, `tools/rpi-checks.py`, `store.py`, `mssqlstore.py` and `rubric.json`.
* No path outside added tracking files changed since `0c11c26`; every original restarted-clamp record is byte-identical to `0c11c26`.

## Deviation correction

The two deviations (in-tree temporary mutation, narrower assertions) are recorded in the currency plan. The original changes and review records are untouched.

## Not run

No unit run (only inert tracking bytes changed; the original 8 tests with 4 skips and the 174 with 62 skips stay attributed to `0c11c26`), and no SQL, Docker, runner, browser or scanner. Actual MSSQL execution of the new method is unverified.
