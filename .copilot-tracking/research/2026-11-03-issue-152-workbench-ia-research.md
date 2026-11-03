---
title: Research, issue 152 role workbench IA delivery status
ms.date: 2026-11-03
---

## Disposition

Executed (bounded, local evidence only). Planning Readiness: Ready.

## Delivered already (merged PRs)

* #317: shared workbench IA, own-queue navigation, 320/390/768/1024/1280 checks, safety-first order (criteria 2 to 4 ticked).
* #659: supported-devices proposal (`docs/reference/research/ux/supported-devices-proposal.md`), recorded as "Proposed, not decided".
* Closure audit 2026-10-31: criteria 1 and 5 remain unmet.

## Unmet criteria

* Criterion 1 (supported devices decided with owner): owner decision. Cannot be delivered by engineering; the manifest keeps `supported_devices.status = proposed`.
* Criterion 5 (cross-profile checks follow AC-034/AC-043 manifest): FR-035 requires per-profile default IDs, count, order and selection. `src/api/checks/workbench-manifest.json` had fixture lists only; the safety profile fixture (ZF-4) differs from its empty own queue, and the contractor fixture order differs from its queue order. The check matrix for AC-034 compares reset IDs/count/order with the default manifest, but no declared default existed.

## Chosen slice

Declare per-profile `default` (ids, count, order, selection, empty reason) in the manifest and test it against the role queues. Offline, no browser, no security/SQL/infra/deployment change. Focused tier.

## Evidence

* `src/api/checks/workbench-manifest.json`, `src/api/tests/test_workbench.py`, `src/api/checks/workbench_browser_check.py` (already asserts `role["ids"]` per role).
* PRD FR-032, FR-035, AC-034, AC-043 in `docs/prds/zava-forward-retrofit-programme-demonstrator.md`.

## Follow-ups

1. Owner decision on supported devices (criterion 1).
2. Technical, procurement, QA, financial and operator scripts for the eight deferred or partial workflows (criterion 5).
3. Human accessibility acceptance.
