---
title: Capacity booking checkpoint correction 1 details (Refs #440 #82 #81)
description: Phase details for the one-row correction
ms.date: 2026-11-06
ms.topic: reference
---

## P01 Edit the row

* File: docs/architecture/cutover-evidence-pack.md, eleventh classification table.
* Old cell: `193 core tests pass on the export of `af891a5cc``.
* New cell: `193 core tests total, 192 executed, 1 declared JSON-only skip; suite exit 0 (PASS), on the export of `af891a5cc``.
* Limit column unchanged. Use the native edit tool.

## P02 Checks

* `git diff --check`; added lines ASCII; diff is one added and one removed line in the pack only (the removed line is the superseded row, an intended correction); anchor id once; README and log diff empty; pins unchanged; state JSON parses.

## P03 Close

* Changes record, one Review after the checks, state JSON, commit with privacy-safe identity (gh id 8036360, login jmservera) and Co-authored-by trailer.
