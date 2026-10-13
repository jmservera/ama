---
title: Account Switch Implementation Review
description: One scoped assessment of fixed selection, diagnostics, deployment and canonical learning
ms.date: 2026-10-13
---

## Scope and Evidence

* Task ID: zava-account-switch-2026-10-13.
* Scope: full P01, not a regrade of historical project or tenant-staff Reviews.
* Assessed boundary: fixed account selection versus ordinary sign-out,
  preserved authorization, five constant events, tested/deployed image and
  private configuration comparison, workflow investigation, canonical learning
  and existing PR publication. Actual authenticated replacement is excluded.
* Plan: .copilot-tracking/plans/2026-10-13/zava-account-switch-plan.md.
* Phase details: .copilot-tracking/details/2026-10-13/zava-account-switch-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-13/zava-account-switch-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-13/zava-account-switch-changes.md.
* Research: .copilot-tracking/research/2026-10-13/zava-account-switch-research.md.
* Documentation validation: .copilot-tracking/documentation/2026-10-13-session.md.
* Source/doc publication: baf6a5c; completion/evidence reconciliation a8f5458.
  Both pushed to the continuing open PR #65.

## Opening Review State

* Goal: compare completed approved P01 with its actual evidence once.
* Readiness: all P01 markers complete, details and changes reconciled, single
  critique disposed, local/deployed validation and exact source-head CI present.
* Acceptance basis: plan requirements/criteria, confirmed owner direction and
  PC-001/002 resolving evidence; no inherited product approval.
* First comparison: fixed source redirects and event gates versus auth tests,
  then deployment, preservation, documentation and workflow evidence.
* Read-only boundary: only this review record may change; no source, plan,
  details, changes, research, directory or Azure mutation.
* Initial blockers: none for the scoped task. Existing-session owner acceptance
  and retained tenant naming remain distinct follow-ups.

## Execution Status

* Execution status: Complete.
* Outcome: Conformant for the approved P01 boundary.
* Review execution evidence: canonical opening persisted before comparison;
  no separate lens agent required for this continuous bounded trace.
* One final-candidate critique and one post-implementation Review; neither is
  repeated. This verdict does not close authenticated-browser, full-product,
  capstone, pilot or production acceptance.

## Reconciliation and Completed-Work Assessment

| Boundary | Assessment and evidence |
| --- | --- |
| P01-T01 fixed selection | auth.py separates switch from ordinary logout. server.py accepts only the single blank-aware switch=1 flag, appends fixed select_account and keeps the fixed /app return. Existing app.js follows the server redirect; no client rewrite was necessary. |
| Preserved behavior and access | Ordinary platform logout and development-password behavior remain. Authorization precedes successful workbench arrival; authenticated POST markers follow the existing CSRF gate. Existing tenant, role and staff-oid checks were not relaxed. |
| PC-001 diagnostic proof | All five complete constant messages are asserted in test_auth.py. Rejected authorization/CSRF requests produce no new successful-flow markers. Normal/picker GET messages were collected live; authenticated POST/arrival remain synthetic evidence, not fabricated Azure activity. |
| PC-002 rollout proof | Changes records the tested image digest, ready revision 0000009, private app/auth comparison and two rollback gates. SQL and tenant assignments were not rewritten by this image-only deployment. |
| P01-T03 learning and publication | PRD learning dispositions, ADR 0002 identity/session mechanics, dated addendum observations, operator guides, index and append-only log reflect the observed boundary. Historical proposals, requirement counts and pending approvals remain. No new business evidence warranted a BRD edit. |
| Completion and handoff | All P01/task markers are complete; details, changes and plan handoff reconcile the same source/image/validation boundary. No active implementation blocker remains. Both plan follow-ups stay outside P01 and its acceptance claims. |

## Implementation-Time Updates and Critique Disposition

* PC-001 and PC-002 were applied directly in the plan/details before delivery.
  Their resolving evidence is present in tests and deployment records. No
  unresolved significant or divergent decision requires owner approval.
* Keeping blank query values implements the approved exact-single-flag
  requirement; it prevents a blank duplicate from enabling switching.
* The private operator comparison normalizes only absent/empty value fields
  beside unchanged secretRef entries. The first rollout rejected this
  platform normalization and restored the prior image; the narrowed semantic
  comparison retains every nonempty value, reference and authentication
  setting. This preserves the approved invariant, not a weakened drift gate.
* All-replica polling replaces premature reliance on latestReadyRevisionName.
  The intermediate gate rolled back rather than accepting unready replicas.
  This is operational validation refinement, not a new product behavior.
* The owner's documentation addition is reflected in P01-T03 and its final
  critique boundary. It changes neither business requirements nor acceptance
  authority. Canonical learning distinguishes reports, observations, proposals
  and pending personal acceptance.

## Validation Evidence and Latest Retry Inspection

| Check | Result and limit |
| --- | --- |
| Targeted auth | 23 passed; fixed flags, all five messages, denied requests and local-password regressions. |
| Full MVP | 289 run, 26 existing skips, no failures. Skipped coverage is not claimed passed. |
| JavaScript syntax and local image | Passed; existing client code and read-only non-root image health/logo/ordinary-login/chooser checks. Named smoke container was cleaned. |
| Live Azure | Deployed tested digest sha256:8cf327786ac2b891a586e78981b4abf0cc9c86313d721cef74ea7fcda80fa599, account-switch-20261013-01, ready revision 0000009. Supplied private comparison and HTTPS evidence establish configuration preservation and forwarded select_account, not a selected user's replacement session. |
| Logs | Existing ContainerAppConsoleLogs collected fixed normal/picker events. New messages contain constants only; pre-existing denial/platform logs are not claimed identity-free. |
| Canonical documentation | Supplied check resolved 23 new links/anchors and found no private selected identities in seventeen changed files. Original case, owner memory and regulatory snapshots remain unchanged. |
| Exact source CI | baf6a5c passed MVP CI 38368944188 and both validation workflows. Later evidence-only head a8f5458 passed MVP CI 38369565686, MVP validation 38369565658 and Prototype validation 38369565827. |
| Scorer and retry request | Scorer 38369565640 completed all jobs successfully for a8f5458; custom rubric/score also reports SUCCESS. Recorded score is 46/100, not full capstone acceptance. No duplicate successful run was restarted for the owner's retry request. |
| Subsequent bot-only head | 65be699 modifies only the rubric badge/score. Its workflows report action_required; inspected MVP CI has no executed jobs. This is neither a test failure nor a claim that bot-head checks passed. |
| Personal browser acceptance | Unavailable: no already-authenticated owner session was supplied. Anonymous Microsoft Sign in and synthetic claims cannot prove a changed account, workload or photo. Routed separately below. |

The original reported scorer job failed with Copilot provider HTTP 403; the
owner's attempt 3 succeeded. Later successful execution does not prove that
the original failure was transient or justify credential rotation.

## Findings and Follow-Up Routing

No material implementation defect or unaccepted decision gap was found.
Defect severity summary: Critical 0; High 0; Medium 0; Low 0.
The following Low-severity residual entries route the existing plan follow-ups;
they are not defects or new active implementation tasks.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Owner authenticated account-replacement acceptance

* Evidence: plan Follow-Up Items, changes live-flow limit and PRD
  review-learning disposition explicitly leave actual session replacement open.
* Impact: the deployed chooser is evidenced, but an existing session changing
  to another authorized person and showing that person's permitted work/photo
  is not yet observed.
* Destination: distinct owner acceptance follow-up, ranked first for small
  effort and immediate confirmation of the reported symptom.
* Next action: start already signed in, use another account, choose a different
  authorized person and verify the returned current-account/work view. Record
  only pass/fail observations, not credentials, cookies or directory names.
  If it fails, route the narrow observed symptom to later research; do not
  silently add global logout or relax authorization.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Retained tenant naming remains separately scoped

* Evidence: the same prior follow-up is retained in plan Follow-Up Items and
  the changes record; this task changes neither directory naming nor role
  permissions.
* Impact: account-selection conformance does not certify every retained tenant
  label or historical compatibility name as migrated.
* Destination: distinct naming follow-up, ranked second because it needs a
  separate evidence/scope boundary and has less immediate value than proving
  account replacement.
* Next action: owner selects this workstream before any directory mutation;
  a child Research phase separates required current names from preserved
  historical/compatibility references. No new discovery was done merely to
  populate this choice.

## Outcome and Parent Handoff

Execution Complete; outcome Conformant for P01. No active blocker or source
fix is routed. RV-001 and RV-002 remain distinct, non-blocking owner follow-ups.
Human acceptance is not marked complete. Return this one Review to the
automatic parent, which persists completion and Follow-up while keeping its
session running, publishes the record and offers only supported choices.
