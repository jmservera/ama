---
title: Independent final-candidate critique for demo-sites-redeploy-1031
ms.date: 2026-10-31
---

## Metadata

* Task ID: 975bbf93-de84-47b4-ad5d-b55583f970c9
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/demo-sites-redeploy-1031-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-1031-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique; no further agents.
* Candidate branch: chore/ops-redeploy-1031
* Deployment source: 4cb5964f7acce89668a37b5a56c3e125e26f6d21

## Inputs and Criterion Boundary

* Caller requirements: exact-main paired redeployment, full RPI loop, local
  commit and NO PUSH. Preserve original digests, complete protected
  configuration, private ACR baseline, eight Manual jobs and min0. Use an
  explicitly authorized shortest practical VM-IP-restricted ACR window, or
  evaluate az acr build if that route is unavailable. Initialize inside the
  existing VNet with counts-only evidence. Roll back on failure without
  overwriting concurrent changes. Resident AI stays OFF.
* Prohibitions: no source/test/auth/cache repairs, sign-in, private dataset,
  .env, secrets in evidence, new RBAC/endpoints, public SQL or RG deletion.
  Current execution instructions also prohibit file operations in temporary
  directories.
* Primary research:
  .copilot-tracking/research/2026-10-31/demo-sites-redeploy-1031-research.md.
* Supporting supplied evidence:
  .copilot-tracking/changes/2026-10-30/demo-sites-redeploy-1030c-changes.md;
  the retained latest ops/build/publish/sql_init/rollout/verify/export/asset
  executors and underlying guarded ops/publish/sql_init/rollout/verify
  executors identified by the caller and candidate. No raw configuration,
  auth, token or private data backups were opened.
* Source corroboration: src/api/src/zava_forward/api/static_assets.py;
  src/README.md local-gate and shared-lock guidance. Required project context
  was consulted; it does not supply additional cloud authorization.
* Decisions and dependencies: AC1-AC8 and P01-T01 through P03-T02 assessed
  once. Preservation precedes writes; registry publication and restoration
  precede SQL; successful SQL receipt and job restoration precede rollout;
  final deployment evidence precedes the single independent Review and local
  persistence.
* Boundary: operational plan credibility, executor compatibility, provenance,
  failure handling and truthful acceptance reporting. This is not a live
  cloud assessment, source review, authenticated acceptance exercise or
  publication gate. Historical successful execution is not current proof.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|----------------------------------------|----------|---------------------|
| Exact-main authority; AC1; P01-T01 | Partial | Correct source/archive/OCI chain contract; transitive adapter binding needs PC-003. |
| Private ACR; AC2; P01-T02 | Covered | DefaultDeny/owned VM32 rule, old manifests before/after, bounded close-first cleanup and stable full readback retained. Heavy-lock conflict is PC-001. |
| az acr build fallback; P01-T02 | Covered | Owner already authorizes evaluation after exact restore. Unsupported private prerequisites correctly block, rather than imply new RBAC or infrastructure authority. |
| Counts-only SQL; AC3; P02-T01 | Partial | One execution/replica/retry0, bound post-COMMIT marker and metadata checks are credible; cleanup classification needs PC-006. |
| Paired rollout; AC4; P02-T02 | Partial | Exact target readiness, preserved auth/history and drift guards are sound; pair-intent persistence needs PC-004. |
| Failure rollback; P02-T02/P03-T01 | Partial | Startup/pair failure recovery exists; late verification failures lack the explicit routing in PC-002. |
| Version/cache/auth; AC5/AC6 | Covered | Exact-main limitations recognized. HTML no-store is authoritative; long-lived asset caching and anonymous employee widget200 are not established. |
| Anonymous browser/dock; AC7; P03-T01 | Partial | Fresh desktop/mobile contexts and launcher/Escape scope are specified; inherited POST must be excluded under PC-005. |
| Evidence/Review/local commit; AC8; P03-T02 | Partial | Correct one-Review, Refs-only, privacy-safe identity and no-push boundary; current executor/export identity needs PC-003. |
| Resident AI OFF and prohibited changes | Covered | No inferred generated-prose/model/accounting authority; protected values preserved, no new infrastructure or source work. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 4 Medium, 0 Low.
* Rationale: The exact-main deployment direction is credible and authorized,
  including honest cache/auth limitations. Six bounded planner corrections are
  needed before implementation can safely reuse the historical procedure.
  None requires source changes, expanded cloud authority or another critique.
  PC-001 is an execution prerequisite blocker until a compliant shared-lock
  mechanism is established.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The proposed heavy-lock command is currently prohibited

* Related IDs: P01-T01, P01-T02; non-functional shared-heavy-lock requirement.
* Evidence: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-1031-phase-details.md:21;
  src/README.md shared-heavy-lock guidance; current caller execution context.
* Concern: The candidate explicitly opens /tmp/ama-rpi-heavy.lock. Historical
  acceptance or rejection of a temporary-path concern does not override the
  current explicit prohibition. Merely using an unrelated lock in the private
  root would also lose coordination with existing heavy work.
* Impact: The stated command cannot execute within this task's constraints;
  silently substituting an unshared lock risks concurrent resource-intensive
  builds/pushes.
* Smallest useful change: Replace the command with a compliant, demonstrably
  shared heavy-lock mechanism. If that cannot be established without prohibited
  file operations or unrelated tooling changes, stop before heavy work and
  report the technical blocker. Do not run the forbidden command.
* Action owner: Planning parent and deployment executor.
* Exact resolving evidence: Revised command plus read-only coordination
  evidence showing the chosen mechanism serializes the same heavy workload;
  actual acquisition/exit record before build/push, or explicit blocked status.
* Decision route: Direct planner correction. No user override of execution
  restrictions is requested or presumed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Rollback coverage ends before final operational verification

* Related IDs: Failure-rollback requirement; AC4/AC5; P02-T02, P03-T01.
* Evidence: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-1031-phase-details.md:53-75;
  supplied latest pair coordinator and underlying verify.py.
* Concern: The pair coordinator compensates exceptions inside its rollout
  loop. The later verifier is a separate invocation; unexpected public-body,
  version/provenance, health or protected-state failures raise without entering
  that coordinator. The plan says actual failure invokes recovery but does not
  assign late-failure classification and compensation to an executor.
* Impact: Both new revisions could remain deployed after genuine verification
  failure, contrary to the owner's rollback requirement.
* Smallest useful change: Specify the post-rollout failure handler and its
  scope. Unexpected target/health/public-byte failures must trigger guarded
  classification and eligible pair compensation using saved intents and old
  digests. Protected/auth drift or ambiguous SQL must stop unsafe writes and
  report unresolved recovery. Known no-long-lived-cache and employee401
  outcomes remain diagnostic, not rollback triggers. Export/commit failures
  alone must not blindly undo a verified deployment.
* Action owner: Planning parent; paired deployment executor.
* Exact resolving evidence: Updated P03-T01 failure-routing contract, named
  handler, and private adapter control-flow review showing every unexpected
  operational assertion reaches classification. Record actual recovery only
  if exercised; otherwise retain it as unproven.
* Decision route: Direct planner correction under existing rollback authority.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Reuse needs a complete current-task binding manifest

* Related IDs: AC1, AC8; research executor-reuse finding; P01-T01, P03-T02.
* Evidence: .copilot-tracking/plans/2026-10-31/demo-sites-redeploy-1031-plan.md Sources;
  phase details:17-18,80-87; supplied latest build.py and export.py.
* Concern: The latest build wrapper loads build() from a third retained session
  not named in the plan's two-root source inventory. Its fixed tag date is
  inside that imported function, not the wrapper. The retained exporter also
  contains historical destination/date/task/issue/outcome literals. Original
  and adapted hashes alone do not establish that all transitive inputs and
  resulting claims belong to this task.
* Impact: A superficially reused wrapper can retain stale identifiers, output
  placement or blanket-success claims even while deploying the right source.
  Missing historical dependencies may surface only after cloud writes.
* Smallest useful change: Before mutation, inventory and hash the complete
  selected dependency closure, including imported build() and standalone
  marker decoder. Name all current-task adaptations, pin SHA/root/tag/
  destination/task IDs, and replace historical exporter outcome/authority
  literals with this task's actual evidence and per-criterion dispositions.
  Compile private adapters without executing cloud actions. Fail closed if a
  required dependency is unavailable.
* Action owner: Planning parent and evidence adapter author.
* Exact resolving evidence: Current-task private dependency/adaptation
  manifest with original/current hashes and syntax/preflight results;
  sanitized export bound to task975bbf93, exact-main SHA, current output path,
  actual browser events and explicitly unmet acceptance checks.
* Decision route: Direct planner correction; private evidence adapters only,
  no application source/test changes.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Historical pair intent is not two pre-PATCH exact intents

* Related IDs: AC4; P02-T02.
* Evidence: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-1031-phase-details.md:54;
  supplied latest rollout.py pair-intent and underlying roll() implementation.
* Concern: The latest coordinator saves app/image lists before the loop, but
  each exact suffix/target/image roll-intent is created inside roll(), immediately
  before that app's PATCH. Thus employee's exact intent is not persisted before
  resident's PATCH, unlike the candidate's explicit promise.
* Impact: The recovery/restart contract relies on a persistence guarantee the
  selected executor does not actually provide.
* Smallest useful change: Allocate and persist both exact target intents before
  the first PATCH, then have roll() consume those intents without replacement.
  Also refuse overwriting existing intent/outcome files on a resumed invocation;
  reconcile current state read-only before deciding any remaining write.
* Action owner: Planning parent and pair-coordinator adapter author.
* Exact resolving evidence: Private adapter inspection showing both complete
  intent records saved before either forward mutation, plus journal order and
  retained intent hashes during execution.
* Decision route: Direct planner correction, not new deployment authority.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Unmodified anonymous verifier still submits a POST

* Related IDs: AC7; P03-T01; no-submission boundary.
* Evidence: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-1031-phase-details.md:75;
  supplied underlying verify.py resident /demo/assistant POST loop.
* Concern: The historical verifier submits a JSON question to /demo/assistant
  and expects401/403. The candidate's new boundary expressly says no
  submission, while named changes only cover rendered HTML and headers.
* Impact: Literal reuse would exceed the declared observational verification
  scope. A denied historical POST is not permission to submit one now.
* Smallest useful change: Explicitly exclude that POST from the current
  verifier adapter. Use GET checks and anonymous launcher open/Escape without
  Send/Enter/form submission; mark POST denial as historical or unexercised.
* Action owner: Planning parent and HTTP/browser adapter author.
* Exact resolving evidence: Current verifier method/path inventory contains
  no POST or submission; actual command/browser network evidence confirms the
  same observational scope.
* Decision route: Direct planner correction. No owner response needed.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: SQL cleanup assumes the retry-limit mutation took effect

* Related IDs: AC3; P02-T01; no blind write retries.
* Evidence: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-1031-phase-details.md:47-48;
  supplied underlying sql_init.py apply() finally block.
* Concern: Cleanup first asserts that the job equals the expected retry0
  definition. If the first PATCH fails without applying and the unchanged
  baseline has retry1, this assertion fails even though no restoration write
  is needed. It masks the original error and omits an authoritative baseline
  equality outcome. Concurrent drift must still block overwriting.
* Impact: An ordinary failed/ambiguous PATCH can leave job-restoration evidence
  unnecessarily unresolved; operators may be tempted to retry writes blindly.
* Smallest useful change: Classify the converged job as baseline unchanged,
  owned retry0 delta, or unrelated/unresolved drift. Accept baseline unchanged
  with eight-job readback and no write; restore only the owned delta; otherwise
  stop and preserve both original and cleanup failures. Do not start SQL or
  continue rollout merely because cleanup succeeded.
* Action owner: Planning parent and SQL execution adapter author.
* Exact resolving evidence: Updated cleanup decision table and private adapter
  control-flow inspection; actual terminal/eight-job equality records when
  available. No second init execution or cloud fault injection is required.
* Decision route: Direct planner correction within existing restoration scope.

## Strengths and Residual Risk

* Exact-main source authority is correctly stronger than a desire for green
  cache/auth checks. Asset Cache-Control no-cache, must-revalidate and HTML
  no-store are source-backed observations; versioned URLs alone do not prove
  long-lived caching. Employee widget401 is an intact anonymous boundary, not
  a deployment failure or anonymous widget200 acceptance.
* The short ACR exception is explicitly authorized. The retained publisher
  preserves defaultDeny/IP ownership, original digests, remote config/source
  chain, close-first cleanup and exact stable baseline readback. Record
  acknowledged enable/confirmed disable times, not an exact service-side
  exposure duration. A cleanup timeout blocks further work.
* The SQL receipt binds worker/input hashes, one replica, terminal Succeeded
  and a post-COMMIT marker. Historical522 is not a current hardcoded target.
  Transaction failures and ambiguous commit evidence remain blockers. Do not
  invent destructive SQL undo after a confirmed commit; app compensation and
  job-definition restoration are distinct from database transaction rollback.
* Read-only rendered HTML reconstruction must use the exact archived route/
  asset mapping, including assets that contribute to the shared version digest.
  Verify accessible versioned bodies/headers; shipped protected image bytes
  are provenance, not authenticated runtime/dock behavior.
* Original critique/Review outcomes remain immutable. Do not upgrade all
  acceptance criteria, close unmet issues, run another critique, or claim a
  full local/publication/hosted/human gate. This local-only task does not
  authorize push, PR, merge or source repair.
* Success-path execution cannot certify fallback, rollback or cleanup-retry
  branches. Missing prerequisites on az acr build remain a technical blocker;
  no fallback execution or new permissions are demanded merely for coverage.

## Questions or Blocking Evidence Gaps

* No significant or divergent owner decision remains unanswered in the
  supplied boundary. Existing authorization already resolves ACR fallback,
  rollback, exact-main deployment and AI OFF.
* PC-001 requires a compliant coordination solution before heavy execution.
  Unavailable transitive executors under PC-003 would also block execution.
  The planning parent can resolve or report these without repeat critique.

## Limitations

* No cloud mutation, browser replay, build, application test, commit, push or
  raw backup read occurred in this critique. Retained selected helpers were
  inspected read-only; syntax parsing of latest build/rollout/verify/export
  helpers passed, but does not certify their runtime behavior.
* Live restore/readiness/count/config claims must come from this task's fresh
  evidence. Historical records do not establish current service condition.
* This artifact is the only intended repository write. Plan, phase details,
  research and historical evidence are unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Resolve compliant shared locking and disposition all
  six direct corrections in plan/details, then proceed with the authorized
  implementation or record a technical block.
* User response required: No.

| Artifact | Description |
|----------|-------------|
| [.copilot-tracking/research/2026-10-31/demo-sites-redeploy-1031-research.md](.copilot-tracking/research/2026-10-31/demo-sites-redeploy-1031-research.md) | Supplied operational research and known limitations |
| [.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-1031-plan.md](.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-1031-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/demo-sites-redeploy-1031-phase-details.md](.copilot-tracking/details/2026-10-31/demo-sites-redeploy-1031-phase-details.md) | Assessed execution details |
| [.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-1031-critique.md](.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-1031-critique.md) | Single complete independent critique |

## Next Steps

The active planning parent applies or explicitly dispositions PC-001 through
PC-006 once, preserves this original Complete/Revise outcome, and advances only
after execution prerequisites are resolved. No user action, second critique,
peer-stage invocation or source/cloud change is performed by this assessor.
