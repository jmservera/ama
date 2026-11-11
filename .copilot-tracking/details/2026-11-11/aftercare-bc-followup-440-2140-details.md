---
title: Aftercare post-1458 follow-up details (Refs #440 #1402)
description: Step-level details for the follow-up observation
ms.date: 2026-11-11
---

Plan: [plan](../../plans/2026-11-11/aftercare-bc-followup-440-2140-plan.md).

* Folder: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/aftercare-bc-followup-440-2140/` holding `export/` (git archive of `src` at `bc123235`), `home/`, `origins.log`, `B1.log` to `B3.log` with `.exit` files, `env.log`.
* Selector commands from `export/src/core`: `python3 -m unittest test_aftercare_intake -v`; `python3 -m unittest test_aftercare.SnapshotTests -v`; `python3 -m unittest test_aftercare_store -v`. The `PYTHONPATH` is `export/src/core/src:export/src/core/tests` plus the export agents and api source only if an import requires it.
* Exit codes are taken from the unittest process, and the Ran and OK or skipped lines are read from stdout; an exit of 0 is not used as proof without the counts.
* Record content: no totals are invented; counts are what each selector printed.
