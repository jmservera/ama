---
title: "Plan: #146 alert owner and runbook links on existing rules"
ms.date: 2026-11-14
task_slug: 146-alert-owner-links-1848
---

## Tier

Focused (infra description text only; no permission, secret, deployment or threshold change). Basis: description strings and a test; strict Bicep build run.

## Steps

* [x] Add `runbookBase` var and owner/runbook text to the six existing rules in `main.bicep` and two in `modules/keyvault.bicep`.
* [x] Add `test_existing_rule_descriptions_link_runbook_and_owner` asserting each rule links the matrix anchor and an owner.
* [x] Update the B3 row of the runbook gap matrix.
* [x] Run Bicep build, infra monitoring/policy tests, ruff check and format.

## Critique

One critique pass executed on the final plan: compatible; no conflict with prior decisions. Disposition: applied (keep rules enabled state unchanged).
