<!-- markdownlint-disable-file -->
# Issue #146 console-alerts demo audit: research (2026-11-13)

Research disposition: executed. Planning Readiness: Ready.
Base: `origin/main` 96da501c1. Tier: Focused (documentation only).

## Owner decision

`bicep_146_routing = keep_console_alerts_for_demo`: keep the existing Container Apps `allLogs` diagnostic setting so the source configuration of the two severity-1 console-based ledger alerts is preserved for the demo. Deployed signal operation is not proven (`monitoring-runbooks.md:119-128`). Candidate `9c2a59f6` (explicit categories, `exportContainerConsoleLogs` opt-in) stays unmerged and is deferred to production, together with Action Group delivery verification and approved activation of the disabled candidate alerts (source already references the Action Group at `operationalMonitoring.bicep:51,80`) and production privacy acceptance.

## Brief versus repository discrepancies

* `infra/modules/observability.bicep` does not exist. The monitoring source is `infra/modules/monitoring.bicep` (workspace, App Insights, private link scope, Action Group), `infra/modules/operationalMonitoring.bicep` (candidate alerts, workbook) and `infra/main.bicep` (metric alerts, ledger alerts, budget).
* `src/orchestrator/.../ledger_verifier.py` does not exist. The ledger verifier markers live in `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py:23-26`.
* `9c2a59f6` is on `fix/demo-diagnostic-routing-146-1109`, not on `origin/main`.

## Verification runs

* `infra/tests/test_bicep_policy.py` with `src/core` and `src/orchestrator` pip-installed in `/tmp/venv-146-1515`: Ran 61 tests, OK.
* `az bicep build --file <f> --stdout` (Bicep CLI 0.48.1) for 10 `infra/*.bicep` and 20 `infra/modules/*.bicep` files: 0 errors each.

## Acceptance criteria proof

Numbering: AC1 to AC4 are the four unchecked infrastructure criteria in order; AC5 is the checked tokenomics criterion (budget notification is not a hard cap).

| AC | Criterion | Source proof | Status |
| --- | --- | --- | --- |
| AC1 | Alerts cover job failures, poison queue, ledger digest, IoT ingestion | Ledger digest and verify-missing: `infra/main.bicep:587-612`, `614-640`, markers `digest_blob.py:23-24`, test `test_bicep_policy.py:1141-1171`. Job failures and IoT: `operationalMonitoring.bicep:25-82`, default disabled (`:12-16`, `main.bicep:28`). Poison queue: no alert; runbook gap `monitoring-runbooks.md:273-295` | Partial: poison queue unmet; candidates disabled |
| AC2 | Workbook shows availability, errors, latency, cost against budget | `operationalMonitoring.bicep:84-105`, `monitoring-workbook.json:37-65` (requests, availability), `:65-67` (budget, actual Unknown) | Unmet overall; partial source evidence (actual cost Unknown, rendering unproved) |
| AC3 | Each alert has a runbook entry with an owner | `monitoring-runbooks.md:56-295` entries each with "Proposed owner"; runbook links in alert descriptions (`operationalMonitoring.bicep:30`, `:60`) | Unmet overall; partial source evidence (owners proposed, not appointed: `monitoring-runbooks.md:15-21`) |
| AC4 | Diagnostic logs exclude personal data, raw readings, chat content | Not met by design in demo: `containerapps.bicep:93-100` exports `allLogs` including console; `monitoring-runbooks.md:373-383` states the criterion stays unmet | Unmet, deferred to production |
| AC5 | Budget notification is a notification, not a hard cap | `main.bicep:24`, `667-690` (80 percent actual, 100 percent forecast); `monitoring-runbooks.md:151-170`; `monitoring-workbook.json:67` | Met in source (documented; delivery untested) |

## Why console alerts stay for demo

`main.bicep:602` and `:630` query `ContainerAppConsoleLogs`. Removing console export (9c2a59f6) would leave both severity-1 alerts without their source table and is gated off by default there. The demo prefers working ledger signals; the privacy exposure of console logs is recorded under AC4 and handled in production.

## Deferred to production

* Merge or rework `9c2a59f6` (explicit diagnostic categories, console opt-in) once a non-console ledger signal exists.
* Action Group delivery verification and `enableCandidateMonitoringAlerts` activation with `monitoringApprovalReference`, named owners and thresholds.
* Poison-queue producer, Portal/KQL rendering, billing reconciliation, DPO/Compliance privacy approval.

## Planning readiness

Ready: a documentation-only runbook section recording the decision and AC proof, no Bicep change.
