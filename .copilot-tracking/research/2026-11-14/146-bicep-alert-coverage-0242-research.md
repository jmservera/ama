# Research: Bicep alert coverage (Refs #146, criteria 1, 3, 5)

Planning Readiness: Ready. Disposition: executed.

* Job failures, IoT transport, poison queue and AI limits are in infra/modules/operationalMonitoring.bicep with owner and runbook anchors.
* Ledger digest alerts in infra/main.bicep lacked owner and runbook text in their descriptions (gap).
* The AI limit rule linked only #ai-limits, not the per-class anchors (calls, tokens, budget, expiry) added in parent 65757bc90.
* Candidates are gated by enableCandidateAlerts, approvalReference and per-rule switches, default false; keep.
