---
title: Issue 1288 live r15 critique
description: One critique of the r15 plan, executed once
ms.date: 2026-11-26
---

Verdict: compatible, with conditions applied directly.

* Risk: setting an operator allowance is an Azure write. Mitigation: finite, small, within the owner's live authorisation and cap, reverted after; no role, network, key or budget change; recorded. Accepted.
* Risk: proactive scan could touch non-demo cases. Mitigation: `ZF_ASSIST_QUALITY_DEMO_HOMES` exact-five scope is already set and Quality refuses other homes; verify via rai-metrics deltas (applied).
* Risk: a mock or fallback response counted as actual AI. Mitigation: require model/version attribution and tokens above 0 in rai-metrics; otherwise report unproven (applied).
* Risk: revision swap loses scan state. Mitigation: state is durable SQL; verify after (applied).
No conflict with a confirmed owner decision.
