---
title: Issue 109 live changes
ms.date: 2026-11-18
---

No source or test changes. Tier: FOCUSED (documentation and tracking only; no SQL, security-control, infrastructure or deployment change, only throwaway Azure resources removed after use). `rpi-checks.py --all` not run.

## Files

* docs/reference/research/issue-109-live-device-monitoring-evidence-2026-11-18.md (new)
* docs/reference/README.md and docs/reference/log.md (index and log entry)
* .copilot-tracking research, plan, details, critique, changes, review and state for `issue-109-live`

## Live actions (2026-11-18, resource group `ama`)

Throwaway job `job-109-probe`, temporary IoT Hub Registry Contributor role, SAS device `probe109-*`, metric alert `alert-109-probe-connectivity`: all created and removed. A first run failed with plain MQTT `ConnectionFailedError`; the rerun used MQTT over WebSockets. Hub still has public access Disabled and local auth disabled.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| #440 stabilisation checkpoint complete | Unproven: process outcome, not provable by a hub run |
| All child features closed or deferred | Unproven: #110, #111, #184, #1818 open, no deferral recorded |
| No sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking | Already ticked; not exercised |
| Demo aim: device last-activity | Partly proven: connection state and timestamp observed; hub `lastActivityTime` never updated (adverse finding) |
| Demo aim: connectivity alert | Proven for rule firing; delivery untested |

Validation: git diff and link review of the Markdown; no unit tests apply.
