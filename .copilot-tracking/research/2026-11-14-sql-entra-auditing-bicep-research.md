---
title: SQL Entra auditing Bicep research (issue 143)
ms.date: 2026-11-14
---

## Scope

Refs #143, stacked on PR #1672 base 59c53274. Inspected infra/modules/sql.bicep, infra/main.bicep, infra/tests/.
Research disposition: executed. Planning Readiness: Ready.

## Findings

* sql.bicep already sets azureADOnlyAuthentication true, minimalTlsVersion 1.2, publicNetworkAccess Disabled, restrictOutboundNetworkAccess Disabled.
* Server auditing to Azure Monitor, threat protection and diagnostic settings (master SQLSecurityAuditEvents, database allLogs) exist.
* No firewall rules, no administratorLogin or password parameters anywhere in infra Bicep.
* infra/tests/test_sql_tier.py covers tier only; no contract test covers governance. keyvault.bicep (#142) is untouched.
* Issue 143 body text describes network edge work; the task scope was taken from the delivery request.
