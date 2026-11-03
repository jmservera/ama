---
title: Issue 125 round 1 details
ms.date: 2026-11-03
---

## Design

* `assess_readiness(evidence)`: ten items from the brief; each needs an evidence reference and a confirming role passing a format check and a placeholder check. Output lists satisfied, missing and invalid items. Status is NOT_READY or READY_FOR_OWNER_DECISION; `connection_to_company_data_permitted` and `approved_solution` are always False.
* `authorise_tool(name)`: forbidden areas give DENIED_BY_AUTHORITY_BOUNDARY; unknown names give NOT_ON_READ_ONLY_ALLOWLIST; the six read-only tools from the brief are allowed. `capture_human_review` and `generate_evidence_document` write only to the assistant's own evidence log.
* `ReadOnlyToolbox(tools, readiness)`: requires a ready report, rejects forbidden or unlisted registrations, records denials.

## Out of scope

Company data connection, model use, deterministic duration functions, store wiring, comparison study.

## Validation

Focused unit tests only (see changes file).
