---
title: Operator suspension 221 final-candidate plan critique
description: Independent bounded engineering credibility assessment and resolving evidence
ms.date: 2026-10-20
---

## Metadata

* Task ID: 221.
* Critique date: 2026-10-20.
* Plan: .copilot-tracking/plans/2026-10-20/operator-suspension-221-plan.md.
* Phase details: .copilot-tracking/details/2026-10-20/operator-suspension-221-phase-details.md.
* Research: .copilot-tracking/research/2026-10-20/operator-suspension-221-research.md.
* Critique execution status: Complete.
* Verdict: Revise.
* Severity summary: 4 High, 3 Medium; 0 Critical, 0 Low.
* Observed branch: feat/operator-suspension-221.
* Observed HEAD and supplied base: 7e95f0224bfb7a8a62990a1de162fbcfa68db539.
* Scope: one independent final-candidate critique, not implementation or an implementation Review.

## Inputs and Criterion Boundary

The exact canonical research, plan and phase details above were assessed
together, against the caller's bounded synthetic direction and actual source.
The initial worktree contained untracked current research, plan, details and
session artifacts. They were treated as supplied candidate inputs and left
unchanged. This assessment writes only this critique.

Requirements considered:

* PRD FR-053 and AC-072: a seeded critical incident or an approved threshold
  breach, dispatch and pending/ready reliance denial, affected versions and
  owner, manual/hazard continuity, corrective tests and distinct authorized
  human approval.
* BRD RULE-024, AC-078 and OD-35: scope, owner, evidence, containment, resident
  impact, remediation and restart authority; OD-35 and relevant RULE-020
  acceptance before affected work restarts.
* Canonical research C1-C8, the plan's AC1-AC6 and persistence/gate criteria,
  P01-T01 through P02-T02, test ownership and the 18-new-method ceiling.
* Existing continuity, release selection/reference/runtime binding,
  trusted-proxy OID-bound capabilities, current-actor validation, checked SQL
  document writes, export projections and continuity test harnesses.
* Original adverse issue #219 Review and its later bounded correction Review.
  Merged primitives are not whole-issue acceptance or evidence that OD-35 has
  been appointed.

Project context was read from docs/case_study_48_original.md,
docs/case_study_48_addendum.md, docs/reference/README.md and
docs/reference/memory.md. Source-level references below are workspace-relative.
No external research, remote action, test execution, source edit, nested agent
or git mutation was performed.

The criterion is implementation credibility for bounded engineering, not
live activation, actual authority appointment, representative evaluation,
regulatory satisfaction, issue closure or publication acceptance. The caller
already resolves the authority question: unknown/unapproved actual authority
must fail closed. No finding asks the planner to invent an approval protocol,
approve a threshold, select a real holder or expand into issue #222.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR-053 / AC-072; AC1 | Partial | Dispatch/reliance consumers exist; exact relevant-history migration and snapshot boundary need PC-003/PC-004. |
| RULE-024 / AC-078; AC2 | Partial | Required incident fields are enumerated, but capture completeness and distinct incident/corrective version snapshots are unresolved: PC-002/PC-003. |
| FR-028 / AC3 | Covered in intent | Actual manual mutation and hazard intake tests are explicitly required; existing note-only assertions are not sufficient evidence. |
| AC4 / AC5; OD-35 / RULE-020 | Partial | Separate capability is appropriate, but no executable fail-closed actual/constructed decision contract is frozen: PC-001/PC-002. |
| AC6 / synthetic fallback drill | Partial | Constructed distinct actor is explicit; must demonstrate persisted actual-provider denial, not only fixture labels: PC-001/PC-006. |
| C2/C4/C5; contract reuse | Covered in direction | Existing release references, continuity document, ledger and optimistic SQL writer are appropriate; no new incident table is needed. |
| C3; task-aware epoch consumers | Partial | Relevant-task intent is right; independent raw claim-epoch comparison and old document behavior need PC-004. |
| C6; identity/capability | Partial | OID-bound separate permission is feasible; trust source, current-actor binding and limits of commit revalidation need PC-001. |
| C7; native SQL / persistence / rollback | Partial | Existing harness is reusable but proposed gate selection cannot run it as written: PC-005. |
| P01-T01 | Partial | Resolve PC-001 through PC-004 before implementation. |
| P01-T02; locked tests | Partial | Resolve native execution and exact method allocation: PC-005/PC-006. |
| P02-T01 | Covered in direction | Preserve failures and unmet human acceptance; component documentation is correctly in scope. |
| P02-T02 | Partial | Original Review and committed freeze order are appropriate; gate filesystem prerequisite is blocked under current instructions: PC-007. |
| C8; prior adverse Reviews / whole #219 | Covered | Preserve original RV findings and later correction evidence; do not relabel their history or close human acceptance. |

## Verdict

Revise. The chosen architecture and bounded scope are credible, but the
candidate is not yet a sufficiently frozen implementation contract. In
particular, identity permission is not actual authority, a structured
self-reported result is not approved corrective evidence, and an existing
actual release could become admissible again if a constructed restart merely
clears the shared continuity hold. Native SQL coverage is also not executable
through the described gate route.

These are direct planner corrections within the caller's confirmed direction,
not reasons to seek a new authority decision. The complete actionable set is
PC-001 through PC-007. The planning parent should dispose it once, preserve this
original critique and finalize without another critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Actual-authority denial and constructed restart need an executable persistent boundary

* Related IDs: AC4, AC5, AC6; RULE-024/OD-35/RULE-020; C1/C2/C6; P01-T01.
* Evidence: plan lines 53-58 require the right outcome but details lines 23-29
  specify only a new claim and immutable binding. In
  src/core/src/zava_forward/core/continuity.py:185-215, Restart changes status
  to Restarted and increments the epoch; active() checks only Suspended.
  src/core/src/zava_forward/core/assistants.py:478-494 reads suspension and
  release admission separately. src/core/src/zava_forward/core/rai_release.py
  selects valid active actual releases independently of OD-35. The current
  auth mapping grants capability only for uniquely OID-bound principals, but
  the continuity HTTP route currently performs no corresponding capability
  boundary.
* Concern: There is no decision table saying what evidence permits a
  constructed-only restart, what remains unavailable for actual restart,
  where that distinction persists, and which runtime consumers enforce it.
  Merely marking a restart synthetic or adding a privileged claim cannot
  stop an existing active actual release from becoming usable when the
  continuity hold clears. A provider switch or later release replacement
  must not erase this boundary either. Body strings, seeded fields and an
  actor's self-attestation cannot establish the missing actual approval.
* Impact: A superficially passing synthetic drill could restore actual
  dispatch or retained reliance without OD-35/RULE-020 acceptance.
* Smallest useful change: Freeze the restart eligibility matrix and
  persistent constructed-versus-actual semantics in P01-T01. Keep actual
  restart unavailable while actual appointment/acceptance is unproved.
  Define the reuse of existing continuity/release gates that preserves this
  denial even after a constructed-only decision, release replacement,
  provider switch and reopen. Specify the trusted HTTP-to-core permission
  source, current registered OID/role checks, distinct-human comparison and
  the dedicated claim; reject password/email-fallback/body/default grants.
  Bound SQL commit revalidation to locally verifiable staff/OID/role and
  trusted request capability facts. Do not imply offline SQL can prove
  current Entra claim revocation or actual professional appointment.
* Action owner: Planning parent; core/API implementer executes the frozen rule.
* Exact resolving evidence: A plan/detail truth table covers missing and
  unapproved actual authority, caller-claimed approval, constructed evidence
  with/without separately provisioned permission, and an actual-provider
  release before/after constructed restart. Named tests exercise the real
  decision and dispatch/reliance paths with zero actual-provider calls, both
  immediately and after reopen/provider or release change; trusted distinct
  constructed permission permits only the explicitly bounded fixture path.
* Decision route: Direct planner correction. The user has already required
  fail-closed actual authority; no user response is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Freeze the corrective evidence interface and separate incident versions from remediation candidates

* Related IDs: AC2, AC4, AC5; C2/C3/C5; P01-T01.
* Evidence: plan lines 49-52 and details lines 26-27 say structured, immutable
  and version-bound without defining the stored or request interface.
  continuity.restart_propose currently accepts one corrective_evidence
  string. assistant_release.BOUND, assistants.runtime_binding,
  ai_registry.legacy_binding and rai_release.reference already define the
  reusable serving bindings and exact release id/version/digest.
* Concern: The plan leaves the evidence schema, validation, server-owned
  fields, result semantics and exact compare-at-decision rule to the
  implementer. It also conflates the incident's immutable impacted versions
  with the version set that a correction is meant to release. Requiring
  equality to the original broken version prevents legitimate versioned
  remediation; accepting a new version without re-proposed evidence allows
  stale corrective claims. An arbitrary result="Pass" plus evidence text
  must not become approved actual corrective testing.
* Impact: Restart can accept malformed, stale or self-certified evidence, or
  valid remediation can be permanently unrepresentable.
* Smallest useful change: Specify one bounded extension inside the existing
  continuity proposal/decision record. Preserve incident-time affected
  versions separately. Freeze the corrective candidate at proposal time
  using server-derived canonical task scope, incident identity/relevant
  fence, exact selected release references and existing full runtime
  bindings. Define mandatory corrective-test identifier/reference, result,
  evidence class, recorder and server timestamp, validation limits and
  explicit unknown/unavailable representation. Copy/hash the stored
  candidate/evidence immutably; do not trust caller binding digests.
  Recompute and compare under the deciding transaction. Candidate drift,
  release replacement, absent bindings or altered evidence deny and require
  a fresh proposal; preserve prior evidence rather than overwrite history.
  Human-recorded constructed results stay labelled claims, not server-run
  evaluations or actual acceptance.
* Action owner: Planning parent with the existing core contract owner.
* Exact resolving evidence: A concrete field/ownership/type table and
  decision algorithm in the details, reusing existing release primitives.
  The test allocation includes malformed/failed/missing evidence,
  changed model/prompt/policy/data/permission/runtime binding, replacement
  release, request/stored-evidence mutation and a positive freshly re-proposed
  corrected candidate while retaining original incident versions.
* Decision route: Direct planner correction; no new domain evidence protocol
  or actual appointment is authorized.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Impacted version evidence is collected outside the incident transaction and may be truncated

* Related IDs: AC1, AC2; FR-053/AC-078; C3/C4/C5; P01-T01/P01-T02.
* Evidence: src/api/src/zava_forward/api/server.py:853-854 calls
  app.assistants.affected before store.suspend acquires its lock.
  assistants.affected at lines 511-521 uses another transaction, a default
  500-row limit and only id/task/registry version/state.
  continuity.suspend stores that supplied list and counts; legacy affected
  rows retain only envelope task_version. Existing release reference and
  serving bindings are not captured there. The plan promises impacted
  proposal/version persistence but specifies no capture/revalidation boundary.
* Concern: A task can be enqueued or change state between collection and the
  suspension commit. A truncated list is not the entire impacted set, and a
  registry/task version is not the affected release/model/prompt/policy
  binding. Correct enforcement can therefore coexist with incomplete or
  misleading incident evidence.
* Impact: AC2 and version-bound corrective review are not reconstructible
  even if dispatch itself correctly stops.
* Smallest useful change: Define how existing SQL transactions/checked
  continuity publication establish a consistent suspension boundary and
  server-derived release snapshot. Either capture the affected set at that
  boundary or retain explicit bounded/incomplete status plus a durable
  reconstructible boundary/reference; never imply a truncated list is full.
  Missing or incomplete version evidence must not prevent immediate
  containment, but cannot qualify restart. Specify JSON unsupported release
  evidence explicitly rather than invent a release snapshot.
* Action owner: Planning parent; core/API transaction implementer.
* Exact resolving evidence: Details identify the actual collection/write seam
  and retained exact release references. Tests inject enqueue/claim/completion
  between collection and commit, exercise truncation and legacy/current task
  snapshots, reopen the incident and show both durable containment and honest
  impacted-set/version completeness. Restart refuses an insufficient frozen
  candidate.
* Decision route: Direct planner correction using existing transactions and
  release contracts, not a duplicate incident store.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Relevant-history validity must replace every independent global comparison

* Related IDs: AC1, AC4; C3/C4/C7; P01-T01.
* Evidence: details lines 31-34 establish the desired task-aware behavior.
  continuity.epoch_current currently takes only a record and global integer;
  continuity_publish independently compares epoch != doc["epoch"].
  assistants.complete at lines 869-873 additionally compares the current
  global epoch with claim_epoch even after epoch_current.
  Legacy consumers in ai_tasks.py/store.py and export also make their own
  currentness decisions. Existing documents have suspension epoch and restart
  new_epoch, but no new history format or migration contract yet.
* Concern: Updating the helper alone still quarantines unrelated in-flight
  work. Conversely, relaxing equality without a precise relevant-change
  rule can revive pre-incident output. The candidate does not define validity
  for old persisted documents, future/malformed epochs, overlapping all/task
  incidents, or incomplete relevant history.
* Impact: Unrelated-task preservation or historical non-revival can fail
  depending on which consumer handles the same record.
* Smallest useful change: Freeze one pure relevant-history contract over the
  existing document, canonical task and captured epoch, including suspension
  and restart boundaries, all-scope overlap and fail-closed legacy/malformed
  behavior. Name the claim/completion/publication/cache/review/list/export
  callers and raw comparisons to migrate. Preserve lease fences, release
  binding checks and monotonic event ordering.
* Action owner: Planning parent; continuity and consumer implementer.
* Exact resolving evidence: One shared validity definition and explicit
  consumer checklist, with tests proving unrelated ready, accepted and
  in-flight work survive a task-only cycle while relevant historical work
  never revives; include all-scope overlap and old/missing/future epoch data
  through runtime views and export.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: The existing gate cannot execute the proposed optional native SQL selector as described

* Related IDs: C7; native SQL acceptance; P01-T02/P02-T02; locked test targets.
* Evidence: tools/rpi-checks.py:28-36 fixes SQL_SELECTORS to test_mssqlstore
  and selected test_assistants classes, not the owning continuity modules.
  Runner.sql supplies ZF_TEST_MSSQL and owned endpoint credentials, then
  removes its container at lines 1361-1362. Extra selectors run later at
  lines 1530-1544 with tests_env only, which supplies PYTHONPATH.
  Existing continuity OwnedMssql requires ZF_CONTINUITY_MSSQL and
  ZF_ISSUE122_OWNED_SQL; neither is supplied by that SQL gate.
* Concern: "Explicitly selected by full gate" is not an executable route.
  Adding --extra-test for the opt-in continuity class will lack both its
  required opt-in/ownership environment and a running owned SQL endpoint.
  Ordinary discovery skips are not native transaction evidence.
* Impact: Required native race/rollback/reopen checks cannot be claimed from
  a full17 receipt using the planned test ownership alone.
* Smallest useful change: Freeze an executable SQL ownership route before
  implementation. A narrow option is an explicitly named bridge method in
  an already selected test_assistants MSSQL class, invoking the issue-owned
  semantic helper under that class's existing owned fixture; include that
  one bridge in the locked targets and method budget. Otherwise explicitly
  scope a reviewed runner-and-receipt-contract extension, not just an extra
  selector. Do not borrow configured credentials, weaken ownership checks,
  change check names or claim an opt-in skip as success.
* Action owner: Planning parent; existing SQL harness/gate owner for the
  selected route.
* Exact resolving evidence: Details name the exact selected class.method,
  fixture, opt-in and connection source, and show how the existing native
  gate invokes it before container cleanup. Implementation evidence must
  retain a non-skipped named native test with actual commit, rollback,
  conflict, reopen and retained-denial assertions. If unavailable, keep this
  validation explicitly blocked.
* Decision route: Direct planner correction. Expanding test ownership for a
  minimal existing-harness bridge does not authorize a new production contract.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: The 18-method ceiling has no locked requirement-to-method allocation

* Related IDs: AC1-AC6; P01-T02; Test Ownership and Locked Targets.
* Evidence: plan lines 98-110 state a maximum and two owners plus an optional
  module; details lines 39-44 enumerate scenarios without methods or
  fixture ownership. Existing restart helpers accept arbitrary references;
  test_manual_fallback_and_hazard_work_continue currently checks suspension
  and explanatory text, not a manual mutation or hazard intake.
* Concern: The positive helpers need coordinated migration without a
  production bypass. The safety and persistence matrix, HTTP capability
  checks and PC-005 native bridge have not been allocated within the cap.
  An accidental test expansion or deletion of old positive controls is
  discoverable now, rather than an implementation-time scope surprise.
* Impact: The parent cannot verify bounded test delivery or whether all six
  ACs have semantic evidence instead of descriptive assertions.
* Smallest useful change: Lock a numbered list of at most 18 new method
  names and owning files, including any native bridge, with matrix-driven
  subcases where appropriate. Name existing helper/method updates separately
  and state no removals. Allocate real manual/hazard writes, provider-count
  assertions, actual-versus-constructed denial, relevant-task completion,
  evidence drift, restart denial audit, failure/rollback and reopen coverage.
  Keep the optional issue module count at one and add no UI.
* Action owner: Planning parent; owning API test implementer.
* Exact resolving evidence: Plan/details contain the fixed allocation,
  AC/finding mapping, fixture responsibility and focused selectors. The
  later diff reports new/updated/removed method counts and preserved existing
  all-scope/late/replay/export controls, with a successful synthetic fallback
  drill and explicitly open human-witnessed acceptance.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: The frozen gate path conflicts with the supplied filesystem restriction

* Related IDs: P02-T02; full17/sealed receipt acceptance.
* Evidence: phase details lines 63-65 require output under
  /tmp/ama-221-rpi-20261020-01. The supplied execution instructions prohibit
  file operations under /tmp and temporary directories. Independently,
  tools/rpi-checks.py:1676-1678 hardcodes its shared lock under /tmp, so merely
  changing --out does not resolve the conflict.
* Concern: The planned gate invocation is not eligible in the stated
  environment. Disabling the shared lock, redirecting prohibited writes or
  claiming a receipt anyway would not be an acceptable workaround.
* Impact: A full17 run and sealed final receipt cannot presently be promised.
  This is a concrete validation blocker, not a source defect in the proposed
  incident control or a reason to fabricate success.
* Smallest useful change: Remove the prohibited path from the executable
  handoff and record the gate prerequisite honestly. Require an eligible
  environment/path policy and a new external evidence location outside the
  candidate before running the unchanged gate. Do not silently broaden this
  issue into runner/lock changes or perform forbidden operations. If the
  current restrictions remain, finish permitted engineering evidence but
  mark the complete gate/receipt and final candidate acceptance Blocked.
* Action owner: Planning parent; execution-environment/gate owner clears the
  prerequisite outside this critique.
* Exact resolving evidence: Corrected P02-T02 names an eligible gate route
  or explicitly records this blocker, retains the commit-before-gate order,
  exact HEAD/current-base binding, fresh receipt and verification requirement,
  and promises no push/PR. A receipt is accepted only after an actually
  permitted full run; no source or historical receipt is a substitute.
* Decision route: Direct planner correction to the honest execution boundary.
  No user response is required to keep the gate blocked.

## Strengths and Residual Risk

* Reusing the existing continuity document, checked SQL writer, audit chain,
  immutable release references and trusted-proxy capability mapping is the
  right architecture. No competing incident or approval system is justified.
* A seeded critical incident satisfies the bounded negative-control branch
  without inventing an approved monitoring threshold.
* Separate current registered staff, engineering restart permission,
  corrective evidence and actual appointment/acceptance are necessary
  distinctions. The plan states them correctly in principle.
* Manual case work, resident challenge and statutory/emergency hazard response
  must remain outside this AI pause; no new home/work-package orchestration
  or generic governance-breach engine is requested.
* Actual OD-35 appointment, competent corrective-test acceptance, approved
  monitoring thresholds, live-provider evidence and a human-witnessed drill
  remain human-blocked. A constructed permission fixture can prove mechanism,
  not discharge those requirements.
* Original issue #219 adverse Review findings remain historical evidence.
  Its later correction Review reports bounded RV-001 through RV-003 resolution,
  not actual authority or whole-issue acceptance.

## Questions or Blocking Evidence Gaps

There is no unresolved user choice needed to correct this candidate. The
caller already forbids actual approval invention and permits only bounded
synthetic engineering. Missing authority remains unavailable, not a default.
PC-007 is a known complete-gate prerequisite blocker. PC-005 requires a concrete
native-test route before that validation can be represented as runnable.

## Limitations

* This is a static independent plan critique, not executed proof of incident
  handling, SQL concurrency, native browser/scanner prerequisites or a receipt.
* Issue acceptance was assessed from the supplied caller boundary and local
  PRD/BRD/source evidence. No live GitHub issue status or remote main was read.
* The current plan candidate and original research/detail records are left
  intact. This artifact does not rewrite an adverse Review or attest a final
  implementation head.
* No regulatory currentness or company authority appointment was inferred
  from the case context.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Freeze the constructed/actual restart decision table
  and persistent actual-provider denial; then directly resolve PC-002 through
  PC-007 in the canonical plan/details and record each disposition.
* User response required: No.
* Preserve this one complete critique. Do not request a second critique or
  nested sub-planner for these direct corrections. Proceed to Implement only
  after the parent finalizes a safe, executable plan, with unavailable final
  validation explicitly blocked rather than presumed passed.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-20/operator-suspension-221-research.md](.copilot-tracking/research/2026-10-20/operator-suspension-221-research.md) | Canonical research and C1-C8 evidence. |
| [.copilot-tracking/plans/2026-10-20/operator-suspension-221-plan.md](.copilot-tracking/plans/2026-10-20/operator-suspension-221-plan.md) | Exact candidate assessed; unchanged. |
| [.copilot-tracking/details/2026-10-20/operator-suspension-221-phase-details.md](.copilot-tracking/details/2026-10-20/operator-suspension-221-phase-details.md) | Exact task details assessed; unchanged. |
| [.copilot-tracking/reviews/2026-10-20/operator-suspension-221-plan-critique.md](.copilot-tracking/reviews/2026-10-20/operator-suspension-221-plan-critique.md) | Original independent critique and complete finding set. |
| [.copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md](.copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md) | Preserved original adverse dependency Review. |
| [.copilot-tracking/reviews/logs/2026-10-15/rai-reliance-review-fixes-219-review.md](.copilot-tracking/reviews/logs/2026-10-15/rai-reliance-review-fixes-219-review.md) | Later bounded dependency correction evidence. |

## Next Steps

The active planning parent directly disposes PC-001 through PC-007, finalizes
the canonical plan/details without another critique and retains all original
adverse evidence. No user action is required. Actual authority/live acceptance
and any ineligible full-gate execution remain blocked; neither synthetic
results nor caller-provided approval strings may clear them.
