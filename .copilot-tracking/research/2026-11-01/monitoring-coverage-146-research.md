---
title: Monitoring coverage 146 research (2026-11-01 slice)
ms.date: 2026-11-01
---

## Disposition

Research disposition: `reused` plus targeted re-inspection. Primary prior evidence:
[2026-10-27 research](../../research/2026-10-27/monitoring-146-research.md) and its merged delivery.

## Findings (current main, 6785d065)

* Delivered: disabled job/IoT candidate alerts and workbook in `infra/modules/operationalMonitoring.bicep`, `infra/monitoring-workbook.json`, catalogue and gap matrix in `infra/monitoring-runbooks.md`, workbook source test.
* Missing for a demo-ready, testable slice: nothing under `src/` links alerts to owners and runbook anchors, evaluates harm/AI-limit indicators with insufficient/blocked semantics, or enforces diagnostic-event content exclusion. All three are criteria in #146 and are only prose today.
* Reusable: `rai_release.named` (named-human check), `ai_consumption` (content-free ledger, not changed here).

## Scope decision

Add one pure module `zava_forward.core.monitoring_coverage` (no I/O, no clock): alert register with owner role and runbook anchor, a register-vs-runbook/Bicep consistency check, indicator evaluation (insufficient/blocked/within/breach, constructed vs approved thresholds, incident owner), and a diagnostic-event allowlist sanitiser. Tests live in `src/core/tests`. No Azure deployment, no new alert resources, no new log categories.

## Planning readiness

Ready. Unproven and left unticked: actual appointments, deployed signals, poison-queue producer, cost/usage feed, privacy approval for existing platform logs.
