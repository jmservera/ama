---
title: Research for issue 217 regulatory assistant security, privacy and audit
ms.date: 2026-11-17
---

* Task: issue-217, tier FOCUSED, base origin/main eb51af5c9.
* Disposition: executed. Planning Readiness: Ready.
* Source: issue 217 body and three audit comments; src/api/README.md "Regulatory security, privacy and audit (#217)".
* Baseline measured: core tests test_regulatory_chat, test_regulatory_privacy, test_rule_engine, test_rulecards, test_regulatory_usage: 96 tests OK.
* Finding: audit-log criterion is covered by append-only tables (rule cards, checks, alerts, alert events) and chat turn audit metadata. The rule-engine append-only test only exercises DELETE across rule_engine.TABLES; the triggers also block UPDATE (rule_engine.py lines 272-282) with no test.
* Unmet by design (human/legal/live): DPIA completion, DPO retention, live Foundry minimisation, tenant Entra roles, Art 22A-22C legal assessment. No store changes, no approvals.
* Gap chosen: add UPDATE-refusal regression for every rule-engine audit table.
