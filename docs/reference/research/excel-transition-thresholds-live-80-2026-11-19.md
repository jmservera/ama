---
title: Excel transition thresholds, issue 80 live check
description: Why the staged transition thresholds criterion of issue 80 cannot be proven by an agent for the demo
ms.date: 2026-11-19
---

Scope: the single unticked criterion of #80, "Owners set the staged transition thresholds (ADR 0001 open item)".

Evidence read on 2026-11-19:

* [ADR 0001, Staged transition](../../adrs/0001-azure-architecture.md): stage 1 exits when measures "meet owner-set targets for N consecutive cycles". N and the targets are unset.
* [Importer README](../../../src/importer/README.md): lists the thresholds as not built because owners must set them.
* The 2026-11-18 owner decisions waive billing reconciliation, DPO/Legal approval and assistive-technology testing. They do not set thresholds, and live Azure has no bearing on a decision.

Finding: unproven. A number written by an agent would be an assumption presented as an owner decision. The criterion closes when a named owner records N, the reconciliation, quarantine and drift targets, and the quarantine age limit. A threshold evaluator can follow once those values exist.
