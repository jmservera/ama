---
title: Issue 162 live audit research (2026-11-18)
ms.date: 2026-11-18
---

## Scope

Issue #162 has criteria 1 to 5 ticked and criterion 6 (admin and break-glass audited with purpose, policy decided) unticked. Task: audit each criterion against repo and live demo, separate production-only items. Prior evidence: docs/reference/research/issue-162-live-isolation-evidence-2026-11-18.md and chat-breakglass-live-proof-2026-11-18.md. Plan: re-run live break-glass refusal probe with retained raw output, re-run local tests with retained output, and prove the grant path with the real server code locally on synthetic data.

## Findings

* Disposition: executed. Planning Readiness: Ready.
* Live: break-glass refused (403), each refusal adds one intact audit entry (2068, 2069, 2070); live env lacks CHAT_BREAKGLASS_ROLES and CHAT_BREAKGLASS_REF.
* Local: 33 tests OK; real route dump shows 5 refusal rows and 2 grant rows with purpose, policy_ref, basis demo-only.
* Grant live needs an app config change: outside authorisation. Policy: demo-only owner decision 2026-11-03.
* Follow-ups: owner accept or reject demo evidence for criterion 6; decide admin Entra role, notification and retention.
