---
title: Bicep quality gates 139 review
description: One post-implementation acceptance review of the offline slice
ms.date: 2026-10-16
---

## Execution and outcome

Task #139 / `bicep-quality-gates-139`. Review execution: Complete, one pass.
Outcome: Residual work. No in-scope implementation defect identified.
This accepts the offline engineering boundary, not production readiness,
deployment, locked retention or legal acceptance. No additional review lens
or worker was necessary for the bounded supplied evidence.

## Compared artifacts

* `.copilot-tracking/research/2026-10-16/bicep-quality-gates-139-research.md`
* `.copilot-tracking/plans/2026-10-16/bicep-quality-gates-139-plan.md`
* `.copilot-tracking/details/2026-10-16/bicep-quality-gates-139-phase-details.md`
* `.copilot-tracking/reviews/2026-10-16/bicep-quality-gates-139-plan-critique.md`
* `.copilot-tracking/changes/2026-10-16/bicep-quality-gates-139-changes.md`
* `.copilot-tracking/rpi-sessions/2026-10-16/bicep-quality-gates-139-state.json`

## Assessed boundary

Implementation diff: existing policy unittest, Bicep config, audit-retention
bound, governance policy IDs, source workflow, infra guide, reference index and
append-only log. Source modules and guards were compared to compiled controls.
P01/P02 implementation markers complete; caller-authorized publication follows
Review. Critique execution is distinct: one independent critique returned
Revise, with PC-001 directly incorporated and implemented. No second critique.

| Requirement | Evidence and disposition |
| --- | --- |
| Error-level lint | Existing selected error rules retained; analyzer enabled; temporary unused parameter fails both real CLI actions with named diagnostic |
| Private endpoints | Each service must retain endpoint target/subnet/DNS arguments, actual endpoint and connection, DNS group and parent; all eight service modules include copied-template negative cases |
| No keys | Case-insensitive forbidden functions; storage/registry/Foundry/Insights/Log Analytics/IoT local-auth properties asserted; removal and reversal mutations rejected |
| Entra-only SQL | Required Azure AD-only flag, no SQL administrator login/password; removed or false flag fails |
| Purge protection | Main forwarding, vault purge/soft-delete/RBAC and profile semantics asserted; removed/false purge and forwarding fail |
| Immutability | Exactly two unconditional policies on named audit containers, positive constrained retention and appropriate append flags; removal, retargeting, zero and disabled-policy mutations fail |
| Production isolation | Presence-sensitive per-service access inventory and forwarding, internal Container Apps and conditional SQL firewall; matrix rejects production/public and production/no-purge; bypass mutations fail |
| Unsupported inputs | Named minLength guards plus SharePoint/token readiness/role map, pilot and edge matrix; guard dependency tests retained |
| CI | Infra triggers and new steps within namespace/src-namespace; all original workflow/job/check names unchanged; legacy gate untouched |
| Documentation | Gaps and live limits explicit in guide; index route added; existing log prefix unchanged |

## Validation evidence

* Bicep 0.48.1: all `infra/*.bicep` and `infra/modules/*.bicep` build/lint exit 0.
* Required full infra suite: 86 tests, no skips, exit 0.
* Six same-assertion mutation tests: 131 compiled-template variants rejected.
  Two further CLI lint-error probes reject build and lint.
* Ruff 0.17.1 scoped E/F/I/B/UP and format check: exit 0.
* Git diff check, original workflow/job/check identity comparison and exact
  append-only log-prefix comparison: pass.
* No deployment, what-if, Azure resource query, private dataset or protected
  environment/editor/tracking-file operation.

Dependency restoration and intermediate failures are explicitly recorded in
changes. Governance correction is justified by all-entry-point build failure and
the existing built-in-policy intent; uses tenantResourceId without changing
enforcement or cost. No significant divergence or missing product decision.

## Findings and routing

### RV-001 [Low]: Live guard/network evidence remains separate

The guide already records no live ARM rejection-message, private DNS/routing
or Front Door origin acceptance. Offline compilation cannot establish these.
Route to distinct deployment/network acceptance work when owner-authorized;
pipeline #138 is not part of this task. No in-scope source correction.

### RV-002 [Low]: Retention remains unlocked and legally unratified

The policies intentionally begin unlocked; 365 days is a demonstrator default.
The positive lower bound is not legal retention approval or locked WORM.
Route to named owner retention/locking approval as a distinct follow-up,
not automatic implementation or an irreversible operation in this PR.

## Handoff

Review complete. No blocking in-scope findings. Parent may record completed
offline task, publish the authorized topic-branch commit and PR, and preserve
the two distinct residual items. No repeat Review or routed implementation in
this lifecycle.
