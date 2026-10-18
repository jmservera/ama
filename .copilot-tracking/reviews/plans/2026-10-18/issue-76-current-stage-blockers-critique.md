---
title: Issue 76 current-stage blockers final-candidate critique
description: One independent bounded plan assessment at the supplied production base
ms.date: 2026-10-18
---

## Metadata

* Task ID: 76.
* Critique date: 2026-10-18.
* Critique execution status: Complete.
* Verdict: Revise.
* Severity summary: 0 Critical, 0 High, 3 Medium, 0 Low.
* Workspace: /home/azureuser/source/ama-wt/issue-76-blockers.
* Confirmed branch: fix/current-stage-queue-blockers-76.
* Confirmed production HEAD: 6c1e376ff1241316272df22a5a3a6853aae9f87b.
* Plan: .copilot-tracking/plans/2026-10-18/issue-76-current-stage-blockers-plan.md.
* Phase details: .copilot-tracking/details/2026-10-18/issue-76-current-stage-blockers-phase-details.md.
* Execution count: exactly one independent final-candidate critique; no implementation, independent implementation Review, nested agent or second critique.

## Inputs and Criterion Boundary

The assessed candidate consists of the supplied plan and phase details, the
current user acceptance conditions, and these preserved research inputs:

* .copilot-tracking/research/2026-10-18/issue-76-current-stage-blockers-research.md.
* .copilot-tracking/research/2026-10-18/issue-76-current-stage-blockers-before.txt.
* .copilot-tracking/research/2026-10-18/issue-76-current-stage-blockers-probe.py.

Relevant source inspection covered the canonical queue evaluator, JSON and SQL
membership paths, final-stage transition and technical helpers, existing queue
tests, the real loopback HTTP suite and the existing MSSQL inheritance/factory
boundary. Project specification, index and memory supplied contextual constraints,
not operational approval.

The assessment checks stage-aware final prerequisites, selection/membership
agreement, durable upgrade compatibility, independent positive and negative test
oracles, current safety/stock/building controls, role projection, unchanged gates,
test ownership, red-first sequencing and bounded publication. It does not assess
an implemented diff or independently establish runtime results. The research's
eight failures are preserved observations, not executions performed by this
critique.

The supplied issue-state evidence is accepted within this boundary: #76 is open,
#290 is closed, and #73 is hierarchy. No Backlog Manager readiness verdict,
live Entra verification or human role-policy acceptance is inferred. No new
external research or GitHub mutation was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C3; P01-T02; acceptance 1-2 | Covered | taskqueues.py:225-255 makes final requirements inactive; :299-337 selects active requirements but classifies blocked from all records. Stage activation and one active list directly address both defects. |
| Public version/default/reset; C4; P02-T01 | Covered | sqlstore.py:310-320 already compares a private fingerprint; internal MEMBERSHIP_REVISION can invalidate indexes without changing work-queues-1 or reset metadata. |
| P01-T01; positive/current-stage controls | Covered | DATA cases[2] is explicitly funded, signed and supplied with resident scope/decision evidence; phase details require isolated deficiencies and early/final/post-final cases through real stores and HTTP. |
| Acceptance 2; pending handoff | Covered | taskqueues.py:307-328 permits pending handoff to suppress the existing final-check fallback. Activating final requirements before selection and testing the pending combination addresses this. |
| Acceptance 3; safety/stock/building precedence | Covered | taskqueues.py:167-224 appends these current stops before final requirements; phase details preserve precedence, hazard owner and clocks, including mixed future requirements. |
| Acceptance 4; C4-C5; P02-T01/T02 | Partial | Certified old-format flags, independent expected IDs, immutable body/audit state and generation checks are specified; inherited MSSQL no-seed reopening needs the concrete safe recipe in PC-002. |
| Acceptance 5; C6; P01-T01; P03-T01 | Covered | Real loopback list/detail/CSV/filter and role/query-spoofing checks are required; test_task_queue_api.py already has the HTTP and denial harness. |
| No gate or authority bypass; P01-T02/P03-T01 | Covered | store.py:504-521 retains final-stage, gate, building, safety, resident and capacity checks. Gate helpers and projection stay out of scope; coupled regression execution is required. |
| Three existing suites; at most 10 methods; inherited MSSQL | Covered | Plan locks ownership, forbids removals/generated targets and prefers inherited SQL cases; no new harness file or resident test edits are required to resolve these findings. |
| Red tests before production fix; P01-T01/P02-T01 | Partial | P02 introduces the upgrade regression after P01 production edits; PC-001. |
| Sanitized offline execution; P03-T01; immutable probe | Partial | env -i does not preserve a workspace-local tempfile override by itself; PC-003. |
| P03-T02/T03/T04; bounded authority and lifecycle | Covered | Candidate hashing, preserved adverse originals, one implementation Review, at most two source corrections, normal topic push and coordinator stop are explicit. |
| Live identity/policy acceptance | Explicitly unmet | Correctly retained as owner/coordinator work, not converted into readiness or permission to implement authority changes. |

## Verdict

* Verdict: Revise.
* Rationale: The functional approach is credible and the public/private version
  decision is appropriate. Three bounded execution-plan corrections are needed
  to honor red-first evidence, make real MSSQL restart evidence trustworthy and
  keep future test/probe file operations inside the authorized workspace.
* No architectural reversal, expanded research phase or user decision is needed.
  These findings do not authorize source implementation by this critique worker.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Upgrade regression is scheduled after the first production fix

* Related IDs: red-first user requirement; plan Test Ownership and Locked
  Boundary; P01-T01, P01-T02 and P02-T01.
* Evidence: The plan places P01-T02 production edits before P02-T01, which
  introduces the internal revision and upgrade regression together. Phase details
  P01-T01 requires red core/store/HTTP regressions, but P02-T01 does not require
  its migration regression to have failed on the untouched production base.
* Concern: The migration regression could first be authored against an already
  corrected evaluator or even the completed revision. The preserved semantic
  probe does not exercise old certified indexes and cannot substitute for this
  red migration evidence.
* Impact: The task could satisfy its semantic red run while missing the explicit
  red-before-production condition for the durable-index correction.
* Smallest useful change: Move authorship and the expected-failure run of the
  certified-old-flags upgrade regression into the pre-production test gate.
  Keep implementation of the private revision in P02. Identify the migration
  selector and expected stale-membership failure separately from semantic failures;
  unchanged controls may pass.
* Action owner: Planning parent for the plan correction; primary implementer for
  the red run.
* Exact resolving evidence: Revised ordering explicitly requires all new defect
  regressions before P01-T02. The later changes artifact records the upgrade
  test selector, expected failure and unchanged production-source hashes at
  6c1e376ff1241316272df22a5a3a6853aae9f87b, followed by its green result after
  the revision. Test changes remain within the three suites and ten-method cap.
* Decision route: Direct planner correction. No user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Inherited MSSQL no-seed restart needs a stable seed-path recipe

* Related IDs: C4; acceptance 4; P02-T01 and P02-T02; inherited MSSQL requirement.
* Evidence: src/api/tests/test_mssqlstore.py:294-307 inherits only
  SqlQueueMembership and wipes its database whenever make_store receives a
  different seed-path string. The existing no-seed migration case in
  src/core/tests/test_sqlqueues.py:203-237 belongs instead to SqlQueueMigration
  and directly constructs SqlStore. Phase details P02-T02 requires the same new
  inherited SQL tests and reopening without a seed but does not identify how to
  preserve the owned database across that reopen.
* Concern: Reusing the existing migration class would not run the new upgrade
  scenario on actual MSSQL. Conversely, using a new nonexistent seed path with
  the inherited make_store factory would wipe the database rather than reopen
  its old populated index. This is an existing harness constraint, not a defect
  alleged in the production stores.
* Impact: A nominal restart/upgrade test can fail for a fixture-lifecycle reason
  or omit real-engine upgrade coverage, instead of proving repair of the
  already-populated MSSQL database.
* Smallest useful change: Explicitly assign the portable certified-old-flags
  regression to SqlQueueMembership. Reopen through self.make_store using the
  identical seed-path string after removing that seed file; do not change the
  path or reset the harness. Keep the existing SQLite schema-migration test
  unchanged.
* Action owner: Planning parent for the test recipe; primary implementer for
  its inherited test.
* Exact resolving evidence: One shared new method is selected in SQLite and
  MssqlQueueMembership on the disposable local engine. It preserves the populated
  database across reopen with the seed absent, seeds the literal original
  fingerprint shape with matching snapshot/day/policy and wrong certified flags,
  and leaves schema columns and other invalidators intact. It checks independent
  repaired IDs/physical flags, generation advancement, and unchanged case bodies,
  rowversions, sequence and ledger state. The run proves repair is attributable
  to the membership revision, not an empty context, schema backfill, changed day
  or reseed.
* Decision route: Direct planner correction. No new harness edits, authority
  change or user response required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Sanitized commands must explicitly retain workspace-local scratch

* Related IDs: caller prohibition on temporary-directory file operations;
  P01-T01, P02-T02 and P03-T01; immutable original probe.
* Evidence: The supplied issue-76-current-stage-blockers-probe.py uses
  tempfile.TemporaryDirectory without a directory argument. The three existing
  test suites also use default tempfile directories. Phase details P03-T01
  requires env -i for every application/test probe but names no TMPDIR override.
* Concern: env -i removes an inherited TMPDIR, so default tempfile allocation
  can target /tmp despite synthetic fixture content. Leaving the original probe
  unchanged does not by itself make its scratch-file destination compliant.
* Impact: Future required red/green and original-probe execution can violate the
  explicit file-operation boundary before collecting valid acceptance evidence.
* Smallest useful change: Require an owned scratch directory beneath this
  workspace and explicitly set TMPDIR to its absolute workspace path inside
  every sanitized Python test/probe command, including MSSQL suite execution.
  Keep the original probe and existing resident tests untouched; clean owned
  scratch files afterward without deleting unrelated content.
* Action owner: Planning parent for the environment contract; primary implementer
  for safe directory lifecycle and command receipts.
* Exact resolving evidence: Revised phase details give a sanitized command
  environment including workspace-local TMPDIR. Later execution receipts show
  tempfile.gettempdir() resolves beneath the workspace under that same
  environment, record actual test/probe commands and confirm owned scratch
  cleanup. No private dataset, secret environment file or existing service is
  used.
* Decision route: Direct planner correction implementing an already explicit
  boundary; no user response required.

## Strengths and Residual Risk

* Preserve future requirement records with current_stop false outside the actual
  final-check stage; do not remove the requirements or substitute a relaxed gate.
* The fully supplied DATA positive control and isolated deficiencies avoid the
  original probe's narrower funding/technical-only coverage becoming the entire
  acceptance oracle. Resident activation belongs in queue tests, not edits to
  the active #86 resident paths.
* Keep the public version, default and reset contract unchanged. Internal index
  invalidation is a compatibility repair; bumping public VERSION would conceal
  whether the private revision independently handles stale flags.
* Existing active safety, stock and building records must remain selected ahead
  of newly active final requirements. Hazard clocks retain their existing
  snapshot basis and named owner; no new clock or human approval is invented.
* Canonical membership is computed before per-user reason projection. HTTP
  parity must therefore include explicit expected membership as well as masked
  reason/action content and unchanged denied actions, not just equal outputs.
* JSON has in-memory cache invalidation and save/reopen behavior; independent
  warm-connection generation behavior is SQL-specific in the existing design.
  The candidate's P02-T02 appropriately distinguishes JSON save/reopen from SQL
  other-process checks and does not authorize adding JSON live synchronization.
* Actual disposable MSSQL execution remains required future evidence, not an
  optional dialect mock or a skipped test counted as a pass.
* No queue change establishes ability to advance, competent-role sign-off,
  resident consent, live identity integration, human definition ratification or
  full issue acceptance. Existing operational boundaries remain unmet where
  identified by the caller.

## Questions or Blocking Evidence Gaps

No decision-critical user question is needed. The supplied evidence supports this
bounded assessment. Implementation results, actual-engine availability at
execution time and later exact-head coordinator acceptance remain future gates,
not missing evidence that blocks the present plan critique.

## Limitations

* No application, test, container or original probe was executed by this worker;
  doing so was unnecessary for this plan-only assessment.
* No private data, .env files, support content or protected resident implementation
  or test paths were read or modified. No cloud writes, spending or model
  inference was performed.
* The mandatory project-context aggregate read exceeded tool output limits;
  bounded relevant sections were read separately. No claim depends on unseen
  portions of that aggregate.
* Shell ripgrep was unavailable; bounded standard source reads and filename
  discovery supplied the needed evidence instead.
* Only this new critique artifact is authorized for persistence. Plan, details,
  research, preserved probe and before output, state and production/test sources
  remain unchanged by this critique.

## Recommended Next Action

* Highest-impact finding: PC-001, because the ordered candidate otherwise permits
  production edits before collecting the upgrade regression's red evidence.
* Action owner: Planning parent.
* Smallest next action: Revise test ordering and add the stable-path MSSQL
  reopening and workspace-local scratch recipes, preserving this original
  three-finding set.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-18/issue-76-current-stage-blockers-plan.md | Assessed final-candidate plan; unchanged. |
| .copilot-tracking/details/2026-10-18/issue-76-current-stage-blockers-phase-details.md | Assessed phase details; unchanged. |
| .copilot-tracking/research/2026-10-18/issue-76-current-stage-blockers-research.md | Supplied bounded research and issue-state evidence. |
| .copilot-tracking/research/2026-10-18/issue-76-current-stage-blockers-before.txt | Preserved original eight-failure baseline; not rerun here. |
| .copilot-tracking/research/2026-10-18/issue-76-current-stage-blockers-probe.py | Preserved original real-store semantic probe. |
| .copilot-tracking/reviews/plans/2026-10-18/issue-76-current-stage-blockers-critique.md | This single complete independent critique. |

## Next Steps

The active planning parent should resolve PC-001 through PC-003 directly in its
owned plan/details and record disposition without another critique. No user
action is required. This worker stops after this one plan assessment and does not
implement, launch Review, publish or claim issue readiness.
