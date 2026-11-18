---
title: Issue 146 monitoring coverage inventory research
ms.date: 2026-11-17
---

## Scope

Issue #146, monitoring coverage inventory (alerts, dashboards, runbooks). Documentation and infra README only; no deployment. Tier FOCUSED. Base eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4.

## Research disposition

Executed (measure first). Planning Readiness: Ready.

## Measurements

* Existing infra tests pass: `test_monitoring_alert_coverage` (5), `test_alert_runbook_signal_matrix` (7), `test_ai_alert_runbook_ownership` (4), `test_monitoring_alerts` (8).
* Declared alert resources: 4 metric and 2 ledger rules (main.bicep), 2 vault rules, job failures, IoT failures, poison queue, AI limits. All names map to a runbook heading with an owner in `infra/monitoring-runbooks.md`.
* Finding: `modules/operationalMonitoring.bicep` `jobFailures` builds its runbook anchor from the job-name suffix. Suffixes `-rank` and `-rank-publish` (added by `enableRankingArchiveBlob`) fall to the final branch, so the ranking-job alert links to `job-auth`, whose runbook text covers Entra token renewal. The runbook has no ranking-job section.
* The matrix test lists only four job anchors and cannot see the mislink.
* Fixing the Bicep anchor is an infrastructure change (FULL tier). Out of scope here; recorded as a follow-up.

## Smallest in-scope fix

Add a `Job ranking` runbook section (owner, triage, response, recovery, and a note on the current mislink), plus a regression test that every job suffix the Bicep can create has a runbook section naming an owner and that the mislink is documented while the Bicep still resolves ranking jobs to `job-auth`.

## Out of scope

#1818 and #1641 (core mssqlstore, chat grounding); actual appointments, live portal rendering, billing reconciliation.
