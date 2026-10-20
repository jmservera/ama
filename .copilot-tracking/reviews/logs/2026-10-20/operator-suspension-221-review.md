---
title: Original independent operator suspension 221 RPI Review
description: Single post-implementation assessment of the supplied engineering boundary
ms.date: 2026-10-20
---

## Scope and Evidence

* Task: #221, branch feat/operator-suspension-221.
* Base: 7e95f0224bfb7a8a62990a1de162fbcfa68db539.
* Boundary: complete tracked diff against base, untracked src/api/tests/test_operator_suspension.py, and supplied canonical research, plan, details, critique and changes.
* This is the one original Review. No correction or replacement Review is authorized.

## Opening Review State

* Goal: independently assess engineering behavior, semantic tests, critique dispositions and evidence without inferring actual restart authority.
* Scope: P01-T01, P01-T02, P02-T01 implementation plus reconciliation of pending P02-T02 and human follow-ups.
* Evidence readiness: canonical artifacts identified; plan and details read; code, research, critique, changes and validation comparison pending.
* Acceptance basis: FR-053/AC-072/NFR-014, RULE-024/AC-078/RULE-020, open OD-35, canonical AC1-AC6 and PC-001-PC-007 dispositions.
* First comparison: canonical requirements and critique versus complete source diff and issue-specific tests.
* Read-only boundary: only this review record may be written. No source edits, git mutation, remote action, nested agents, cloud/live activation or cohort evaluation.
* Initial limitations: native SQL/full17 and committed candidate are parent-owned subsequent work, not passed evidence; reported focused checks require assessment. Reviewer may not use forbidden temporary paths.

## Execution Status

* Review execution: Complete.
* Review evidence: entire supplied tracked diff and untracked issue test module assessed once, canonical task set reconciled, actual source-function probes executed without disk fixtures, and findings routed below.
* Implementation execution: Partial; P02-T02 and human acceptance remain pending.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 | Incident capture, restart permission/evidence, actual_hold and epoch consumers | Delivered source exists, but not wholly conformant | RV-001 through RV-004 qualify the completion tick; no retrospective plan edits performed |
| P01-T02 | Owning regression updates, 10 issue tests and one native bridge | Method allocation and bounded fixture intent reconciled | Semantic coverage is substantial; four uncovered edge/lifecycle gaps remain |
| P02-T01 | Focused/static checks, component contracts, knowledge index/log | Reconciled as reported implementation work | Documentation correctly preserves actual-authority limits, but broad completeness/audit/history/export claims require the RV qualifications |
| P02-T02 | Original Review, commit, native/full17, sealed handoff | Intentionally pending parent work | This record supplies only its original Review component; it does not satisfy commit, SQL, full gate or acceptance |
| Follow-Up Items | Actual appointment, thresholds, competent evidence, human drill and #222 | Explicitly outside bounded engineering | Retained separately under RV-006; no new active implementation scope |

Plan AC1-AC6 checkmarks describe bounded engineering intent, not full issue or
human acceptance. AC2 and AC4 cannot be treated as unqualifiedly established
because of RV-001/RV-003 and the historical-contract gap. The unchecked
SQL/JSON/native aggregate is conservative: JSON containment and SQLite
engineering are reported, while native SQL is not yet run. Full17/receipt/
commit and actual acceptance remain unchecked. Research's early Q1-Q4 rows
still say Open, but its later findings explicitly answer every question and
its readiness conclusion is clear; this editorial residue does not prevent
a credible review boundary.

## Completed Work Assessment

| Marker / criterion | Actual files and semantic evidence | Assessment |
| --- | --- | --- |
| P01-T01 / AC1 | src/core/src/zava_forward/core/continuity.py, assistants.py and ai_tasks.py; shared drill checks affected ready verification denial, pending/new execution denial and unchanged provider-call count | Correct core containment direction; no inferred live activation |
| P01-T01 / AC2 | Transactional incident_versions and affected_assistant_tasks under SqlStore.save; boundary-enqueue test and reference/binding assertions | Assistant snapshot seam improved and no preview truncation; legacy completeness defect RV-001 |
| P01-T01 / AC3 | log_call and raise_hazard actually execute and reopen retained state in drill/manual_hazard_drill | Semantic mutation evidence, not merely MANUAL_NOTE or constants |
| P01-T01 / AC4-AC5 | Dedicated trusted OID-bound capability, current staff revalidation, manager/distinct email-code-OID checks, structured constructed claims and exact candidate/proposal digests | Missing/self/untrusted/stale/altered/drift/replay requests tested; early denial audit incomplete, RV-003 |
| P01-T01 / AC6 | Actual Ai provider test installs an actual-class release after constructed restart, asserts disabled task, no dispatch/calls and retained authority gap; shared drill reopens and switches provider | Persistent actual_hold is real engineering enforcement, not just fixture labelling; no actual authority acceptance |
| P01-T01 / task isolation | Both proposal and claim epochs use task-aware history; shared drill preserves unrelated accepted and in-flight work | Raw global comparisons migrated across identified assistant and legacy consumers; malformed/history/export exceptions remain RV-002/RV-004 |
| P01-T02 / persistence | _proc_write failure and independent-document conflict preserve Suspended state; reopen and denied audit exercised | No partial restart found in the ordinary covered SQL writer rollback/conflict paths; native execution still pending |
| P01-T02 / auth HTTP | test_trusted_capability exercises real principal mapping, email fallback, password stripping and loopback trusted decision | Meaningful source/auth semantic coverage; password HTTP denial audit and pre-try identity denial not checked |
| P02-T01 / documentation | src/core/README.md, src/api/README.md, docs/reference/README.md and append-only log | Consistent about constructed claims, unavailable actual authority and human gates; overbroad complete-snapshot/denial/history claims need later correction with source |

No existing test method was deleted. The legacy accepted-priority assertion
was moved into the current cache/incident sequence, so the later latest-record
status is now Proposed rather than Accepted; assistant accepted-history
non-revival tests remain. Existing helpers now construct explicit permission
and evidence instead of using an arbitrary authority string. Those changes
do not introduce a production bypass. The new mypy override follows the
existing untyped shared-fixture convention, rather than excluding production
code from checking.

## Implementation-Time Plan and Detail Update Assessment

| Area | Change and rationale | Trigger and decision | Reconciliation / assessment |
| --- | --- | --- | --- |
| PC-001 / P01-T01 | Persistent actual_hold plus separate trusted AIRestart capability; no seed grant | Actual authority must remain unavailable under confirmed bounded caller direction | Reflected in plan, details, code, tests and guides; correct direction, no new authority decision inferred |
| PC-002/PC-003 / P01-T01 | Current corrective candidate is separate from immutable incident versions; SQL captures impacted rows inside writer | Stale evidence and pre-write/truncated preview defects | Reconciled; RV-001 is an implementation shortfall, not a reason to invent a new incident system |
| PC-004 / P01-T01 | Shared relevant-task history replaces raw equality including claim_epoch | Unrelated-task preservation versus relevant historical non-revival | Reconciled consumer migration; RV-002/RV-004 expose incomplete implementation of the frozen contract |
| PC-005/PC-006 / P01-T02 | Ten issue methods plus native shared-drill bridge, 11 total | Locked method ceiling and existing SQL selector lifecycle | Below plan maximum 18 and details maximum 12; exact actual names present; no runner/receipt extension or extra-test bypass |
| P01-T01 / P02-T01 | Password authentication strips seeded capability/provider claims; HTTP distinguishes committed acknowledgement failure | Tightly coupled trusted-sign-in and atomic-outcome boundary | Within confirmed scope and documented; no material divergent product/authority decision |
| P02-T02 | Review before committed full17 and external handoff; no post-Review production correction here | Explicit caller sequencing and preservation of negative evidence | Honoured; source defects route to later work, not a second Review |

## Critique and Material Revision Assessment

The original critique remains Complete / Revise, 4 High and 3 Medium. It was
not rewritten into a pass and this record does not create a second critique.

| Critique | Recorded disposition | Assessment against implementation |
| --- | --- | --- |
| PC-001 High | Accepted; details decision matrix and actual_hold | Substantially implemented: no actual restart approval API, distinct trusted capability, current local staff check and actual-provider hold across reopen/release change. Constructed export consistency gap is RV-004 |
| PC-002 High | Accepted; structured claim and incident/candidate separation | Implemented explicit test ID/reference/class/result, actor/time, full binding, candidate, digest, reproposal history and transactional recheck. Legacy incident completeness remains RV-001 |
| PC-003 High | Accepted; transaction-owned complete incident snapshot | Pre-write HTTP preview removed; unbounded assistant snapshot under writer is implemented. Legacy unknown impacted versions do not affect completeness, RV-001. No native pass inferred |
| PC-004 Medium | Accepted; all identified consumers migrated | Relevant/unrelated semantic drill and old all-scope controls exist. Unknown/malformed/generic history is not fully fail-closed, RV-002; export context differs, RV-004 |
| PC-005 High | Accepted; bridge in already selected class | test_assistants.MssqlDurabilityTests.test_operator_incident_drill calls shared drill using MssqlFixture. tools/rpi-checks.py SQL_SELECTORS selects the class while owned SQL is alive. Route is executable in principle; required non-skipped native result is still pending, RV-005 |
| PC-006 Medium | Accepted; bounded semantic allocation | 10 issue methods plus one bridge, no method removals; real manual/hazard writes, provider counts, current binding drift, identity and rollback tested. Missing cases are routed as implementation defects, not satisfied by fixture constants |
| PC-007 Medium | Rejected by parent as inapplicable under its explicit caller-authorized gate path/lock | Exact rejection and original contrary critique preserved. This review has a separate filesystem restriction and does not access the offered temporary interpreter/logs or run that gate. No parent-policy permission is inferred by this reviewer; parent/platform must ensure an eligible environment before gate execution |

The available artifacts describe critique incorporation before affected
implementation and contain no contradictory execution evidence. Review does
not independently reconstruct undocumented chronology. The changes are
within the existing confirmed synthetic direction; no significant divergent
decision needs rpi-plan, and no new material research question needs
rpi-research. The acceptance gaps are defects or already distinct follow-ups.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Route |
| --- | --- | --- | --- |
| Actual OD-35 appointment and RULE-020 evidence protocol | Engineering cannot appoint authority or infer actual approval | Building Safety and Sponsor with Digital/task/control owners record named authority and accepted protocol before actual restart | RV-006 distinct governance follow-up |
| Approved monitoring thresholds and competent corrective-test evidence | Constructed Pass is a human-recorded claim, not live evaluation or competent acceptance | Data and Performance, Safety, DPO/Legal and competent task owners obtain approvals/evidence | RV-006 distinct evaluation follow-up |
| Human-witnessed fallback/restart drill and actual acceptance | Unit/HTTP/SQLite checks cannot establish operational oversight | Programme and relevant control owners arrange an explicitly authorized, human-approved exercise | RV-006 distinct human acceptance follow-up |
| #222 cohort evaluation | Separately owned and expressly not authorized in this task | #222 owner obtains its own approved evaluation scope and lawful evidence | RV-006 distinct later issue; not added to P01/P02 |

These follow-ups remain open without becoming active implementation tasks or
being reclassified as code defects.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Legacy impacted versions do not participate in snapshot completeness

* Related scope: AC2/AC4, P01-T01/P01-T02, PC-002/PC-003.
* Evidence: src/core/src/zava_forward/core/continuity.py:177-187 computes snapshot_complete from current candidate and assistant-task bindings before collecting legacy recommendations. Legacy affected entries can contain no release, envelope, prompt_version or task version without changing that flag. restart_propose at lines 368-372 subsequently trusts snapshot_complete as its incident-version prerequisite.
* Independent reproduction: executed the actual validate_sql function extracted from the source AST against an in-memory SQLite database. With an explicitly supplied complete current candidate, no assistant tasks and one historical source=ai/status=Proposed priority recommendation lacking release/version fields, the retained impacted entry had release=None, version=None, envelope=None, prompt_version=None, but snapshot_complete=True. The selected-current-candidate dependency was stubbed to isolate completeness, not claimed as a full integration run.
* Impact: approving a current release can make an incident appear reconstructibly complete despite unknown versions of its impacted historical output. This defeats the frozen incomplete-evidence restart prerequisite. Actual use still remains held; this is not evidence of an actual-authority bypass.
* Destination: later rpi-implement.
* Smallest useful next action: include the entire legacy impacted set and its exact retained release/version evidence in completeness calculation; preserve explicit unknowns and immediate containment, but refuse constructed restart when impacted evidence is insufficient. Add missing-reference and prior-release legacy snapshot/reopen tests.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Historical task and epoch validation is permissive or raises instead of failing closed

* Related scope: P01-T01/P01-T02, PC-004; generic historical/export compatibility.
* Evidence: src/core/src/zava_forward/core/continuity.py:72-76 calls task.removeprefix without checking its type. epoch_current at lines 93-112 does not distinguish a supported old priority record from a generic assistant entry missing its task identity, accepts any string suspension scope, permits missing intermediate event epochs and treats an empty restart object as a suspension-only boundary. The export consumer at lines 518-522 passes p.get("capability"), which can be None.
* Independent reproduction: actual extracted epoch_current returned True for an unrelated epoch-0 record with each of (a) an unregistered suspension scope, (b) epoch 3 with only suspension boundaries 1 and 3, and (c) a status=Restarted history entry with restart={} and epoch 1. A generic proposal containing only id and continuity_epoch=1 passed the helper against epoch-1 history; the actual export condition then raised AttributeError on active(doc, None).
* Impact: malformed/incomplete retained history can be classified as current despite the explicit fail-closed contract, and a generic historical export entry can prevent evidence export after an incident. The probe does not establish a bypass of independent release or actual-hold checks.
* Destination: later rpi-implement.
* Smallest useful next action: validate canonical registered task/scope and coherent suspension/restart event coverage before granting epoch currentness; handle missing/unknown task identities conservatively without exceptions. Preserve supported old valid documents and explicit historical unknowns. Add malformed-history, missing-task and generic export cases through runtime consumers, not only helper assertions.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Identity and sign-in-route restart denials bypass the durable denial audit

* Related scope: P01-T01/P01-T02, AC4, denial-audit/current-identity requirements.
* Evidence: src/core/src/zava_forward/core/continuity.py:209-211 performs current-actor lookup and inactive-staff rejection before the try/except whose lines 241-246 create and persist ai_restart_decide_denied. src/api/src/zava_forward/api/server.py:860-862 rejects a password-route restart before invoking that wrapper.
* Independent reproduction: executed the actual extracted _incident_action decorator with a current-actor lookup that raises PermissionError and an audit collector. The decision was refused and the collector contained zero audit entries. The password HTTP early-return gap is additionally directly visible in source.
* Impact: the highest-value stale/forged/inactive identity and untrusted-route restart attempts leave no durable restart-denial record, contrary to the stated audit contract. They remain denied; permission enforcement itself is not bypassed.
* Destination: later rpi-implement.
* Smallest useful next action: persist a bounded denial event for these early authenticated attempts without attributing verified authority to an invalid actor and without changing incident state. Exercise password HTTP, current-identity mismatch and inactive-staff denials, including reopen, exactly-one audit and failure rollback.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Constructed post-restart export contradicts current proposal views

* Related scope: P01-T01/P01-T02, PC-001/PC-004, constructed-only restart and consistent export evidence.
* Evidence: src/core/src/zava_forward/core/assistants.py:481-483,535-540,677-685 supplies constructed=True for a non-Ai fixture provider when applying continuity holds. src/core/src/zava_forward/core/continuity.py:518-522 reprojects the same exported proposals using active with its default constructed=False and overwrites epoch_current=False as well as reliance/actionability.
* Independent reproduction: actual extracted helpers on a task incident suspended at epoch 1, constructed-restarted at epoch 2 with actual_hold=True, and a fresh task proposal recorded at epoch 2 returned epoch_current=True and no constructed assistant hold, but the continuity export hold was True. The actual export branch therefore strips the fresh constructed eligibility and reports its valid epoch as noncurrent.
* Impact: a permitted fresh constructed proposal can be actionable/relied on in assistant views and its source export but represented as noncurrent/non-relied-on in the supplier-independent bundle. This damages the synthetic drill's evidence consistency, not actual-use safety.
* Destination: later rpi-implement.
* Smallest useful next action: align bundle projection with trusted current constructed-versus-actual context, keeping actual_hold effective for actual providers and not trusting caller-supplied authority flags. Test fresh constructed ready/accepted detail/list/export parity and actual-provider switch/reopen denial.

<!-- rpi:review id=RV-005 -->
### RV-005 [Low, residual]: Committed candidate, native SQL/full17 and sealed handoff remain unexecuted

* Related scope: P02-T02 and unchecked engineering gate criteria.
* Evidence: plan, details, changes and parent handoff consistently say the candidate is uncommitted and native SQL/Docker/full17 occur after this original Review. HEAD still equals the supplied base. The focused run has 36 opt-in skips, not native SQL passes.
* Impact: no exact committed-head/local full-gate or receipt acceptance can yet be claimed. This expected sequencing is not a newly discovered source defect.
* Destination: distinct active-parent delivery/platform continuation.
* Smallest useful next action: preserve this adverse original Review, commit only under the parent's authorized identity/workflow, then use an eligible environment to run the unchanged full gate against the frozen candidate and retain the named non-skipped native bridge result and verified external receipt. If prerequisites fail, record the actual error/blocked status. Respect the stop-before-push/PR direction. A passing gate cannot erase RV-001 through RV-004.

<!-- rpi:review id=RV-006 -->
### RV-006 [Medium, residual]: Actual authority, competent evidence and operational acceptance remain human-blocked

* Related scope: plan Follow-Up Items, FR-053/AC-072/NFR-014, RULE-024/AC-078/RULE-020 and open OD-35.
* Evidence: the plan, details, changes, source actual_authority/actual_hold and component guides explicitly retain unavailable actual appointment, approved monitoring thresholds, competent corrective-test acceptance and human-witnessed drill. Original #219 RV-004 remains open; the later #219 correction evidence resolved only its bounded RV-001 through RV-003 engineering defects.
* Impact: neither a constructed restart nor future local/native gate success establishes actual restart permission, live safety, lawful cohort evaluation, professional acceptance or whole-issue closure.
* Destination: distinct governance, evaluation and human-acceptance follow-ups listed above; #222 remains separately owned.
* Smallest useful next action: the named human owners record their actual authority and approved evidence before any future affected operational restart; preserve current fail-closed actual use. No cloud/live activation or cohort exercise is authorized here.

## Defects

* RV-001 Medium: incomplete legacy impacted evidence is labelled complete.
* RV-002 Medium: historical task/epoch handling permits malformed history or raises during export.
* RV-003 Medium: early identity/sign-in-route restart denials are not durably audited.
* RV-004 Medium: fresh constructed export eligibility contradicts runtime views.
* No Critical or High finding; no actual-authority or dispatch bypass demonstrated.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Later rpi-implement | Core/API owner includes legacy evidence in completeness and adds historical snapshot regressions | Defect within accepted contract |
| RV-002 | Later rpi-implement | Core/API owner validates historical task/event structure and tests generic export without exceptions | Defect within accepted fail-closed contract |
| RV-003 | Later rpi-implement | Core/API owner covers early denial paths with safe, durable exactly-once denial records | Defect within accepted audit contract |
| RV-004 | Later rpi-implement | Core/API owner aligns trusted constructed/actual export projection with runtime and tests parity | Defect within accepted constructed-only contract |
| RV-005 | Active-parent delivery/platform continuation | Commit/freeze, permitted native/full17 execution and honest sealed receipt/handoff | Expected remaining delivery work, not source defect |
| RV-006 | Distinct named human follow-ups | Governance, evaluation, operational acceptance and separate #222 owners | Known out-of-scope human authority/evidence, not new active implementation |

No rpi-plan or rpi-research route is needed. Later implementation does not
require another Review. No production changes follow this Review in the
current task; route defects to distinct later work and preserve this outcome.

## Residual Work

* RV-005 remains active-parent P02-T02 delivery work, separate from source fixes.
* RV-006 remains outside bounded engineering acceptance; do not check those
  criteria using constructed claims, local/native tests or role-agent output.
* Original #219 adverse findings and later correction evidence remain
  historical records, not relabelled or replaced by this #221 assessment.

## Blockers and Remaining Work

* Review blockers: none. Supplied artifacts, static source and in-memory
  probes suffice for a complete bounded adverse verdict.
* Engineering acceptance blockers: RV-001 through RV-004. Passing focused
  tests does not establish these missing edge/lifecycle semantics.
* Remaining active delivery: P02-T02 commit, native SQL/Docker/full17 and
  exact-candidate receipt/handoff, RV-005. No remote action is authorized.
* Human/live acceptance: RV-006, deliberately unavailable. Missing actual
  authority remains a hold rather than a default grant.
* Reviewer execution limitation: system Python lacks installed zava_forward
  distributions, the offered interpreter/logs reside in a prohibited path
  for this reviewer, and fixture-generating suites would violate the
  only-review-record write boundary. No dependency install, disk-fixture test
  run or native gate was attempted.

## Validation Evidence

| Command / evidence | Scope | Status | Result and limits |
| --- | --- | --- | --- |
| Parent-supplied credential-scrubbed pre-Review focused run: test_operator_suspension test_continuity test_continuity_epoch_export test_assistant_release test_auth | Focused API/continuity/release/auth | Passed with skips, reported | 162 run, OK, 36 opt-in skips. Exact external log named in changes/user handoff; not opened here because of reviewer path restriction. Not 162 non-skipped passes or native SQL proof |
| Parent-supplied core/API Ruff and mypy | Core/API production and owning tests | Passed, reported | Core 128/API 63 source files type-checked according to changes; no claim of independently repeating them |
| git diff --check | Complete tracked candidate diff | Passed, independently executed | No whitespace errors |
| env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=<current> python3 -B, AST parse of all changed Python files | Nine tracked Python files plus untracked issue test | Passed, independently executed | 10 files parsed; no bytecode written; pyproject.toml also parsed with tomllib |
| Same scrubbed python3 -B, extracted actual active/epoch_current/_incident_action functions | Historical eligibility, export predicate and early identity-denial audit | Executed; defects reproduced | Fresh constructed current=True but default export hold=True; unknown/missing-event/empty-restart history current=True; generic export predicate AttributeError; current-identity denial produced zero audit entries. Minimal in-memory collaborators, not full owning suites |
| Same scrubbed python3 -B, actual extracted validate_sql with sqlite3 :memory: | Legacy impacted snapshot completeness | Executed; defect reproduced | Legacy affected row retained all version/reference fields as None while snapshot_complete=True. Current-candidate dependency supplied as complete to isolate validator |
| python3 -B -c import zava_forward.core | Reviewer installed distribution availability | Failed | ModuleNotFoundError. No installation or source-path workaround performed |
| Independent full focused-suite repeat | Owning synthetic suites | Skipped | Only-review-record write boundary disallows their generated fixture files; prohibited offered interpreter/log path not used |
| Named native SQL bridge / Docker / all17 / sealed receipt | Actual disposable SQL and exact committed candidate | Not run, pending parent | Explicit post-Review/commit sequence; no success inferred from selector presence or skips |
| Actual provider, approved thresholds/evaluation, appointed authority, human drill, cloud/cohort work | Operational/human acceptance | Not run / unavailable | Outside authorization; unavailable authority retained fail-closed |

The source-function probes execute actual parsed definitions, but isolate
their dependencies in memory. They establish the cited local behaviors,
not an end-to-end database, HTTP, provider or operational acceptance result.
No reviewer-authored fixture, scratch, dependency, cache or source file was
created; only this canonical review record was written.

## Outcome

* Outcome: Not accepted.
* Execution status: Complete for this one original Review; Partial for
  overall implementation/delivery because P02-T02 remains pending.
* Severity summary: 0 Critical, 0 High, 4 Medium implementation defects;
  separately 1 Medium human residual and 1 Low delivery residual.
* Rationale: the core direction and much semantic engineering are credible,
  including persistent actual-provider denial, current local identity,
  exact candidate drift, manual/hazard continuity and normal rollback. The
  complete supplied contract is not established because incident
  completeness, malformed historical handling, early denial audit and
  constructed export parity have reproducible gaps. No actual approval,
  live activation, human acceptance, issue closure or gate success follows.
* Original negative result is preserved. No fixes or second Review were
  performed or requested in this task.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement, RV-001 through RV-004 | Core/API owner creates distinct later correction work with owning regressions; no production correction now |
| Decision gap or invalid assumption | None | No divergent authority/product decision is needed to implement the already frozen contract |
| Material new research gap | None | Existing confirmed requirements and source evidence are sufficient for this verdict |
| Non-blocking delivery residual | Active parent, RV-005 | Preserve adverse Review, complete authorized commit/gate/handoff with honest status; stop before push/PR |
| Non-blocking human residual | Distinct follow-ups, RV-006 | Named governance/evaluation/acceptance owners; #222 separate |

* Validation coverage: reported 162-test focused run with 36 skips and static
  checks; independent whitespace, syntax/TOML and no-write behavioral probes.
* Remaining blockers: four engineering defects, unexecuted native/full gate
  and unavailable actual/human authority/evidence. These are not conflated
  with review execution completeness.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-20/operator-suspension-221-research.md](.copilot-tracking/research/2026-10-20/operator-suspension-221-research.md) | Canonical C1-C8 evidence and bounded readiness |
| [.copilot-tracking/plans/2026-10-20/operator-suspension-221-plan.md](.copilot-tracking/plans/2026-10-20/operator-suspension-221-plan.md) | Current markers, criteria, dispositions and follow-ups |
| [.copilot-tracking/details/2026-10-20/operator-suspension-221-phase-details.md](.copilot-tracking/details/2026-10-20/operator-suspension-221-phase-details.md) | Frozen corrective contract and actual test allocation |
| [.copilot-tracking/reviews/2026-10-20/operator-suspension-221-plan-critique.md](.copilot-tracking/reviews/2026-10-20/operator-suspension-221-plan-critique.md) | Preserved original Revise, PC-001 through PC-007 |
| [.copilot-tracking/changes/2026-10-20/operator-suspension-221-changes.md](.copilot-tracking/changes/2026-10-20/operator-suspension-221-changes.md) | Reported attempts, failures, final checks and open work |
| [.copilot-tracking/rpi-sessions/2026-10-20/operator-suspension-221-state.json](.copilot-tracking/rpi-sessions/2026-10-20/operator-suspension-221-state.json) | Parent automatic continuation state, unchanged |
| [.copilot-tracking/reviews/logs/2026-10-20/operator-suspension-221-review.md](.copilot-tracking/reviews/logs/2026-10-20/operator-suspension-221-review.md) | This one original complete adverse Review |
| [src/api/tests/test_operator_suspension.py](src/api/tests/test_operator_suspension.py) | Untracked issue-owned semantic tests and shared native drill |
| [src/api/tests/test_assistants.py](src/api/tests/test_assistants.py) | Existing selected native SQL class and new bridge |
| [src/core/README.md](src/core/README.md) | Core incident/authority contract, qualified by findings |
| [src/api/README.md](src/api/README.md) | API/auth/structured claim contract, qualified by findings |
| [docs/prds/zava-forward-retrofit-programme-demonstrator.md](docs/prds/zava-forward-retrofit-programme-demonstrator.md) | FR-053/AC-072/NFR-014/OQ-017 acceptance basis |
| [docs/brds/agentic-retrofit-programme-brd.md](docs/brds/agentic-retrofit-programme-brd.md) | RULE-024/AC-078/RULE-020 and open OD-35 |
| [.copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md](.copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md) | Preserved original #219 adverse findings |
| [.copilot-tracking/reviews/logs/2026-10-15/rai-reliance-review-fixes-219-review.md](.copilot-tracking/reviews/logs/2026-10-15/rai-reliance-review-fixes-219-review.md) | Later bounded #219 correction evidence, not actual acceptance |

## Next Steps

The active parent preserves this Complete / Not accepted original Review,
routes RV-001 through RV-004 to distinct later rpi-implement work without
production edits or a repeat Review in this task, and owns remaining
authorized P02-T02 commit/gate/handoff under RV-005. Record any unavailable
gate prerequisite honestly and stop before push/PR. RV-006 stays with its
separate human owners; no actual authority or operational acceptance is
inferred. No user decision or action is required for this bounded handoff.
