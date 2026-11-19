---
title: Issue 80 live research (demo)
description: Opening research for the one unticked criterion of #80, staged transition thresholds
ms.date: 2026-11-18
---

Refs #80. Task `issue-80-live`, Research disposition `executed`. Scope: synthetic desktop demo, docs and evidence only.

## Unticked criteria

* Owners set the staged transition thresholds (ADR 0001 open item). Only this one is unticked; the other three are ticked and are not re-opened.

## Findings

* `docs/adrs/0001-azure-architecture.md` "Staged transition" says "proposed, thresholds to be set by owners". Stage 1 exit needs reconciliation, quarantine and drift measures to meet "owner-set targets for N consecutive cycles"; N and the targets are unset. Stage 2 needs staff sign-off, an out-of-hours route, rollback and data protection approval.
* `src/importer/README.md` lists the staged transition thresholds as "Not built ... which owners must set".
* The owner decision of 2026-11-18 excludes DPO and Legal approval from the demo and names no transition-threshold owner.

## Planning Readiness

Ready. Proposed approach: record the criterion as unproven for the demo with the reason, run the importer tests as a bounded local check of the mechanics the thresholds would measure, and change no source.
