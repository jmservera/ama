# Research: 146-ai-alert-runbook-0150 (Refs #146)

Disposition: executed. Planning Readiness: Ready.

* operationalMonitoring.bicep already authors job-failure, IoT, poison-queue and single ai-limits rules, each naming a proposed owner and a runbookBase anchor.
* monitoring-runbooks.md has anchors for ai-limits, agent-tasks-poison, job-*, iot-*, ledger-*; the four AI classes (calls, tokens, budget, expiry) had no distinct anchor or owner.
* Reasons in ai_consumption.py: call-budget-limit, request-call-limit, token-budget-limit, money-budget-limit, price-unknown, liability-unknown, authority-expired, authority-expiring.
* Baseline failures present before the change: test_bicep_policy ledger-alert test and four tests in src/core test_ai_consumption (not touched).
