<!-- markdownlint-disable-file -->
# RPI Plan Critique: demo-sites-redeploy-1030b

## Metadata

* Task ID: task870037be-e9ad-4240-8734-fa056bea01df/demo-sites-redeploy-1030b
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030b-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Supplied research: .copilot-tracking/research/2026-10-30/demo-sites-redeploy-1030b-research.md.
* Caller requirements: full ordered RPI; build pinned current main a72cb268e11f2fc744d299b2b72bdcb1e05b5d6f; reuse prior exact commands where permitted; existing redeploy authority and cost admission; local commit only, no push.
* Binding constraints: no new RBAC, private endpoints or public-network exception; no secrets, private rows, source/test edits, added tests or removed tests; no temporary-directory file operations.
* Decisions and dependencies: P01 backups precede builds; P02 publication is blocked by incompatible prior publisher and inaccessible existing private login; initialization and rollout depend on publication; P03 independently checks unchanged live sites and preservation. AI activation remains off.
* Assessment boundary: assess coherence, evidence sufficiency, protected-resource and secret boundaries, dependencies, acceptance criteria, truthful partial outcome and local evidence-only closeout. This is not authorization or verification of deployment, costs, model activation, live state, regulatory compliance or publication readiness.
* Repository context: startup index, owner memory and opening case-study/addendum context were read for orientation, not substituted for operational evidence. No additional operational investigation was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI / AC8 / P03-T02 | Covered | One critique, later independent Review, preserved original outcome, local Conventional Commit with references and trailer; no push, PR or publication receipt. |
| Source pin / AC1 / P01-T02 | Partial | Tracked git archive, two specified Dockerfiles, source/config hashes and revision label are credible; planned lock violates execution constraints, PC-001. |
| Preservation / AC6 / P01-T01 / P03-T01 | Covered | Full private app/auth/history/job/ACR snapshots; explicit absent resident auth handling; eight exact Manual definitions; four minima zero; stable-state comparison and unchanged history. |
| Research C3/C8 / AC2 / P02-T01 | Covered | Prior publisher's public exception conflicts with current prohibition; public 403 and confirmed login 10.40.4.21 TCP timeout support the supplied blocker, not permission for a workaround. |
| AC3/AC4 / P02-T02 | Covered | Initialization and rollout remain blocked; no worker start, SQL mutation or app PATCH; no rollback claimed without an owned rollout. |
| AC5 / P03-T01 | Covered | Bounded cold-start retries, anonymous curl/browser checks and source-byte comparisons distinguish existing-site health/version differences from new-source deployment. |
| Research C4-C7 / AC7 | Covered | SQL setting names do not prove accounting activation; absent enable/endpoint names, older sentence-selection scope and expiring allowance do not authorize generated prose. |
| Secrets / audit / P01-T01 / P03-T02 | Covered | Private full backups, permissions, names-only summaries, sanitized exports and hash-bound executor/raw evidence are planned; no secret values or OAuth query logging are authorized. |
| No source/test changes / local-only boundary | Covered | Maximum additions zero, removals none; actual builds and public checks are not proxies for rollout or authenticated acceptance; no publication gate claimed. |

## Verdict

* Verdict: Revise
* Rationale: The bounded partial-execution plan is otherwise credible and appropriately preserves the deployment blocker. One directly correctable execution-constraint conflict prevents the build phase from being executable as written. This verdict does not reopen network or AI decisions.
* Severity summary: 0 Critical, 1 High, 0 Medium, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The required build lock uses a forbidden temporary-directory path

* Related IDs: AC1, P01-T02, Non-Functional Requirements.
* Evidence: .copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030b-plan.md:68-70 requires /tmp/ama-rpi-heavy.lock; .copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-phase-details.md:32-34 repeats that path with flock -n -E75. Current execution constraints explicitly prohibit all /tmp file operations.
* Concern: Replaying the historical locking wrapper would open a forbidden path. Simply switching to a unique lock without coordination would also lose the intended shared-heavy-operation exclusion.
* Impact: P01-T02 cannot run as specified; bypassing the lock or substituting an uncoordinated one risks overlapping heavy work in the shared environment.
* Smallest useful change: Correct only the locking wrapper in plan/details to an admissible persistent, project-relative nonblocking lock with documented shared coordination. Preserve the pinned archive, Docker build commands and exit-75 exclusion behavior. If equivalent exclusion cannot be established within scope, mark the build blocked rather than touch /tmp or silently run unlocked.
* Action owner: Planning parent.
* Exact resolving evidence: Both plan and P01-T02 consistently name the permitted relative lock path and document how competing heavy executors share that coordination, or explicitly mark AC1/P01-T02 blocked pending equivalent exclusion. Subsequent implementation evidence must show the actual admissible flock invocation, exit status and both build results before AC1 is marked met; lock contention must remain a stop, not an unlocked retry. No execution is required to resolve the planning text itself.
* Decision route: Direct planner correction. The current constraint already decides against /tmp; no significant or divergent user decision and no new cloud authority are required.

## Strengths and Residual Risk

* P02 is deliberately unchecked, with AC2-AC4 unmet. Completing backups, builds and existing-site checks must leave the overall redeployment outcome blocked.
* No public exception, new endpoint, role, proxy or remote-builder workaround is inferred from old authority. Any future publishing route requires a separate authorized task with fresh drift/source checks.
* Retained image references and stable ACR configuration do not prove old manifest existence when the registry data plane is inaccessible; the plan explicitly retains that limitation.
* AI stays off. The older pilot's sentence-selection scope, USD20 allowance and 2026-11-01 expiry do not establish generated-prose authorization, live SQL accounting, remaining allowance or authenticated acceptance.
* Private evidence handling is a planned safeguard, not a verified property of the retained executors. The independent Review must inspect actual executors, raw evidence and sanitization before relying on the local record.
* A local evidence commit is not publication approval. No full local publication receipt, hosted checks, authenticated journey or accessibility/model acceptance is claimed.

## Questions or Blocking Evidence Gaps

* No user question is required for this bounded plan correction.
* The supplied private-login timeout/public denial and publisher conflict remain an accepted operational blocker, not a missing fact this critique can resolve.
* No alternative network route or AI activation is requested or recommended.

## Limitations

* Assessment used the supplied research, plan, phase details and caller context; cited historical executors and raw operational receipts were not independently inspected.
* No cloud, build, browser, model, Git publication or deployment operations were run. Freshness and completeness of reported observations remain implementation/Review evidence obligations.
* Only this critique artifact was written. Plan, details, research, source and existing evidence were not edited.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Resolve the locking wrapper directly, or explicitly block the build if equivalent permitted coordination is unavailable; finalize without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/demo-sites-redeploy-1030b-research.md](.copilot-tracking/research/2026-10-30/demo-sites-redeploy-1030b-research.md) | Supplied operational research and blocker rationale |
| [.copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030b-plan.md](.copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030b-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-phase-details.md](.copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-phase-details.md) | Assessed execution details |
| [.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-1030b-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-1030b-plan-critique.md) | This single independent critique |

## Next Steps

Planning parent resolves PC-001 directly, preserves this original Revise verdict,
and advances only eligible operations after finalizing the correction. P02 and
AC2-AC4 remain blocked; AI remains off. No second critique, user response, push
or publication handoff is required.
