---
title: Issue 891 employee AI live observation changes
description: Actual commands and outcomes without sensitive values
ms.date: 2026-11-08
---

No source, config, infrastructure, access or deployment change. Records only.

Observations (external evidence `/home/azureuser/evidence-891-ai-1108`, scripts and JSON outputs, no values):

* Token endpoint attestation: success (tenant matches the Azure CLI tenant, object present). Held in memory only.
* Run 1 (`live_employee.py` entered at `/`, a public page): sign-in selector timeout, my navigation error, no model call. Run 2 (same script via auth entry, maintained `verify_employee` on a non-employee page state): identity predicate passed (authenticated, expectedIdentity, employeeRole, notViewOnly, providerMatches, schemaValid true; displayEmailMatches and rosterBound false as designed), chat stage failed at the launcher before any ask. Runs 3 and 4 diagnostics only. These adverse outcomes are preserved.
* Run 5 at `/app`: identity admitted; demo disclaimer visible; one ask on a skill with no case detail returned HTTP 200, `model` azure-openai, `workflow_only` false, `model_calls` 1, outcome answer, tokens 375; UI label "Model-generated, not approved. Demo only."

Not proven: maps, case view and briefing stages of the full maintained acceptance on this head; five-agent autonomy; sensor-fed Quality Verification Agent; Legal, DPO, Finance, RAI approvals; current-main acceptance.
