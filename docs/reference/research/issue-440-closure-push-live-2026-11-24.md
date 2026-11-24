---
title: Issue 440 closure-push stabilization checkpoint evidence (2026-11-24)
description: Per-criterion proven or unproven record and per-epic closure readiness for epics 81, 89, 93, 109 and 113, with local regression runs and a signed-in read-only probe of the live demo
ms.date: 2026-11-24
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `7023da86d8520404d663fe912d6c1289b5970f5a` (`origin/main`, read 2026-11-24). Refs #440. No `src/` change, no Azure resource created or changed, no write call on the demo. Sign-in values were read at runtime and never printed. The checkpoint record is the section "Closure-push checkpoint for epics 81, 89, 93, 109 and 113 (2026-11-24, Refs #440)" in the [cut-over evidence pack](../../architecture/cutover-evidence-pack.md). It supersedes the 2026-11-23 nine-epic checkpoint for these five epics ([note](./issue-2301-stabilization-checkpoint-live-2026-11-23.md)), which stays historical.

## Evidence

* Document pins at the head: BRD 0.21.0 `draft` blob `fe5320f9b5b0958e39dbbb56f3e83c18d4c5c2e5`; PRD 0.21.0 `in-review` blob `d1d2c569c51e700940af95e7a82ced4ce4b5e8c5`. Unchanged since the 2026-11-23 checkpoint, so its requirement traceability still holds. Twenty-one commits landed on `main` since `2c06796f5f` (for example 2347 SQL startup lock and continuity tests, 2343 AI input bounds, document controls and sensor grounding, 2331 demo AI override on the SQL store); none changes a gate, grant, procurement or sensor-authority module named in the traceability.
* Local tool audits: `tools/test_epic_81_child_disposition.py`, `test_epic_93_child_disposition.py`, `test_epic_113_child_disposition.py` and `test_epic_child_disposition_audit.py` ran 24 tests, OK, exit 0.
* Local `src/core` suites (`test_gates`, `test_safety_consent_exercise_scenarios_81`, `test_quality_procurement`, `test_grant_lifecycle_controls`, `test_funding_automation_boundary`, `test_coordinator`, `test_sensor_non_authority`, `test_sensor_analysis`): all pass in a 324-test run, 26 skipped, 1 expected failure, 159 s. Six import errors in the same run came from my own wrong module paths (the IoT tests live in `src/api/tests`, not `src/core/tests`); they are not product failures and were re-run from the right package.
* Local `src/api` suites: `test_sensor_ingestion` and `test_iot_stream` 99 tests OK (76 s); `test_iot_credential_hygiene`, `test_iot_device_dedup`, `test_iot_threshold_advisory`, `test_no_public_ingestion_surface`, `test_accessibility_baseline` and `test_content_standard` 76 tests OK. Runs were sequential.
* Azure, read-only: `az containerapp revision list -n ca-cutover-test-demo-api -g ama` shows `ca-cutover-test-demo-api--0000059`, `Healthy`, traffic 100, created 2026-11-24T00:14Z; `ca-resident-demo--0000029` `Healthy`; `/healthz` returns 200 on both; an unauthenticated `GET /api/cases` returns 401.
* Azure, IoT ingestion for Epic #109: `az monitor metrics list` over 2026-11-23T07:00Z to 2026-11-24T07:15Z shows `d2c.telemetry.ingress.success` on `iot-cutover-test-rzsrg` of 12426, 12417, 12457, 12447 and 513 (partial) per six-hour bucket, and `IncomingMessages` on the routed Event Hub namespace `eh-iot-cutover-test-rzsrg` with identical values, so the hub-to-route path carries every message. This is transport observed; it says nothing about analysis authority.
* Signed-in Playwright desktop probe (`.copilot-tracking/evidence/2026-11-24/issue-440-live/live_probe.py`, GET only, output reduced to status and shape): `/api/me`, `/api/cases`, `/api/packages` (1), `/api/workorders` (601), `/api/funding` (167), `/api/resident/choice-queue`, `/api/progress`, `/api/stats` and `/api/checklists` return 200; the case `sensor-summary`, `sensors` and `sensor-drafts` routes return 200 with `state`, `label`, `alert`, `calibrated` fields (a draft state, no authority field); `/api/aftercare` without a concern id returns 404 "That concern was not found", which is input validation. Screenshot: `.copilot-tracking/evidence/2026-11-24/issue-440-live/app-signed-in.png`.
* Child state: Epic #81, #89, #93 and #109 criteria other than the checkpoint box are ticked in the epic bodies (read 2026-11-24). Epic #113 has two further unticked boxes, "All child features closed or deferred" and "No production claim without measured load, recovery and DPO or Legal approvals", and children #115, #116, #117 and #121 read OPEN on 2026-11-24 with `status:partially-delivered` on the two labels read before the GitHub API rate limit hit.

## Per-criterion record for the issue 440 boxes still unticked

| Criterion | Status | Evidence or exact reason |
| --- | --- | --- |
| Triage confirmed findings into independently scoped RPI bug or refactor issues | Proven for this checkpoint | No functional defect was confirmed (see above), so no issue is required; the 2026-11-18 triage note records the earlier disposition. Owner approval is still required for any requirement change, pivot or deferral. |
| Deliver research, plan and details, changes and independent review artifacts | Proven locally | Dated artifacts under `.copilot-tracking/` for this task; the review is a self-run bounded review, not an independent human one. |
| Coordinator change reviewed as a Major HVE Builder change | Unproven for this run | No coordinator file changed here; the earlier HVE Builder evidence is outside this run. |

## Per-epic closure readiness

| Epic | Checkpoint box | Other unticked boxes | Verdict |
| --- | --- | --- | --- |
| #81 | Evidence complete | None | Ready to close |
| #89 | Evidence complete | None | Ready to close |
| #93 | Evidence complete | None | Ready to close |
| #109 | Evidence complete; transport observed on Azure, analysis local | None | Ready to close |
| #113 | Evidence complete for what is delivered | Children #115, #116, #117, #121 open; production-claim box unmet | Not ready: close or defer the four children by owner decision, and leave the production box unticked because production is deferred |

## Production items deferred by the owner

Production load and recovery measurement, DPO and Legal approvals, Azure billing reconciliation and person-run assistive-technology testing are not demo requirements per the 2026-11-18 owner decision. They remain unverified, not passed.

## Limits

Hosted CI, SQL Server variants and `rpi-checks.py` were not run. The GitHub API rate limit stopped two label and parent-link reads, so the #113 child list is as read earlier in the session. The five epic bodies were not edited; ticking and closure are owner actions.
