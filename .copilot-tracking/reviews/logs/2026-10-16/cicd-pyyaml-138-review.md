---
title: CI infra test dependency correction review
description: One post-implementation review of the PR 357 correction
ms.date: 2026-10-16
---

Task: 138-ci-pyyaml. Execution: Complete. Outcome: Residual work.
No correction defect identified; inherited live acceptance remains unmet.

## Compared artifacts and boundary

* `.copilot-tracking/research/2026-10-16/cicd-pyyaml-138-research.md`
* `.copilot-tracking/plans/2026-10-16/cicd-pyyaml-138-plan.md`
* `.copilot-tracking/details/2026-10-16/cicd-pyyaml-138-phase-details.md`
* `.copilot-tracking/plans/2026-10-16/cicd-pyyaml-138-critique.md`
* `.copilot-tracking/changes/2026-10-16/cicd-pyyaml-138-changes.md`

Review only the bounded CI dependency correction after merge of origin/main.
P01 and P02-T01 have completion evidence. P02-T02 is this review;
P02-T03 publication remains an explicit post-review administrative action.
No repeat review or implementation loop.

## Assessment and validation

The actual failing CI step installs the exact existing test pin before
discovery, in the same interpreter environment. Source CI already does so.
The new assertion is scoped to each executing infra step; deletion, unpinning
and late-install mutations fail it in both consumers. All original workflow
permission/approval/runner/pinning/no-echo mutations are retained and pass.
No missing-dependency skip, fallback parser or production dependency added.

The source-only isolated baseline reproduces missing yaml. The same interpreter
passes all 156 infra tests after the test-only pin; the Bicep-required run
also passes with absolute source fixture paths. Seven workflow test methods
pass separately. Existing real installed API probes verify health 200 and
three authentication-denial cases against constructed local data.
Ruff/format and strict helper mypy pass. Diff whitespace, excluded-path and
production-manifest checks pass. Programmatic comparison confirms every prior
log entry from both branch and origin/main survives verbatim.

Plan and detail markers match implementation evidence; pending publication is
explicit, not represented as already completed. One critique disposition
rejects a worker-local temporary-directory restriction inapplicable to parent
execution and retains the valid tool-install ordering clarification.
This preserves user intent; no unresolved design decision.

No new image build, deployment, OIDC flow, live approval or live log audit was
executed. These are unnecessary for this CI-only repair and cannot be inferred
from the passing local checks.

## Acceptance audit

| Issue criterion | Evidence and result |
| --- | --- |
| Per-environment OIDC | Unmet: actual federation/RBAC/authentication unverified |
| PR what-if with attached result | Unmet: no live pipeline what-if result |
| Approval and matching environment parameters | Unmet: actual reviewer configuration/approval and target prerequisites unverified |
| Versioned pushed image referenced by deployment | Unmet: no live pipeline image push/apply/quarantine-release evidence |
| Automatic post-deployment checks | Unmet: local probes pass, live private checks remain unverified |
| No secret values in logs/repository | Unmet end to end: static/no-echo coverage retained, live workflow log audit not performed |

All issue checkboxes remain unchanged. ADR 0005 is accepted only for synthetic
development. Juan Manuel Servera remains the named exercise Legal, Compliance
and DPO owner; real owners/sources remain a gap. No legal interpretation,
rule activation, consent, safety or financial approval is invented.

## Findings and routing

### RV-001: Live acceptance evidence remains unavailable

Severity: Medium, inherited residual evidence gap, not a correction defect.
Owner: human-controlled platform setup and separately authorized acceptance
work. Destination: distinct follow-up using the original PR acceptance audit,
not another correction or Review within this task. Required evidence:
protected environments, scoped federation/private runners, observed
what-if/release/apply and live runtime/log results. No automatic action.

## Next action

Parent records this single completed Review, commits/pushes the correction to
the existing PR without force, and leaves merge and issue acceptance to owner.
