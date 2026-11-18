---
title: Excel transition thresholds evidence for issue 80 (demo)
description: Per-criterion record for the one unticked criterion of #80 on 2026-11-18; the staged transition thresholds are an owner decision and cannot be proven for the demo
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 80
  - excel transition
  - staged transition
  - thresholds
estimated_reading_time: 3
---

Refs #80. Scope is the synthetic desktop demo, authorised by the owner on 2026-11-18. Nothing here is production evidence. Production-only parts stay deferred.

## Per-criterion result

| Criterion in #80 | Result | Evidence |
| --- | --- | --- |
| Owners set the staged transition thresholds (ADR 0001 open item) | Unproven, and cannot be proven for the demo | The [ADR](../../adrs/0001-azure-architecture.md#staged-transition-proposed-thresholds-to-be-set-by-owners) still reads "proposed, thresholds to be set by owners". Stage 1 exit needs reconciliation, quarantine and drift measures to meet "owner-set targets for N consecutive cycles"; neither the targets nor N exist. A grep of `src/importer/src` finds no threshold setting. The criterion is a decision by named owners (import owner, quarantine owner); the 2026-11-18 owner decision names none and excludes DPO and Legal approval for the demo. A number written here by an agent would not be an owner-set threshold. |

The three ticked criteria were not re-opened.

## Supporting check

* `src/importer` tests: 125 tests, all passed, on this branch (run from `src/importer` with `PYTHONPATH=src:tests:../core/src`). They show the import, quarantine and export mechanics that the thresholds would measure. They do not show that any threshold was set.
* No live Azure action was taken. The importer has no HTTP or web surface and is not deployed to the demo API (`src/importer/README.md`), so a live run could not exercise it.

## What would close the criterion

Named owners approve, in the ADR or a recorded decision, a target for each measure in ADR 0001 "Transition measures" and a value for N, then a person ticks the box.

## Evidence limits

* The 125-test result is a local observation; raw output is not retained.
* "Not deployed to the demo API" is inferred from the importer README, which says the HTTP surface is not built.
