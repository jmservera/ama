---
title: Quality sensor values and review flag, fifteenth audit (Refs #1288)
description: Fifteenth audit of the demo Quality sensor integration; a live allowance attempt found the owner demo override never reached the assistants path, fixed in source, with the per-criterion proven or unproven table
ms.date: 2026-11-26
---

Scope: synthetic demo, desktop only. Follows the [fourteenth audit](./issue-1288-live-r14-quality-sensor-evidence-2026-11-23.md). Credentials were read at run time and never printed. Evidence: `.copilot-tracking/evidence/2026-11-26/issue-1288-live15/` (`live_probe.json`, `walk.json`, `azure_set_allowance.txt`, `azure_revert.txt`); no email, token or key is stored.

## What changed since r14

The earlier blocker (no approved release record) is gone: `GET /api/assistants` on revision `ca-cutover-test-demo-api--0000079` lists every assistant as `release: "in force"`, deployment `standard`, model `gpt-4.1-nano-2025-04-14` (from the #107 release records of 2026-11-25). The app already carries the five-home Quality scope (`ZF_ASSIST_QUALITY_DEMO_HOMES`) and the owner-directed suspension override (`ZF_DEMO_AI_SUSPENSION_OVERRIDE`), but no operator allowance.

## Live walkthrough attempt

* I set a finite allowance on the demo API (authority label, 10 calls, 200000 tokens, expiry now plus 3 hours, proactive on) as revision `0000080`, within the owner's live authorisation and the USD 700 cap, watched for 10 minutes, then removed the five variables (revision `0000081`, Healthy, the two pre-existing `ZF_ASSIST_*` settings kept). Nothing else changed; no resource was created.
* Result: no model call. `rai-metrics` stayed at `tokens` 0 and `invocation` 3 for the whole window; only `fallback` rose from 20 to 25 (scanner rounds refused to a manual route).
* Cause found: `GET /api/assistants/proposals?case_id=...` for the five demo homes returned `disabled: "Suspended (SUS-1) ..."` and every Quality task `state: disabled`, `display_state: suspended`. The 2026-11-23 owner override was applied in `continuity.continuity_suspension` (store level, used by chat) but not in `Assistants.suspended()` and two display sites, which called `continuity.active` directly. The override therefore never lifted the hold for the assistants, including the Quality assistant.

## Defect and fix (source)

`Assistants.open_suspension` now skips the hold when `continuity.demo_owner_override()` is true (demo profile and exact owner value); `suspended()` and the two task-view sites use it. `gate_hold` (fail-closed gate mismatch) still applies and the suspension record stays open. Test `test_owner_demo_override_lifts_the_assistant_hold_and_keeps_the_record_open` fails on the base and passes with the change. Targeted run: 274 tests OK (83 skipped for SQL Server and browser prerequisites); ruff check and `src/api` mypy clean; `src/core` mypy shows the 3 pre-existing errors and `ruff format --check` flags `assistants.py` as on the base.

## Why the live leg is still unproven

The fix is source only. The Container Apps image comes from `crcutovertestrzsrg`, which has public network access disabled (`az acr build` was refused with 403 in earlier passes); opening it is a network-posture change outside the owner's decisions, so the fix is not deployed. Clearing the open SUS-1 record needs a named human restart authority, which does not exist for the demo. A mock or fallback output would be the deterministic outcome the criterion excludes.

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3. Quality AI snapshot consumes the identical reading IDs and values shown by the UI | Proven locally (mock provider); not live | Grounding and correlation tests in the 274-test run; no live model request |
| 4. Release-admitted proactive, durable, deduplicated, bounded flag | Unproven live | Release in force and bounded allowance accepted (scanner ran, fallback only); the assistants hold blocked it (SUS-1), override defect fixed in source, not deployed. Local dedup and bounds covered by retained tests |
| 5. Employee sees finding, cited IDs, source time, model/version, unapproved status | Proven locally; not live | No live model output exists |
| 6. Explicit insufficient, blocked and unavailable states with a human route | Proven locally; seen live | Live: `disabled` with the SUS-1 text and manual route, `suspended` display state, release-denial reasons; no zero substitution or silent normal state |
| 7. Focused SQL, API and browser tests correlate UI values and IDs with the model-request snapshot | Proven as local engineering evidence | Fixture data, mock provider; SQL Server and browser cases skipped here |
| 8. Finite live walkthrough, actual model consumption, visible attributed flag | Unproven | Simulator, Hub, SQL and UI legs seen live in r12; the model leg was blocked by the assistants hold; tokens stayed 0 |

Criteria 1, 2 and 9 are ticked. No tick or closure is claimed; independent review and hosted CI remain outstanding. To finish 4 and 8: deploy a build containing this fix (needs registry access), set the same finite allowance, and run one walkthrough.
