---
title: Live demo evidence for the affected-person challenge and correction route (issue 220)
description: Recorded 2026-11-18 run against the synthetic demo showing what the challenge and referral route enforces live, one blocking identity defect for staff writes, and a per-criterion proven or unproven result
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 220
  - challenge route
  - non-retaliation
  - hazard clock
estimated_reading_time: 6
---

Refs #220. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Production-only criteria stay deferred (#1905-#1908). Nothing here is resident, production or legal evidence.

Four of the five acceptance criteria in #220 are already ticked. This note covers the one unticked criterion, "No retaliation, inferred refusal or delayed hazard response", and checks the ticked ones only for what the live demo shows.

## Method

* Target: `ca-cutover-test-demo-api` (image digest `sha256:5368f4e4...e17e5fb`), Entra sign-in with the employee demo account (role `Retrofit Programme Manager`), Playwright Chromium at 1366 by 900. Credentials were read at run time and never printed; a literal scan of every evidence file for each credential value found no match.
* Case: synthetic `ZF-2025-0331` (stage "Waiting for block programme", one damp and mould hazard, state "Repair evidenced, hold active"). Driver scripts, JSON outputs and screenshot are under `.copilot-tracking/evidence/2026-11-18/issue-220-live/` (`run1.py`, `run1.json`, `run2.py`, `run2.json`, `route-view.png`, `local-repro.txt`).
* Offline: `src/core/tests/test_no_retaliation_guard_220.py` (5 tests) and `src/api/tests/test_challenge_non_retaliation_hazard_guard.py` (9 tests), both OK.
* No Azure resource was created or changed, so there is nothing to delete.

## Observations

| Observation | Result |
| --- | --- |
| Route view `GET /api/cases/ZF-2025-0331?view=nomination-routes-html` | 200, accessible HTML: "Urgent hazards use the hazard reporting route immediately and are never queued here. A named person owns every review and response." |
| Case detail guarantees | Three plain-language guarantees: no lowered priority, eligibility or queue place; no refusal or withdrawal recorded and no consent change; no pause, hold or extension of any hazard or safeguarding clock |
| Case detail assurance | `no_retaliation: true`, `inferred_refusal: false`, `hazard_response_delayed: false` with plain text |
| Extra field `retaliation_flag`, `refusal`, `hazard_pause` or `priority_penalty` in a route write | 400 each, "Supply only permitted route fields", before any write |
| Referral write with `hazard_concern` omitted | 400 (field required) |
| Referral write with `hazard_concern` true or false, valid staff-recorded phone route | 403 "Reload your current staff identity before recording this step." (see defect below) |
| Protected state after every refused write (stage, days in stage, closed, resident, hazards, measure decisions) | Hashes identical to the pre-run snapshot; hazard still "Repair evidenced, hold active"; 0 nomination records |

## Defect that blocks a live write proof

Every resident-workflow write by an Entra-signed-in employee is refused with the 403 above. In `resident_decisions._operation` the check `actor != _person(store, user.get("email"))` compares the verified Entra principal (which carries session keys such as `app_roles`, `auth_provider`, `view_only`, `rule_roles`, `identity_source`) with the stored staff row, which cannot carry those keys. `local-repro.txt` reproduces it offline: an Entra principal with a roster row holding its `email`, `code`, `name`, `role`, `oid` and `tid` still raises `PermissionError`. The offline unit tests pass because they use non-Entra test users. Fixing it changes `src/core` and needs the full validation tier plus a redeploy of the demo image, neither of which the owner authorised here, so no source changed. This is the same gap on the live path for `nomination_record`, `nomination_acknowledge`, `nomination_correct`, `nomination_review` and `challenge_open`.

## Per-criterion result

| Criterion in #220 | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Digital and staff-recorded non-digital routes both work on constructed challenges | Offline only (already ticked) | Offline tests pass. Live write refused by the identity defect; live read shows both channels offered (`digital`, `staff_recorded_non_digital`, assisted phone, paper, letter, in person). |
| Permitted AI, source and policy explanations, owner, next update and resolution are visible | Offline only (already ticked) | The live case has no recorded challenge, so no explanation can be displayed. A challenge also needs a priority suggestion; live `/api/assistants/proposals` returns none (AI tasks disabled for the demo). |
| Only dependent proposals and reviews become stale | Offline only (already ticked) | Needs a correction write; blocked live by the defect. |
| No consent, refusal, sanction, unrelated closure or hazard-clock change is inferred | Partly proven live | Four forbidden adverse fields are refused before any write and protected state is unchanged; the positive write path could not run. |
| No retaliation, inferred refusal or delayed hazard response | Not proven live; proven offline | Live shows the published guarantees, the assurance flags, the forbidden-field refusal and unchanged hazard and queue state across refused writes. The server-side check that a successful challenge leaves protected state unchanged (`assert_no_retaliation`, `stamp_assurance`) passes its 14 offline tests but was not observed on a live successful write. Checking an actual hazard referral on receipt also needs that write. |

## What this does not prove

* A successful live challenge, correction, acknowledgement or hazard-referral write, because of the identity defect.
* Behaviour for a real resident, any retaliation outcome over time, or the independence of a named human owner's response, which are production and human matters.
* The resident app `ca-resident-demo` offers no challenge route, so no resident-side proof was attempted.

## Remaining work

* Fix the Entra identity comparison in `_operation` (compare identity fields, not the whole principal), add a test that uses an Entra principal, redeploy the demo image and repeat `run1.py`. This needs the full validation tier and owner approval for the redeploy.
* Run a live priority suggestion with AI tasks enabled so `challenge_open` can be exercised.
