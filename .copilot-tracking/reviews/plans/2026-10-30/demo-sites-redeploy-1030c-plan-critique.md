---
title: Fresh main two-site redeployment final-candidate plan critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: fc881d21-3ba8-4071-a186-c2dba4fa081e
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030c-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030c-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.
* Severity counts: Critical 0; High 1; Medium 2; Low 0.

## Inputs and Criterion Boundary

The supplied research, plan, phase details and current caller direction define
this assessment. Read-only Git inspection confirmed branch
chore/ops-redeploy-1030c and HEAD
252a498e2001193b0142b4f4ac031096dd6cc2b7. Existing untracked research, plan,
details and state were left untouched. No fetch was performed; equality with
freshly fetched origin/main and inclusion of PR #568 are supplied research
claims, not a fresh remote observation by this critique.

Supporting evidence was limited to the supplied prior-success pointers:
.copilot-tracking/changes/2026-10-30/demo-sites-redeploy-1030b-publish-changes.md,
.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-1030b-publish-plan-critique.md,
.copilot-tracking/reviews/logs/2026-10-30/demo-sites-redeploy-1030b-publish-review.md,
and the explicitly permitted prior executor files ops.py, publish.py,
sql_init.py, rollout.py and verify.py under the supplied prior session's
files/redeploy root. These scripts were read as text, not imported or executed.
Required case-study and knowledge-base context documents were consulted; they
do not grant operational authority.

The owner authorizes redeploying both existing demos through 2026-11-15 and
accepts USD337.19/700. The ACR-only short VM-IP public exception and exact
restoration/readback, including failure, supersede the earlier prohibition.
The fallback is az acr build, not a new network, RBAC, endpoint or execution-host
exception. Source must remain exact tracked main, both apps min0, all eight
jobs Manual with full definitions preserved, and config/auth/history backed up
and protected. No .env, private dataset, secret output or model call is allowed.
Generated-prose approval under the earlier sentence-selector pilot remains
unestablished; the implementation path keeps resident AI off.

The criterion boundary covers C1-C6 and the contrarian research conclusions,
AC1-AC8, P01-P03, dependencies, failure recovery, provenance, anonymous checks,
one independent Review, and local-only persistence. The critique assesses
planning credibility, not deployment success, current cloud state or approval
of a broader feature. Existing historical critique and Review outcomes remain
unchanged. This artifact contains the complete actionable finding set for this
boundary; no second critique is requested.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner decisions / research C1-C3 | Covered | Fresh source pin, existing authority, accepted cost, historical preservation and local-only outcome are explicit. |
| P01-T01 / AC1 | Partial | Exact tracked src, revision labels, unique tags, fresh builds and fresh backups are required; the shared lock instruction conflicts with the current execution constraint, PC-002. |
| P01-T02 / AC2 | Partial | Main-route manifest/config/source checks and restoration gates are concrete; the alternate build needs its own evidence mapping, PC-003. |
| ACR failure cleanup / AC2, AC6 | Covered | Inspected successful publisher includes an independent 600-second cleanup budget, deferred handled signals, ambiguous-close readback/retry, exact stable comparison and an explicit restoration-failed receipt. Actual cleanup remains an implementation obligation. |
| P02-T01 / AC3, AC6 | Covered | Pinned-source compatibility check, one counts/schema/view execution, retry0, standalone decoder, post-COMMIT receipt and eight full job comparisons are required. No AI accounting migration is inferred. |
| P02-T02 / AC4 | Partial | Individual-app intent, drift checks, cold-start budgets and recovery are concrete; pair-level compensation is not implemented by the script selected for reuse, PC-001. |
| P03-T01 / AC5 | Covered | Warm health, exact public asset bytes, fresh anonymous desktop/mobile contexts, denial checks and protected employee image-byte inspection preserve the public-only boundary. |
| Research C4-C5 / AC7 | Covered | Names-only inventory, no generated-prose authority assumption, AI-off path and separately held activation prerequisites are appropriate. |
| P03-T02 / AC8 | Covered | One Review, actual journal/browser binding, sanitized evidence, explicit-path local commits, fresh privacy-safe identity, Refs/trailer and no push are specified. |
| Tests / unchanged source | Covered | No application, infrastructure, dependency or test edits are planned; test removals and additions are none. The operations parent owns actual cloud/SQL/HTTP/browser checks. |
| Dependencies and unresolved live facts | Covered with findings | Builds and backups precede publication; exact ACR restoration and both remote proofs precede init/rollout; SQL commit/restoration precede rollout. Alternate-artifact proof and pair failure disposition require the revisions below. |

## Verdict

* Verdict: Revise
* Rationale: The main-route authority, source binding, restoration controls and
  honest anonymous-only acceptance are credible. Three substantive execution
  gaps remain: the promised two-app failure handling is absent from the reused
  executor, the selected lock location cannot be used in this environment, and
  the alternate build artifact lacks an equivalent provenance recipe. These
  are direct planner corrections within existing authority.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The reused rollout has no pair-level compensation path

* Related IDs: P02-T02, AC4, backup/rollback requirement.
* Evidence: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030c-phase-details.md:45-53
  directs reuse of rollout.py and recovery of an already-updated first app if
  the later app fails. The supplied prior rollout.py main loop calls roll or
  finish for each app sequentially, with no pair-level exception coordinator.
  recover handles only the app passed to it and raises even after successful
  original-image recovery. A prewrite failure for employee also exits the loop
  without visiting the already-delivered resident app.
* Concern: The detail states the desired pair outcome, but selecting the exact
  prior executor does not implement it. Its successful two-app history provides
  no evidence of cross-app compensation. "As necessary" does not define whether
  an employee not-applied failure, recovered failure or unresolved write should
  compensate resident, or how that compensation survives the deliberate
  recovery exception.
* Impact: The task can terminate with resident on the new image and employee on
  the old or unresolved image, contrary to its promised failed-pair handling.
  The parent may also mistake an intentional recovery exception for proof
  that all owned changes have been restored.
* Smallest useful change: Specify a bounded external wrapper or minimal
  execution-copy adaptation around the unchanged per-app procedure. Persist
  pair intent and each app's classified outcome. On a confirmed later-app
  failure, reconcile both apps before compensating any already-updated owned
  app; perform fresh protected/auth drift guards and a unique recovery intent,
  recover its backed-up original digest and verify readiness/history/config.
  Record each compensation result independently despite expected recovery
  exceptions. On unresolved state or unrelated drift, stop without overwrite
  and record the precise partial/unresolved pair rather than success. Cold
  timeout alone remains a read-only retry condition.
* Action owner: Planning parent; operations parent implements the external
  coordinator before rollout.
* Exact resolving evidence: Revised P02-T02 specifying these pair branches,
  followed before execution by a hash-bound wrapper/adaptation and static
  inspection showing first-app compensation, intentional exception handling,
  per-app reconciliation and guarded unresolved-state reporting. Actual
  forward or recovery receipts remain operations-parent obligations; no
  fault-injection or cloud replay is required by this critique.
* Decision route: Direct planner correction. The current owner already
  requires rollback; no divergent user choice or new authority is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The planned shared lock uses a prohibited temporary path

* Related IDs: P01-T01, P01-T02, non-functional requirements.
* Evidence: .copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030c-plan.md:55-56
  selects /tmp/ama-rpi-heavy.lock. The prior successful command recorded in
  .copilot-tracking/changes/2026-10-30/demo-sites-redeploy-1030b-publish-changes.md
  uses that lock. The current execution constraint prohibits file operations
  in /tmp or other temporary directories and requires new working files to
  be relative to the project.
* Concern: Exact historical-command reuse cannot include creating/opening that
  lock in the current environment. Omitting the lock or silently substituting
  a different per-session lock would not preserve shared heavy-runner
  exclusion.
* Impact: The build/publication command can be rejected before completion, or
  an ad hoc workaround can remove the intended coordination across heavy
  operations.
* Smallest useful change: Replace the forbidden location with one explicit
  permitted project-relative persistent lock, documenting this required
  environment adaptation alongside source/root/build substitutions. Confirm
  that relevant concurrent heavy runners use the same lock identity; if that
  cannot be established, stop rather than claim equivalent shared exclusion.
  Preserve the selected nonblocking contention behavior and lock lifetime over
  both builds and publication.
* Action owner: Planning parent and operations parent.
* Exact resolving evidence: Revised plan and P01 instructions naming the
  permitted lock and coordination prerequisite, plus the actual invocation
  showing that same lock held for the specified heavy operations. No file
  operation in a temporary directory is a resolving alternative.
* Decision route: Direct planner correction required by the execution
  constraint. No new deployment or spending decision is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The alternate builder lacks an independent artifact-proof recipe

* Related IDs: P01-T02, AC1, AC2, research fallback conclusion.
* Evidence: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030c-phase-details.md:29-31
  requires restoration before evaluating az acr build from the tracked archive
  with no role/network change. It does not specify the alternate submission,
  build completion receipt or alternate config binding. The supplied
  publish.py verify_images and push functions instead consume local
  build-proof.json, require the remote config digest to equal the retained
  local config digest and require a matching local Docker RepoDigest.
  The supplied prior critique PC-003 already distinguishes these artifacts.
* Concern: A remote rebuild from the same source need not yield the local
  build's config digest. The main-route publisher proof cannot certify the
  alternate artifact unchanged. The owner selected the fallback, but selection
  alone establishes neither its feasibility under private ACR restrictions
  nor the receipt that permits downstream rollout.
* Impact: If the short-window route is unavailable, the parent must improvise
  a decision-critical evidence path or stop with an incompletely specified
  authorized alternative. Treating the local config assertion as applicable
  could falsely reject a sound build or misbind the rollout proof.
* Smallest useful change: Add a conditional fallback recipe naming the two
  pinned Dockerfiles, src context, exact archive hash, source labels and unique
  tags, bounded terminal build handling and existing permissions/network/cost
  limits. Define a separate remote-build receipt and manifest/platform/config/
  label chain bound to the exact submitted archive; do not require equality
  to the independent local config or local RepoDigest. Preserve old-manifest
  verification, exact restoration/readback and a two-image proof schema usable
  by init/rollout. If proof collection or build execution is infeasible under
  current private access, stop with that evidence, without broadening access.
* Action owner: Planning parent; operations parent owns any actual fallback
  submission and remote verification.
* Exact resolving evidence: Revised P01-T02 with the fallback command recipe,
  evidence schema, AC1/AC2 mapping, terminal/restoration gates and fail-closed
  unavailable disposition. A live fallback build is not needed to resolve
  this planning gap; actual receipts are required only if that route is used.
* Decision route: Direct planner correction. Escalate only if later feasibility
  requires authority outside the already selected fallback; do not infer that
  expansion here.

## Strengths and Residual Risk

* The new exact source pin and fresh builds prevent reuse of historical image
  success as proof of PR #568 delivery.
* The prior publisher's safety adaptations address the earlier cleanup
  critique: close first, reconcile ambiguous closure, defer handled signals,
  retain an independent cleanup budget and block forward progress without
  exact restoration proof. No procedure can guarantee control-plane
  availability; explicit unconfirmed-restoration reporting remains necessary.
* Warm health and read-only same-target retry avoid classifying a single cold
  timeout as a failed deployment. The inspected rollout contains the stated
  900-second convergence and 180-second health-attempt handling.
* The private counts-only initializer and full job-definition comparisons
  preserve the data and scheduling boundary; current-source compatibility
  remains an implementation preflight, not a proven fact here.
* AI-off, generated-prose authority limits, employee sign-in restrictions,
  model-quality exclusions and human/accessibility acceptance limits are
  appropriately retained. Do not convert public asset/image-byte proof into
  authenticated Enter/Send acceptance.
* Accepted cost, standing authority and the narrow ACR exception are not
  reopened. Local evidence persistence is not push approval, issue closure,
  a full publication gate, hosted approval or human acceptance.

## Questions or Blocking Evidence Gaps

No unresolved owner decision blocks the three direct corrections. Live drift,
registry/build availability, source-compatible SQL success and app readiness
remain operational gates. If safe restoration or an authorized fallback is
unavailable, the operations parent must report the specific blocked state.
The prior original build wrapper outside the expressly permitted executor
root was not read; the supplied research and prior Review establish its
historical pointer, not a fresh-build receipt.

## Limitations

No cloud, build, browser, model, authenticated check or application test was
performed. No sensitive resource/credential file, .env or private dataset was
read. No private backup content was inspected. Source and infrastructure have
no tracked diff against the supplied HEAD; no test ownership was transferred
to this critique and no tests were added or removed. The operations parent
owns actual cloud/SQL/HTTP/browser checks and the later independent Review.
No plan, details, research, state or historical evidence was edited. This
critique neither commits nor pushes.

## Recommended Next Action

* Highest-impact finding: PC-001, pair-level compensation absent from the
  selected executor.
* Action owner: Planning parent.
* Smallest next action: Directly revise P02-T02 to require the bounded pair
  coordinator, and resolve PC-002 and PC-003 in the same finalization.
* User response required: No.
* Handoff: Return this one complete finding set to the active parent for direct
  revision/finalization without another critique.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/demo-sites-redeploy-1030c-research.md](.copilot-tracking/research/2026-10-30/demo-sites-redeploy-1030c-research.md) | Supplied fresh-source research |
| [.copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030c-plan.md](.copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030c-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030c-phase-details.md](.copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030c-phase-details.md) | Assessed execution details |
| [.copilot-tracking/changes/2026-10-30/demo-sites-redeploy-1030b-publish-changes.md](.copilot-tracking/changes/2026-10-30/demo-sites-redeploy-1030b-publish-changes.md) | Supplied prior successful operational record |
| [.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-1030b-publish-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-1030b-publish-plan-critique.md) | Preserved prior critique and corrections |
| [.copilot-tracking/reviews/logs/2026-10-30/demo-sites-redeploy-1030b-publish-review.md](.copilot-tracking/reviews/logs/2026-10-30/demo-sites-redeploy-1030b-publish-review.md) | Preserved prior independent Review |
| [.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-1030c-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-1030c-plan-critique.md) | This single final-candidate critique |

## Next Steps

The active planning parent should directly resolve PC-001 through PC-003 and
finalize the candidate without a second critique. No user action is required.
This critique stops here; it performs or authorizes no operational action,
source change, commit or push.
