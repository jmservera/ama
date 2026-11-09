---
title: Streamline local validation while preserving coverage
description: Created issue record for the lighter local-validation policy, separate from #470's full-gate timing measurement
ms.date: 2026-11-08
ms.topic: reference
---

## Created Issue

* Issue: #1294, https://github.com/jmservera/ama/issues/1294
* Created: 2026-11-08T21:33:27Z, by the coordinator after finding no issue templates.
* Template: none; .github/ISSUE_TEMPLATE absent.
* Labels: none. Assignees: none. Milestone: none. State at retrieval: OPEN.
* Author: jmservera.
* Title: ci: streamline local validation while preserving coverage
* Relation: related to #470; does not satisfy #470's outstanding full-gate timing measurement.

## Scope and Acceptance Criteria (as filed)

* Reconcile hosted Source CI triggers, affected-project selection and executed checks against local gate coverage; identify local-only checks and execution guarantees, including the employee-chat browser harness and its skip verification; do not equate a path-filtered, absent or skipped workflow with success.
* Document targeted local tests during development; small and documentation-only changes need relevant local checks and applicable required hosted checks, without a blanket `rpi-checks.py --changed` run; preserve local-only coverage or add it to hosted CI first.
* Retain the full exact-head local gate and verified external receipt plus applicable hosted CI for major features, SQL, infrastructure, deployment, security-sensitive changes and releases; mixed changes take the stricter tier; independent exact-head review and human approvals remain.
* Reconcile affected instruction and guide wording without changing branch protection or presenting historical evidence as current; record and test documentation, small employee-chat, SQL, Bicep/security and mixed-scope cases.
* Deliver dated RPI research, plan, changes and original review, plus independent review and applicable checks on the final candidate.
* No Azure deployment, production data access, application AI provider calls, weakened security or change to required hosted checks is authorized.
