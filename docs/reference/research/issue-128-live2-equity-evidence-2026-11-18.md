---
title: Accessibility, equity and journey ownership live demo evidence, run 2 (#128)
description: Re-run of the per-criterion demo audit for the unticked user research protocol criterion, with retained commands, raw output and desktop axe results
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and limits

Synthetic demo only, desktop (1366 by 900) only, 2026-11-18. Owner decisions 2026-11-18: DPO/Legal approval, person-run assistive-technology testing and billing reconciliation are not needed for the demo; live Azure is authorised without production changes. No source changed and no Azure resource was created or changed. Automated axe results are engineering proof, not WCAG conformance, fairness or usability findings. This run repeats the [first run](./issue-128-live-equity-evidence-2026-11-18.md) and keeps the commands and raw output that run did not retain.

## Per-criterion result

| Criterion | Status | Evidence |
| --- | --- | --- |
| Direct user research protocol agreed | Unproven | The protocol is a draft in the [equity test plan](./ux/equity-journey-test-plan.md); every row of its agreement record has no named person or date. Waiving DPO/Legal and person-run testing for the demo does not agree the protocol, so no agreement is recorded or fabricated. |
| Usability measures aggregate only | Proven at source level for the demo | `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_usability_programme test_journey_register` ran 26 tests, OK (verbose list in `core-unittest-raw.txt`). The module blocks unagreed audit-use statements, rejects individual fields and masks cells below five. `grep -rniE "participant\|usability\|sus_score" src/api/src --include=*.py -l` returned no file (exit 1, `api-source-search-raw.txt`). The deployed API serves no route inventory (`/openapi.json` and `/docs` return 404), so absence on the live service is not proven. |
| Keyboard and screen reader (ticked, deferred to #1907) | Stays unproven | Person-run testing is production-only. Automated axe-core 4.10.3 reported 0 violations on the workbench (32 passes), a case view (34), and the resident signed-out page (21). A resident "signed-in" scan (21 passes) was also recorded, but its screenshot shows the page still loading ("Still signing you in"), so it is not counted as a signed-in result. |

Criteria already ticked (missing data and incomplete appointments get human review; the eight RAI cohort criteria) were not re-audited here; see the earlier demo records indexed in the knowledge base.

## Journey ownership observation

The live case view text shows an owner, a next step and human review wording. The resident check (`manual_route: false`) ran while the resident page was still loading, so it says nothing about a phone, letter or visit route; no finding is drawn. A rerun after the page has loaded is needed.

## Production-only items

* Named agreement of the protocol, thresholds, lawful basis and audit-use statement with staff.
* Person-run keyboard and screen-reader sessions and direct user research (#1905 to #1908).

## Retained evidence

All under `.copilot-tracking/evidence/2026-11-18/issue-128-live2/`: `live_proof.py` (driver), `live_proof_raw.txt` and `live_proof.json`, `core-unittest-raw.txt`, `api-source-search-raw.txt`, and screenshots `workbench-1366.png`, `case-1366.png` and `resident-1366.png` (the last shows the loading state). The driver imports its sign-in helper from the existing `issue-619-live` evidence folder. Sign-in credentials were read at runtime from the owner's files and never printed; the raw output contains no e-mail address.
