---
title: Usability Testing Programme Evidence on the Live Demo (Issue 155)
description: Per-criterion record for the usability programme on the synthetic demo; the SA-010 staff-agreement criterion is not provable without named staff, so only the code gate and the absence of a demo measures surface are shown
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live
Azure is authorised (resource group `ama`, cap USD 700, no drills, no Key Vault
rotation, no production change). Representative-user sessions and any agreement
with staff representatives are production-only. No Azure resource was created
or changed, so nothing needs deleting. The test sign-in was read from the
owner's files at run time and never printed. No source code changed.

## Evidence gathered

* Plan present: [usability-test-programme-plan.md](ux/usability-test-programme-plan.md)
  (dated 2026-11-15) with code in `src/core/src/zava_forward/core/usability_programme.py`.
* Unit tests: `PYTHONPATH=src:tests python3 -m unittest tests.test_usability_programme -q`
  from `src/core`: 15 tests, OK (observed; raw output not retained).
* Gate behaviour, run locally against the default plan: the staff agreement
  flag is `False` (`agreed_with_staff`), and `validate_audit_use_agreement()`
  refuses with `SA-010 gate: staff audit-use statement must be agreed with
  staff representatives before usability measures are recorded`.
* Live read-only run on `ca-cutover-test-demo-api` as the test employee (role
  `Retrofit Programme Manager`, Entra sign-in), Playwright Chromium 1366 by 900,
  2026-11-18. Script and outputs under
  `.copilot-tracking/evidence/2026-11-18/issue-155-live/` (`live_proof.py`,
  `live-proof.json`, `workbench-landing-signed-out.png`).
  * `workbench-landing-signed-out.png` shows the signed-out landing page ("Sign in to the workbench"), not a signed-in workbench; the script saved it under the name `workbench-signed-in.png` before the rename. The string check in `live-proof.json` was taken from that page state, so it supports no claim about the signed-in workbench. No negative claim about usability, survey or participant strings in the workbench is made.
  * Probes of `/api/usability`, `/api/usability-programme` and
    `/api/telemetry/users` returned 403, but so did a nonexistent control route
    (`/api/zz-nonexistent-control`). These probes therefore show nothing about
    the absence of such endpoints and are not counted as evidence.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Test plan names tasks, participants, accessibility support, consent, data handling | Ticked in the issue; plan file present | Plan and tests above; no new claim |
| Task scripts derive from the journey contract and bundles | Ticked in the issue; plan file present | Same |
| Measures aggregate only and audit-use statement agreed with staff first (SA-010) | Not proven | See below |
| Findings logged with severity and linked to backlog issues | Ticked in the issue; code present | Same |
| Negative and inconclusive outcomes recorded; synthetic walkthroughs labelled not user validation | Ticked in the issue; plan states label | Same |

## Why SA-010 cannot be proven for the demo

The criterion has two parts. Aggregate-only measure handling exists in code and
passes its unit tests (`evaluate_role_measures()` rejects individual fields and
masks cells below five). The other part needs a named human staff
representative to agree the audit-use statement before any measure is
reported. The demo has no real staff, and the owner has ruled
representative-user sessions production-only. The agreement record in the plan
stays blank (`Not agreed`) and is left so. The live demo shows no usability
measures surface to the test employee, which is consistent with nothing being
reported but does not prove it, given the uninformative probes above.

## Limits

One role, one account, desktop only. No sessions were run, so there are no
usability results, thresholds remain hypotheses and the criterion stays
unticked.

## Evidence limits

* The signed-in workbench home was not captured. The route after Entra sign-in did not render as a workbench in this run, and the run was not repeated.
* The unit-test result and the gate behaviour were observed locally; raw output was not retained.
* The 403 route probes are uninformative, as stated above.
