---
title: Resident completed author refinement independent plan critique
description: Final-candidate implementation readiness for bounded unsigned integration
ms.date: 2026-10-23
---

## Metadata

* Task ID: jmservera/ama#441, resident-portal-requirements-441.
* Critique date: 2026-10-23.
* Plan: .copilot-tracking/plans/2026-10-23/resident-portal-requirements-441-refinement-plan.md.
* Phase details: .copilot-tracking/details/2026-10-23/resident-portal-requirements-441-refinement-phase-details.md.
* Critique execution status: Complete.
* Verdict: Pass for the planned unsigned documentary integration only.
* Findings: 0 Critical, 0 High, 0 Medium, 1 Low execution prerequisite.
* No mandatory plan correction or new owner decision is required.

## Inputs and Criterion Boundary

The assessment covers the complete supplied plan, phase details and current
refinement research, including AC1-AC7, P01-T01 through P02-T03, scope/test
ownership, selected evidence, historical continuity and stop conditions.
The current owner direction expressly permits author-complete UNSIGNED
REVIEW-PROPOSAL integration despite the fresh adverse requirements review.
That direction resolves whether unsigned integration may proceed; it does not
waive any finding or authorize a lifecycle exit.

Inputs read:

* .copilot-tracking/plans/2026-10-23/resident-portal-requirements-441-refinement-plan.md.
* .copilot-tracking/details/2026-10-23/resident-portal-requirements-441-refinement-phase-details.md.
* .copilot-tracking/research/2026-10-23/resident-portal-requirements-441-refinement-research.md.
* .copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/validate-integration.py.
* .copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/test_validate_integration.py.
* .copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/markdownlint.json.
* src/README.md, local RPI gate contract; relevant clean-input and receipt
  implementation in tools/rpi-checks.py.
* Supplied project context and the owner-approved refinement package at
  ../../../.copilot/session-state/b9cc4727-b806-4e0f-a2cf-c5010d92428c/files/resident-442-refinement-20261023/.
  Relevant actual inputs inspected include the reviewer summary, PRD output
  manifest and validation, reconciled proposal, reconciliation input/output
  manifests, reconciled requirement-map structure, reconciliation report,
  reconciliation validation and integration handoff.

Read-only inspection confirmed local HEAD 8ada8109 on
docs/resident-portal-requirements-441 and PR442 OPEN/non-draft, targeting main.
The initial untracked files were the supplied refinement Research, Plan and
details, not product edits. All four supplied pins were independently
recomputed by this critic:

| Input in approved package | SHA-256 |
| --- | --- |
| prd/zava-forward-retrofit-programme-demonstrator.md | 7fb40549ba4975c2feb8d8a2a3de882e06677875c02e4a43c4b3a94ddf218343 |
| prd/output-manifest.json | cbbcc45fde3653343115a2071793cb21dcede1c335cbf1e3800e7e41a59c46b1 |
| adr/resident-service-unregistered-proposal-reconciled.md | 8e44d6ffbfe907a5e7e8cd057d0a29e0e977e916456ed0f0d9799efe8e1a4d77 |
| adr/reconciliation-output-manifest.json | c0b97777d015926573a320d004e38f11c45e965f0540e2e64d8e241bde4f57ce |

The parent's supplied 18+3+10 closure checks, definition comparisons and exact
patch reconstruction are credited as Research evidence, not represented as
independently rerun here. This is a plan credibility assessment, not an
integrated-byte Review, formal requirements assessment or gate receipt.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1; Research readiness; P01 entry | Covered | Independent critique precedes product edits; prior phases and outcomes are not fabricated. |
| AC2; P01-T01 | Covered | Four pins match; raw candidates/manifests remain immutable, derivative substitutions and hashes are mapped. Selection is deliberate, not a claim to archive the entire author workspace. |
| AC3; P01-T02 | Covered | One existing canonical PRD and one evolving existing proposal; id:null/proposed/unregistered, unchanged assets and definitions, bounded coupled notices. |
| AC4; P01-T03; locked ownership | Covered | Eight existing regression methods retained; existing validator plus task-local refinement checks; at most three added regression methods only for actual coupled helper changes. |
| Current seven findings; P01-T02/P02-T01 | Covered | Current summary and proposal retain all seven findings; author-source quality is not an attestation of editorially changed integrated bytes. |
| AC5; P02-T01 | Covered | One actual-byte independent Review, explicit execution/outcome distinction and stop on material integration defects; no historical Review replacement. |
| AC6; P02-T02 | Covered, execution pending | Stable clean committed candidate, fresh refs, nonblocking protected gate, external receipt and official verification; PC-001 is a current eligibility prerequisite. |
| AC7; P02-T03 | Covered | Exact head/tree/base/lease handoff; this session stops before push, PR edits, merge or closure. |
| Correction1 and historical evidence | Covered | Existing scripts/tests/bot/history, original source evidence, reports and gate environments remain protected; new dated notices do not rewrite author-era observations. |
| Sibling overlap and later publication | Covered | Refresh and stop on movement; no sibling import or worktree write. PR439 shared-document reconciliation remains later work, not an invented dependency. |

## Verdict

* Verdict: Pass.
* The plan is credible for the owner-authorized unsigned refinement integration.
  It specifies enough custody, relocation, preservation and test ownership to
  proceed without redesigning requirements or architecture.
* PC-001 implements the existing AC6 clean-input condition. It does not require
  a substantive plan revision and does not block P01 documentary integration.
  A technical gate is not eligible on the currently observed checkout.
* This verdict is not a PRD quality PASS, Validate/Finalize exit, ADR
  registration, architecture acceptance, acceptance-test result, publication
  permission or live-service approval.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Low]: Resolve observed ignored input before the single technical gate

* Related IDs: AC4, AC6, P01-T03, P02-T02, P02-T03.
* Evidence: Read-only git ls-files --others --ignored --exclude-standard
  returned .copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/__pycache__/validate-integration.cpython-312.pyc.
  tools/rpi-checks.py:153-155 rejects ignored inputs independently of ordinary
  Git status. The adjacent regression module imports the validator, which can
  recreate bytecode unless the focused-check environment prevents it.
* Concern: A tracked-clean commit alone cannot establish eligibility. Leaving
  this cache in place would make the one allowed gate attempt fail at
  preflight, before technical validation. This is an observed execution
  prerequisite, not evidence that the plan authorizes dirty-input validation.
* Impact: Avoidable consumption of the single protected run or an inaccurate
  clean-candidate handoff.
* Smallest useful change: Execute the plan's existing eligibility condition
  explicitly: identify the cache's ownership, resolve only owned disposable
  generated input through the permitted cleanup process, and prevent focused
  checks from recreating in-tree bytecode. Keep test scratch in an authorized
  location. Do not delete unknown inputs or historical gate environments.
  Check ordinary, untracked and ignored status before attempting the gate.
  If cleanup is not authorized or another input remains, report the precise
  not-run blocker rather than spending or retrying the gate.
* Action owner: Planning parent/integration executor.
* Exact resolving evidence: A pre-gate record of the exact committed
  HEAD/tree/base and empty git status --porcelain --untracked-files=all plus
  empty git ls-files --others --ignored --exclude-standard after focused
  checks, with ownership-safe cache disposition. Alternatively, an explicit
  gate-not-run handoff naming the remaining input.
* Decision route: Direct execution of an already approved planner condition;
  no significant or divergent user decision and no plan change required.

## Strengths and Residual Risk

### Portable evidence and canonical identity

The selected raw archive versus navigable derivative strategy is appropriate.
Blindly copying the package would bring scripts, snapshot context and a
subsidiary ADR into scope. The plan instead preserves exact author candidates
and manifests, maps deliberate link transformations, and retains one evolving
proposal at its existing canonical path. Historical proposal bytes are inert
evidence, not a second current decision.

Implementation must maintain the stated distinction: raw manifest inventories
describe original author outputs, including intentionally unselected files;
they are not a promise that every inventoried output is copied. Source hashes
and source line references remain source identities. Actual integrated hashes,
portable paths and editorial changes belong in the integration mapping.
The planned task-local checker and actual-byte Review own verification of
that distinction. Selected raw-source link failures must not be advertised as
navigable derivative passes.

### Preserved current adverse quality

The reviewer summary identifies current FAIL / Validate BLOCKED / Finalize
NOT_EVALUATED, singular 1 below minimum 2, and 7 CAUTION / 34 COVERED / 0 RISK.
All seven remain in scope for faithful preservation, not repair:

| Finding | Severity | Required continuing visibility |
| --- | --- | --- |
| pr442-qual-005 | High | Bundled FR-044/FR-060 and AC-104-106; singularity remains blocking. |
| pr442-qual-040 | High | Unsigned BRD and missing governed handoff. |
| pr442-qual-006 | Medium | Unconfirmed provider, staffing, recovery, budget and delivery feasibility. |
| pr442-qual-024 | Medium | GOAL-005 achievability and time-bound evidence missing. |
| pr442-qual-041 | Medium | Generic/resident latency and file-size applicability/precedence OPEN. |
| pr442-qual-009 | Low | Inherited two-cell AC-104-106 rows in a five-column table. |
| pr442-qual-039 | Low | FR-059 goal-definition/matrix mismatch. |

Qualified 71/71 trace is structural author linkage, not quality acceptance.
The summary is not persisted raw reviewer payloads, crypto verification,
application execution or human approval. Technical checks and RPI conformance
must not replace this current requirements outcome.

### Bounded ownership and historical continuity

P01-T03 assigns custody/definition/link checks without demanding application
implementation or new acceptance results. Existing eight regression methods
remain protected. A real coupled helper change requires its bounded regression
coverage and final verification before Review; the task-local checker does
not silently replace the old validator.

The plan correctly preserves Option B and rationale, assisted/manual paths,
explicit current grants, default human review, routine automation OFF, live
and unsigned gates, and all 30 Not-run resident criteria. Registration remains
deferred, with no numbered ADR, configuration, allocator or invented lineage.

Correction1 is later verified native history, while author-era validator/PID
statements remain historical observations. Dated integration notices preserve
both facts without rewriting old reports. Existing scoring residuals stay
OPEN; no scorer JSON edit, paid dispatch or generated-score acceptance is
authorized.

The full gate remains a later conditional technical operation on stable
eligible committed bytes. Lock contention, source/base/remote movement,
missing prerequisites or material Review defects stop execution. No cloud
fallback, waiting queue, retry loop or receipt transplant is justified.

## Questions or Blocking Evidence Gaps

None for the bounded implementation-readiness decision. The owner has already
resolved unsigned integration versus formal lifecycle acceptance. No further
answer is needed to proceed with P01.

## Limitations

* The approved external package was readable. No access restriction prevented
  this assessment; no parent inability to read it is inferred.
* Actual integrated bytes do not yet exist. Derivative links/anchors, complete
  mapping, focused results and final clean-candidate eligibility are future
  acceptance evidence, not findings claimed complete by this critic.
* No heavy gate, scorer, application test, hash-manifest closure rerun or
  independent exact-head publication assessment was performed. No remote
  mutation or delegation occurred.
* Source review of selected relevant material and the four recomputed pins
  does not establish independent requirements, legal, privacy, accessibility,
  feasibility, registration or operational acceptance.
* The initial untracked Research/Plan/details were preserved. Only this
  caller-specified critique artifact was written.

## Recommended Next Action

* Highest-impact actionable finding: PC-001, Low, future gate eligibility.
* Action owner: Planning parent/integration executor.
* Smallest next action: Record this Pass and PC-001 execution disposition,
  then perform P01-T01. Before the single gate, prove ignored-input cleanliness
  or report a precise not-run blocker.
* User response required: No.
* Stop boundary: This critic stops here. The parent retains the ordered
  integration/Review process and must not push or edit PR442 under this task.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-23/resident-portal-requirements-441-refinement-plan.md](../../../plans/2026-10-23/resident-portal-requirements-441-refinement-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-23/resident-portal-requirements-441-refinement-phase-details.md](../../../details/2026-10-23/resident-portal-requirements-441-refinement-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-23/resident-portal-requirements-441-refinement-research.md](../../../research/2026-10-23/resident-portal-requirements-441-refinement-research.md) | Current custody and scope research |
| [.copilot-tracking/reviews/plans/2026-10-23/resident-portal-requirements-441-refinement-plan-critique.md](resident-portal-requirements-441-refinement-plan-critique.md) | This independent critique |

## Next Steps

The active planning parent records the Pass and carries PC-001 into execution,
then proceeds with the authorized P01 integration and later independent
integrated-byte Review. No user action or second critique is required.
STOP BEFORE PUSH, PR updates or merge.
