---
title: Accessibility, equity and journey ownership live demo evidence, run 3 (#128)
description: Third per-criterion demo audit for the unticked user research protocol criterion, closing the resident loading gap left by run 2
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and limits

Synthetic demo, desktop (1366 by 900), 2026-11-18. Owner decisions 2026-11-18: DPO/Legal approval, person-run assistive-technology testing and billing reconciliation are not needed for the demo; live Azure is authorised without production changes. No source changed and no Azure resource was created or changed. Axe results are engineering proof, not WCAG conformance, fairness or usability findings. Run 3 repeats [run 2](./issue-128-live2-equity-evidence-2026-11-18.md) and closes its gap: the resident page was still loading when read.

## Per-criterion result

| Criterion | Status | Evidence |
| --- | --- | --- |
| Direct user research protocol agreed | Unproven | The protocol in the [equity test plan](./ux/equity-journey-test-plan.md) is a draft; its agreement record (protocol and thresholds, audit-use statement, lawful basis and minimum fields) has no named person or date. Waiving DPO/Legal and person-run testing for the demo does not agree the protocol, and no agreement is fabricated. Agreement needs named humans, so it cannot be proven by an agent run. |
| Usability measures aggregate only | Proven at source level for the demo | `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_usability_programme test_journey_register` ran 26 tests, OK (`core-unittest-raw.txt`). `grep -rniE "participant\|usability\|sus_score" src/api/src --include=*.py -l` returned no file (exit 1), so the API serves no measure route in source. The deployed API returns 404 for `/openapi.json` and `/docs`, so absence on the live service is not proven. |
| Keyboard and screen reader (ticked, deferred to #1907) | Stays unproven | Person-run testing is production-only. Axe-core 4.10.3 found 0 violations on the workbench (32 passes), a case view (34), the resident signed-out page (21) and the resident signed-in page (21, now confirmed loaded). |

The two ticked criteria and eight RAI cohort criteria were not re-audited; see the earlier demo records.

## Journey ownership and manual route (run 2 gap closed)

* Live case view text shows an owner, a next step, human review wording and a manual alternative (all four checks true).
* The first resident probe still screenshotted the "Still signing you in" state (`resident-1366.png`), so its `manual_route: false` is discarded as a loading artefact.
* A second probe (`resident_wait.py`) read the page at 10, 30, 60 and 120 seconds after sign-in: loaded at 10 s (no loading text), and the text contains phone, letter, visit or help wording (`resident_wait_raw.txt`, `resident-wait-120s.png`). The page shows a Help tab, a paused-contact next step and the notice that neither rules nor AI make decisions. This supports the manual-alternative aspect of journey ownership on the demo; it does not satisfy the protocol criterion.

## Production-only items

* Named agreement of the protocol, thresholds, lawful basis and audit-use statement with staff.
* Person-run keyboard and screen-reader sessions and direct user research (#1905 to #1908).

## Retained evidence

Under `.copilot-tracking/evidence/2026-11-18/issue-128-live3/`: `live_proof.py`, `live_proof_raw.txt`, `live_proof.json`, `resident_wait.py`, `resident_wait_raw.txt`, `core-unittest-raw.txt`, and the screenshot `resident-1366.png`. The workbench, case and resident-wait screenshots were deleted because they showed home addresses. Credentials were read at runtime from the owner's files and never printed; raw outputs contain no e-mail address.
