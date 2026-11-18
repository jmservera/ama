---
title: Resident Portal Documentation Integration Status (Issue #441)
description: Live-demo assessment of the unticked #441 acceptance criterion, with the evidence checked and why it cannot be proven for the demo
ms.date: 2026-11-18
---

## Evidence limits

The test result below was observed during the run; raw output not retained. The BRD and PRD statements come from repository files read at the cited lines.

## Scope and limits

Documentation-only check of issue #441 on main `76d89fee2`, run under the owner decisions of 2026-11-18 (synthetic desktop demo; live Azure authorised; DPO/Legal approval, billing reconciliation and person-run assistive-technology testing not needed for the demo). No source, Azure resource or credential was touched.

## Criterion status

Eight of nine criteria are ticked in the issue and were not re-assessed. One is unticked.

| Criterion | Status | Basis |
|-----------|--------|-------|
| 5: requirements owner dispositions FR-044/AC-084 wording before publication; human review stays default and any exception inactive; unsigned status, quality findings, OD-52-55 and Not run criteria visible | Unproven | See below |

## Why criterion 5 cannot be proven for the demo

* The criterion is a named human decision, not a runtime behaviour. Browser or Azure evidence cannot satisfy it, so none was gathered.
* Present wording is consistent with the safe default: [BRD FR-044/AC-084](../../brds/agentic-retrofit-programme-brd.md) (line 1602) keep named per-output review normative with a routine exception only under RULE-028/FR-061, and BRD OD-53 (BRD line 2171) and PRD OQ-029 (PRD line 2969) stay OPEN with routine automation OFF.
* The owner direction of 2026-11-02, recorded in [the log](../log.md#2026-11-17-update--record-owner-fr-044ac-084-directions-in-brd-od-53-and-prd-oq-029-refs-441), approves the exception only in principle subject to named Legal/Compliance approval, and states that a synthetic demo display does not satisfy FR-044/AC-084.
* The 2026-11-18 decision that DPO/Legal approval is not needed for the demo does not name FR-044/AC-084, so it is not treated as the disposition. Ticking would require reading it as one, which the earlier direction rules out.
* `tools/test_resident_portal_docs.py` passes (2 tests), confirming the recorded directions are still present. Observed; raw output not retained.

## Smallest next step

The requirements owner confirms in the issue that the integrated wording makes per-message review normative now, with any routine exception inactive and subject to a later OD-53/RULE-020 approval. This is not a request to activate automation.
