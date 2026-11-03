---
title: Issue 117 round 1 research
ms.date: 2026-11-03
---

Research disposition: executed. Planning Readiness: Ready.

## Prior delivery checked

* Merged: #270 (scan before availability, retention listing, owner-approved deletion, legal hold), #395 (bounded pending rescan job), #410, #614 (closure audit).
* Code evidence: `src/core/src/zava_forward/core/doc_controls.py` (scanner interface, local synthetic scanner, Defender tag reader, fail-closed verdict checks, hold-blocked deletion).
* Criterion 2 (retention list, owner approval, legal hold) is ticked and proven.

## Gap found

* `infra/modules/containerapps.bicep` sets `ZF_DOC_STORE=azure-blob` but not `ZF_SCANNER`, so a deployed app defaults to the synthetic local scanner with no signal that it gives no malware assurance.

## Slice choice

Smallest coherent slice: log a warning when the local scanner guards an Azure Blob store. No behaviour change, no infrastructure edit (a hard failure would break the current deployment). Touches a security-adjacent control; focused tier only, gate not run.

## Unmet after this slice

* Criterion 1 stays unmet: no real scanner is enabled. Defender for Storage enablement, `ZF_SCANNER=defender` in the deployment and evidence against a real account remain open infrastructure work.
* Approved retention periods (DPO and Legal) remain open.
