---
title: Redeploy cache final-candidate plan critique
ms.date: 2026-10-31
---

## Metadata

* Task: demo-sites-redeploy-cache
* Task ID: 2c99fa13-81cb-4fd2-af53-81ad16cb565a
* Plan: .copilot-tracking/plans/2026-10-31/demo-sites-redeploy-cache-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-cache-phase-details.md
* Critique date: 2026-10-31
* Critique execution status: Complete
* Execution count: one independent final-candidate critique.

## Inputs and Criterion Boundary

* The current caller direction controls: full RPI loop; deployment authority
  through 2026-11-15; short /32 ACR window, private restoration and existing
  live digest protection; authorized private-compatible ACR-build fallback;
  min0, eight Manual jobs and full configuration backups; SQL only for a
  source delta touching SQL; AI OFF; no sign-in, secrets, .env, new RBAC,
  endpoints, public SQL or resource-group deletion.
* Sources assessed: the plan and phase details above;
  .copilot-tracking/research/2026-10-31/demo-sites-redeploy-cache-research.md;
  .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md.
* Project context read: docs/case_study_48_original.md;
  docs/case_study_48_addendum.md:1-110; docs/reference/README.md:1-100;
  docs/reference/memory.md. These are context, not new operational authority.
* Criterion boundary: P01-P03, their five tasks, AC1-AC7, research C1-C3,
  dependencies, stated decisions, failure boundaries, evidence persistence
  and local-only commit. No source changes or application test changes.
* The retained verifier and build function were read only to assess the
  exact pre-publication image-proof contract. No Azure, Docker, browser,
  network deployment or application validation was performed.
* This critique cannot establish actual live outcomes, fallback feasibility,
  signed-in acceptance or full publication/hosted/human gate completion.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Standing authority and prohibited changes | Covered | Caller direction and plan User Decisions; no contrary approval requirement introduced. |
| C1 / AC5 | Covered | Exact-year immutable public assets and no-store HTML require actual source-equal live receipts. |
| C2 / AC6 | Covered | Employee anonymous denial preserved; packaged bytes are not signed-in live200. |
| C3 / P01-T01 | Partial | Concrete-subdirectory fix retained, but verifier still requires a post-push receipt; PC-001. |
| P01-T01 / AC1 | Partial | Tracked archive/build binding specified; pre-publish local proof input needs adaptation; PC-001. |
| P01-T02 / AC1-AC2 | Covered | /32/defaultDeny, old manifests, close-first exact private restoration and conditional fallback. |
| Shared build/publish exclusion | Partial | Plan requires a forbidden /tmp lock location; PC-002. |
| P02-T01 / AC3-AC4 | Covered | Actual no-SQL disposition, fresh full eight-job guard, single-PATCH intents and protected pair recovery. |
| P03-T01 / AC4-AC6 | Covered | Long read-only convergence, real curl/browser state assertions and final baseline comparisons. |
| P03-T02 / AC7 | Covered | Current sanitized provenance, one Review, original outcomes retained, identity-safe Refs-only local commit. |
| Publication and acceptance limits | Covered | No push or whole publication, signed-in, model or accessibility acceptance claim. |

## Verdict

* Verdict: Revise
* Original verdict: Revise. Preserve this single execution and verdict;
  planner dispositions do not constitute another critique.
* Rationale: The operational boundary is credible, but the mandatory local
  image proof cannot run in its planned position using the retained helper
  unchanged. The shared lock contract also conflicts with the current
  environment's explicit filesystem restriction. Both are direct planner
  corrections, not requests to expand owner authority or acceptance scope.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Pre-publication image proof consumes a post-publication receipt

* Related IDs: C3, P01-T01, P01-T02, AC1.
* Evidence: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-cache-phase-details.md:29-37
  requires the original corrected image_assets() before the public window.
  The retained helper
  ../../../.copilot/session-state/975bbf93-de84-47b4-ad5d-b55583f970c9/files/redeploy/verify.py:116-124
  instead loads push-proof, iterates its images and requires item["digest"].
  The retained build function
  ../../../.copilot/session-state/f09558e0-64f4-4440-856f-8e9a302dbb6f/files/redeploy/images.py:49-52
  emits build-proof with local_id/config_digest, not the remote digest.
* Concern: A fresh current-session root has no current push-proof until
  P01-T02. Changing only SHA/root/tag and preserving the original
  image_assets() input contract therefore fails P01-T01. An old or fabricated
  push-proof would not establish current pre-publication image identity.
* Impact: The mandatory proof gate blocks implementation or tempts moving
  verification after the registry mutation, weakening the expressly required
  local-proof-before-cloud-write boundary.
* Smallest useful change: Explicitly adapt the local proof to consume the
  current build-proof's local_id/config_digest/source/archive binding.
  Preserve the concrete root/sub relative paths and byte comparisons.
  Keep remote index/platform/config/digest verification in P01-T02 and bind
  it to those same locally proven images; do not invent a remote digest
  before publication.
* Action owner: Planning parent; implementation parent owns the adapter.
* Exact resolving evidence: Revised P01-T01 details name build-proof as the
  pre-push input and separate local from remote receipts. The adapted helper
  has no pre-push push-proof/digest requirement; its later actual receipt
  binds both current local IDs and all packaged bytes to the current archive,
  with completion before the first registry network mutation.
* Decision route: Direct planner correction. Existing authority and scope
  already require this ordering; no significant or divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Required heavy-operation lock uses a prohibited filesystem path

* Related IDs: P01-T01, P01-T02, Non-Functional Requirements.
* Evidence: .copilot-tracking/plans/2026-10-31/demo-sites-redeploy-cache-plan.md:64-65
  mandates the shared /tmp/ama-rpi-heavy.lock. The current execution
  instructions explicitly prohibit any file operation under /tmp or other
  temporary directories. The prior #596 changes record that historical path;
  historical execution does not remove the current restriction.
* Concern: Acquiring the specified lock accesses a forbidden path.
  Silently dropping locking or choosing a unique per-session lock would
  instead lose shared build/publish exclusion.
* Impact: The stated command contract cannot be executed as written under
  current restrictions.
* Smallest useful change: Specify a permitted, non-temporary shared lock
  location, referenced relative to the working directory, with the same
  nonblocking contention behavior. Establish that relevant concurrent
  heavy-operation participants use that lock; if this cannot be established,
  stop before heavy operations rather than bypassing exclusion.
* Action owner: Planning parent; implementation parent establishes the lock
  contract before execution.
* Exact resolving evidence: Plan/details identify the permitted shared path
  and common-participant precondition; recorded actual build/publish argv
  uses that path. No /tmp access or isolated-lock substitution is required.
* Decision route: Direct planner correction to obey the execution boundary.
  No new deployment permission or significant/divergent user decision.

## Strengths and Residual Risk

* Fresh full baselines, old digest retention, exact ACR restoration and
  drift-guarded owned compensation are explicit prerequisites.
* SQL is correctly skipped for the supplied no-SQL delta; historical init
  or success-shaped SQL evidence must not be reused.
* Local proof, administrative errors and browser-tool defects are expressly
  outside healthy-app compensation. Timeout alone does not classify failure.
* Exact max-age plus immutable and post-undock state assertions address the
  supplied prior acceptance gaps without source or authentication changes.
* Conditional ACR fallback is not presumed successful. Missing existing
  support blocks that branch; it does not authorize network/RBAC creation.
* Actual live outcomes and unexercised recovery/fallback branches remain
  unproven until execution. This is an accepted verification boundary, not
  a finding demanding broader tests or new application tests.

## Questions or Blocking Evidence Gaps

* No unresolved owner choice is required for the two corrections.
* The supplied inputs support the bounded assessment. Live success and
  final exact invariants remain implementation evidence, not critique proof.

## Limitations

* Research claims about the source delta and current cache policy were
  assessed as supplied evidence, not independently re-run.
* Only the exact retained helper dependencies needed for PC-001 were traced;
  this is not a fresh audit or certification of all transitive executors.
* No app, cloud, browser, source or existing evidence artifact was mutated.
  Only this caller-designated critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct P01-T01's input contract and the shared lock
  path, record dispositions against this original critique, then finalize
  the plan without a second critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-cache-plan.md](.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-cache-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-31/demo-sites-redeploy-cache-phase-details.md](.copilot-tracking/details/2026-10-31/demo-sites-redeploy-cache-phase-details.md) | Assessed phase contracts. |
| [.copilot-tracking/research/2026-10-31/demo-sites-redeploy-cache-research.md](.copilot-tracking/research/2026-10-31/demo-sites-redeploy-cache-research.md) | Supplied research and decisions. |
| [.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md](.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md) | Retained #596 outcomes and corrections. |
| [.copilot-tracking/reviews/plans/2026-10-31/demo-sites-redeploy-cache-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/demo-sites-redeploy-cache-plan-critique.md) | Single original Complete / Revise critique. |

## Next Steps

The active planning parent applies direct PC-001/PC-002 corrections and records
their dispositions, then proceeds through the authorized RPI loop and its
remaining gates. Do not run a second critique. No user action is required.
