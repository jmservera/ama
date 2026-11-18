---
title: Accessibility, equity and journey ownership live demo evidence (#128)
description: Per-criterion demo record for the unticked user research protocol and aggregate-only criterion, with desktop axe results on the live synthetic demo
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and limits

Synthetic demo only, desktop (1366 by 900) only, 2026-11-18. Person-run assistive-technology testing, DPO/Legal approval and billing reconciliation are not needed for the demo (owner decisions 2026-11-18). Automated axe results are engineering proof, not WCAG conformance, fairness or usability findings. No source changed; no Azure resource created or changed.

## Per-criterion result

| Criterion | Status | Evidence |
| --- | --- | --- |
| Direct user research protocol agreed | Unproven | The protocol is a draft in the [equity test plan](./ux/equity-journey-test-plan.md); its agreement record and the [programme plan](./ux/usability-test-programme-plan.md) gate table have no named person or date. The owner waiver of DPO/Legal and person-run testing is not an agreement of the protocol, so none is recorded. |
| Usability measures aggregate only | Proven at source level for the demo | 59 core tests pass (Observed; only the closing summary lines are retained, without the command, module list or date): `evaluate_role_measures` blocks unagreed or backdated audit-use statements, rejects forbidden individual fields and masks cells below five. A source search of `src/api/src` for participant or usability storage found no match (Observed; raw output not retained). The deployed route inventory is unavailable (`/openapi.json` and `/docs` return 404), so absence on the live service is not proven. |
| Keyboard and screen reader (ticked, deferred, #1907) | Stays unproven | Person-run testing is production-only. Automated axe-core 4.10.3 (WCAG 2.0 to 2.2 A and AA tags) found 0 violations on the workbench (32 passes), a case view (34), the resident signed-out page (24) and the resident signed-in page (21). |

## Journey ownership observation

On the live case view the body text shows an owner, a next step or action, and human review wording. The resident landing text did not contain a phone, letter or visit route in the page body (the chat widget states a person can help, see [#619](./issue-619-live-at-consent-evidence-2026-11-18.md)); this is recorded as observed, not as a defect finding.

## Retained evidence

* `live_proof_raw.txt` and `live_proof.json` hold the same data in two formats. Core test output (summary lines only): `.copilot-tracking/evidence/2026-11-18/issue-128-live/core-unittest-raw.txt`.
* Driver, raw and redacted browser output: `live_proof.py`, `live_proof_raw.txt`, `live_proof.json` in the same folder.
* Screenshots: `workbench-1366.png`, `case-1366.png`, `resident-1366.png` in the same folder.
* Sign-in credentials were read at runtime and never printed; e-mail addresses are redacted.

## Remaining human gates

A named person agreeing the protocol, thresholds and audit-use statement with staff, and the production person-run assistive-technology and user research sessions (#1905 to #1908).
