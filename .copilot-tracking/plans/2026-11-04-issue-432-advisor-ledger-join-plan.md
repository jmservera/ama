---
title: "Plan: #432 resident advisor ledger join"
ms.date: 2026-11-04
---

Details: [details](../details/2026-11-04-issue-432-advisor-ledger-join-details.md)

* [x] 1. Let `LedgerTopicMeter` take capability and case type (defaults unchanged); add `advisor_meters` for the two advisor request kinds.
* [x] 2. Add optional `meters` and a `Meter` protocol to `AzureAdvisor`: reserve after the SQL reservation, dispatch recheck through the wrapped credential, close on every post-dispatch outcome with counts and returned model only.
* [x] 3. Behavioural tests in `test_resident_ledger_meter.py`; update the inventory description.
* [x] 4. Focused tests, ruff, mypy (cache /tmp/mypy-432, tests included).
* [ ] 5. Commit, push, PR with Refs #432.

## Critique (single pass)

* Risk: a held meter blocks residents. Applied: a hold raises `AssistantUnavailable("meter_held")`, so the resident gets the rules summary labelled "AI unavailable" and the manual path; nothing is shown that implies approval.
* Risk: a request kind sent unmetered when a ledger is configured. Applied: with any meters configured, a kind without a meter is refused.
* Risk: raw resident text reaching telemetry. Applied: only counts, outcome and model name reach the ledger; a test asserts case text is absent from ledger records.
* Risk: claiming more than proven. Applied: no host wires meters, so criterion 1 stays unticked.
