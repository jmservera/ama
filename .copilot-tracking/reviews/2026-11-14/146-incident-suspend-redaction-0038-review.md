---
title: Issue 146 incident suspension and diagnostic redaction review
date: 2026-11-14
task_slug: 146-incident-suspend-redaction-0038
---

## Execution and outcome

Review executed once, by the implementing agent over the diff (self-review, not independent). Outcome: conformant for the offline slice, with open items routed below.

* Redaction is fail-closed and additive; a `%`-placeholder swallowed by a mask is still consumed, so logging cannot raise. Operational markers (`AI_LIMIT_BREACH reason=... route=...`, counts, timestamps) are tested to survive.
* Over-redaction risk accepted: key words such as `name:` or `token:` followed by a value are masked in message text.
* The new end-to-end test covers critical-harm count, approved threshold breach, ownerless refusal, task-only suspension, manual work, reopen persistence and denied restart. Actual restart authority (OD-35) stays unappointed.

## Routed follow-ups

* Compare the core and agents environment failures with base in a provisioned venv (`/home/azureuser/source/ama/.venv` missing).
* Independent exact-head review, hosted CI and human approval remain required; local checks do not satisfy them.
* Live telemetry (Azure Monitor) leak verification stays out of offline scope.
