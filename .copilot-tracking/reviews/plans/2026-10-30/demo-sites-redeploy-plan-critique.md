---
title: Demo sites redeployment final-candidate plan critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: f09558e0-64f4-4440-856f-8e9a302dbb6f
* Task: demo-sites-redeploy
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/demo-sites-redeploy-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one final-candidate critique; one complete actionable finding set.

## Inputs and Criterion Boundary

* Caller requirements: Rebuild and redeploy both demo sites from origin/main
  ffd8f35e63b24905b9aeb937dbf2a7fe9968747f, using the #542/#545 guardrails,
  within resource group ama. Renewed authority through November 15 is accepted;
  no renewed-authority question is raised.
* Preserve minima0, eight Manual jobs, ACR policies, existing live digests,
  app/auth configuration and revision history. No resource-group deletion,
  .env access, secret output, broad role, private endpoint, push or source/test
  additions or removals. Heavy work requires nonblocking lock admission;
  contention means defer, not wait or bypass.
* The authorized extension is the minimum existing-hub registry role for the
  verified operator and additive sensor-table initialization through the existing
  in-VNet job. SQL proof is counts/status/shape only; it does not authorize
  telemetry activation, row seeding, resident permission expansion or devices.
* Live Playwright/curl semantic checks and explicit blocked steps are required.
  Static assets, local regressions and anonymous health cannot substitute for
  authenticated feature acceptance.
* Primary evidence:
  .copilot-tracking/research/2026-10-30/demo-sites-redeploy-research.md;
  .copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md;
  infra/README.md, existing-hub and resident SQL/feedback-window sections;
  src/README.md, local RPI gate.
* Repository context: Original case study, addendum opening, reference-index
  opening and owner memory were read. Memory is context, not deployment evidence.
* Dependencies: Preservation preflight precedes mutation; lock admission
  precedes builds; restored ACR precedes app writes; committed SQL compatibility
  and restored jobs precede rollout; resident success precedes employee rollout;
  independent Review precedes local evidence closeout. Publication gates remain
  coordinator-owned and cannot be claimed by this local-only task.
* Assessment boundary: Supplied planning and historical evidence, not fresh
  Azure, GitHub, SQL, Docker or browser verification. No cloud commands,
  additional research, deployment, test execution or second reviewer were used.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| P01-T01; renewed authority; RG ama | Covered | Correct existing-resource scope and accepted November 15 authority; no deletion or infrastructure redeploy. |
| P01-T01; research C3; RBAC principal | Covered | Resolve current managed-identity oid without Graph /me; exact hub-scoped Registry Contributor to verified ServicePrincipal only if missing. The historical User example is not copied blindly. |
| P01-T01; research risk; cost limits | Partial | Authority and time limits are present; measured spend/headroom preflight is absent. PC-004. |
| P02-T01; immutable source; lock | Covered | Exact src archive, two correct Dockerfiles, source/config/manifest binding, unique tags, no untracked/.env input, nonblocking admission and defer. |
| P02-T01; research C1; ACR restoration | Partial | Finite exception and private-first cleanup are strong; cleanup-time concurrent drift needs the prior explicit no-overwrite rule. PC-001. |
| P02-T02; research C4/C5; SQL scope | Covered | Canonical conditional DDL, no configure/seeding, third GO batch only, transaction, shape/count/allowlist/SID/rights and impersonated 17-column proof. |
| P02-T02; ambiguity and job restoration | Partial | No automatic SQL retry is correct. Execution-bound commit evidence and safe restoration are underspecified. PC-001 and PC-002. |
| P02-T03; exact raw app/auth invariants | Covered | Image/suffix-only template PATCH, absent/null/secretRef preservation, separate auth, latest/ready/health/traffic and retained history. |
| P02-T03; startup failure and recovery | Partial | Logs before one old-image recovery, no tooling-triggered rollback and resident-first order are correct; explicit inherited recovery deadline and safe log output need carrying forward. PC-003. |
| P03-T01; named live UX | Covered | Named issue/PR matrix, desktop/narrow checks, authorized-session condition, protected-path denials, no authentication bypass or model smoke. |
| Source/test freeze; evidence boundary | Covered | Zero additions/removals, private external executors, evidence-only commit, semantic acceptance distinct from asset availability. No new test/source work is recommended. |
| P03-T02; Review and local persistence | Covered | One independent Review, originals preserved, no post-Review implementation, authenticated noreply identity, Refs and trailer, no push. Full gate/exact-head/hosted/human approval are not claimed. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 3 Medium, 0 Low.
* Rationale: The operational direction is credible and respects the renewed
  owner decisions. Four planner-owned corrections are needed to make cleanup,
  ambiguous SQL reconciliation, failure recovery and spending preconditions
  explicit enough for a private generated executor. None requires new source
  or tests, expanded cloud authority, or a further critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Restoration must not overwrite concurrent ACR or job changes

* Related IDs: P01-T01, P02-T01, P02-T02, P02-T03; research C1; prior Applied
  Critique Contracts PC-001 and PC-005.
* Evidence: The current details require restoring original ACR default/export
  settings and restoring "all eight full job definitions exactly." They require
  drift checks before writes, but do not define cleanup-time expected-state
  comparison. The prior details explicitly require closing public access first
  on ACR drift without overwriting unrelated changed fields, and restoring only
  the initializer's captured replicaRetryLimit configuration change.
* Concern: A preflight comparison cannot protect against drift occurring during
  the exception or SQL execution. Literal full-job restoration could write
  seven untouched jobs or erase another actor's legitimate change. Blindly
  restoring baseline ACR fields has the same lost-update risk. Exact final
  equality is an acceptance check, not permission to force equality.
* Impact: Cleanup can exceed the image/schema-only operational boundary and
  destroy concurrent configuration even while reporting restored invariants.
* Smallest useful change: Distinguish restoration writes from verification.
  Restore only this run's initializer retry field; verify the eight complete
  job definitions without PUT/PATCH of untouched jobs. Before each cleanup
  write, compare fresh state with baseline plus this run's recorded owned
  delta. On ACR drift, close public access first, remove only the owned
  normalized rule where safe, preserve unrelated changes and mark restoration
  blocked. On conflicting initializer drift, do not overwrite it. Block all
  dependent app writes until the restoration conflict is resolved.
* Action owner: Planning parent, specifying the executor contract for the
  implementation operator.
* Exact resolving evidence: Revised P02-T01/P02-T02 distinguish owned-field
  cleanup from full-resource readback, enumerate expected deltas, and specify
  fail-closed conflicting-drift outcomes. Implementation evidence must show
  sanitized pre-cleanup comparisons, actual owned-field writes and complete
  post-cleanup equality or an explicit blocked result; no source/test change
  is needed.
* Decision route: Direct planner correction; current owner direction already
  prohibits scope expansion. No user decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Bind ambiguous SQL reconciliation to the current worker and execution

* Related IDs: P02-T02, P02-T03; prior Applied Critique Contracts PC-001;
  research C4/C5.
* Evidence: Current P02-T02 says "COMMIT once" and "Ambiguous execution/write is
  inspected without repeat." The prior SQL contract additionally records worker
  SHA, one execution ID, attempt/completion, commit status and ordered
  column/count proof. These identifiers and the reconciliation success rule
  are not explicit in the new candidate.
* Concern: Existing conditional tables and an already-compatible view can
  satisfy shape/count checks even when the new execution failed or its COMMIT
  outcome is unknown. Conversely, client failure can occur after COMMIT.
  Read-only inspection is the right action, but object existence alone cannot
  establish this execution's completed transaction or permission checks.
* Impact: An ambiguous or failed initializer could be marked successful and
  release dependent rollout, or unnecessarily invite a later manual replay.
* Smallest useful change: Carry forward the execution-bound receipt contract:
  hash the current pinned worker/SQL inputs; record one execution ID and
  attempt; emit a post-COMMIT counts/status/ordered-shape marker; require a
  terminal successful execution and its bound proof. On uncertainty, inspect
  that execution and fresh permitted metadata without a second start, SQL
  reapply or compensating SQL write. If commit/proof cannot be established,
  keep SQL verification and dependent rollout blocked, even if tables exist.
  Cleanup remains required and is not evidence that SQL succeeded.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T02 defines the receipt fields and the
  succeeded, failed-before-commit and unresolved/possibly-committed branches.
  The eventual sanitized receipt binds the worker hash, execution ID,
  terminal result, post-COMMIT marker and principal/ordered-shape/count proof;
  unresolved evidence has an explicit blocked disposition.
* Decision route: Direct planner correction. Do not seek fresh authority or
  reinterpret no-retry as permission to repeat after a client timeout.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Make failure recovery finite and diagnostic output safe

* Related IDs: P02-T03; prior Applied Critique Contracts PC-002; no-secret-output
  requirement.
* Evidence: Current P02-T03 requires bounded console/system logs before one
  old-image recovery, but gives no numeric recovery convergence deadline.
  The prior employee recovery contract explicitly limits convergence to
  600 seconds. Current private-journal redaction mentions token-bearing calls;
  it does not explicitly cover application/SQL exception and diagnostic text.
* Concern: Bounded log collection does not bound recovery PATCH/polling.
  Collecting raw application diagnostics into ordinary output can also
  disclose secrets or resident/case data; private backup permissions alone
  do not sanitize output.
* Impact: Failure handling can run beyond its intended bound or violate the
  evidence/privacy limits while trying to prove a safe recovery.
* Smallest useful change: Explicitly inherit a maximum 600-second recovery
  convergence deadline for either app, with every request/poll bounded by the
  remaining time. If exhausted or ambiguous, stop mutations and report
  recovery verification blocked; do not make a second recovery attempt or
  touch the healthy resident after employee failure. Keep diagnostics
  size/time bounded and private, emit only reviewed sanitized status/type
  summaries, and ensure SQL exceptions cannot print SQL bodies, values or
  credentials.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T02/P02-T03 state the diagnostic-output rule
  and numeric per-app recovery deadline. Eventual failure evidence, if that
  path is exercised, records elapsed time, one recovery request identity,
  sanitized diagnosis and recovery/read-only-blocked result. An unexercised
  recovery path must be labelled unexercised, not validated.
* Decision route: Direct planner correction; no new recovery or logging
  authority is requested.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Renewed authority does not establish measured cost headroom

* Related IDs: P01-T01, P02-T01, P02-T02; research Risks and Residual Uncertainty;
  infra/README.md resident and existing-hub cost boundaries.
* Evidence: Research explicitly records that no actual all-in spend/headroom
  query was performed and renewed authority is not a measured cost statement.
  The supplied operations notes retain spending/headroom checks and cost stop
  conditions. The candidate preflight has configuration and source refusal
  conditions, but no disposition for that known financial evidence gap.
* Concern: A time-bounded ACR exception, min0 and one finite job are not monetary
  caps. Renewing the operational window through November 15 supersedes stale
  date restrictions; it does not prove that the existing ama spending envelope
  has remaining headroom.
* Impact: The executor can begin additional chargeable build/job/rollout work
  without checking a known prerequisite or recording it as blocked.
* Smallest useful change: Add an ama-scoped read-only spend/headroom preflight
  against the applicable owner-approved envelope, recording query time,
  available billing period/freshness, delayed-charge uncertainty and bounded
  incremental exercise estimate. Require available headroom before paid
  actions; if the applicable cap or evidence cannot be established, report
  that precondition blocked rather than inventing spend, treating min0 as a
  cap, or requesting broader access. Retain the renewed November 15 authority.
* Action owner: Planning parent for the precondition; implementation operator
  for its permitted execution evidence.
* Exact resolving evidence: P01-T01 names the existing cap/evidence source,
  scoped read-only check, admission condition and unavailable/insufficient
  headroom stop. Execution evidence contains the dated aggregate result and
  uncertainty or an explicit blocked step before chargeable work.
* Decision route: Direct planner correction now. Only an actual later request
  to increase spending authority would require a significant user decision;
  this critique does not request one.

## Strengths and Residual Risk

* The candidate correctly treats both sites as required deliveries, sequences
  resident before employee, and does not misreport recovery as delivery.
* It preserves the exact source pin and distinguishes a Docker index ID from
  actual configuration bytes. Remote manifest/source binding and old-digest
  retention are materially stronger than a successful tag push.
* SQL initialization is additive and transaction-bound, with no row seeding or
  consumer activation. Creating tables and granting registry permission cannot
  establish live Hub-to-SQL transport or resident sensor-gauge acceptance.
* The role target is the verified managed-identity service principal, not the
  historical human-user example. No broader role or network shortcut is
  justified by this critique.
* Missing credentials or authorized browser sessions legitimately block named
  authenticated steps. Anonymous health, shell byte equality and protected
  denials remain useful but narrower evidence.
* Existing SQL allowlist windows and secret validity are independent of renewed
  operation authority. No row, credential or expiry renewal is authorized here;
  any resulting UX blockage must stay visible rather than being repaired by
  scope expansion.
* No source/test changes are needed for these findings. Private generated
  executors and sanitized operational evidence remain the implementation
  mechanism. A local evidence commit does not establish publication readiness.

## Questions or Blocking Evidence Gaps

* No user response is required for this finding set.
* Runtime account/scope, current configuration, role propagation, billing
  headroom, terminal SQL outcome and authenticated sessions remain execution
  preconditions. Their absence must block their dependent steps, not prompt
  guessed success or broader permissions.

## Limitations

* Historical procedure and research reports were assessed as supplied; no
  fresh cloud state, manifest, budget, principal token, generated executor,
  database transaction or authenticated browser result was independently
  verified.
* The private historical executors and PR bodies were not separately reopened.
  Their behavior cannot be certified from prose. This is a plan credibility
  assessment, not an execution receipt, security audit or live acceptance.
* The requested shared lock path was assessed as a future execution
  requirement only; this read-only critique did not acquire it or perform any
  file operations there.
* Existing untracked planning/research/session inputs were left untouched.
  Only this requested critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise the ACR/job cleanup ownership and conflict
  contract, incorporate PC-002 through PC-004 in the same direct finalization,
  and record their dispositions without another critique pass.
* User response required: No.

## Next Steps

The active planning parent should finalize the plan/details with these four
planner-owned corrections and preserve this original critique unchanged.
Proceed to implementation only after the resulting preconditions pass; retain
explicit blocked outcomes where they do not. No additional reviewer, source
change, cloud action or user command is requested by this critique.
