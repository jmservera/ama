---
title: Capacity page 523 original independent implementation Review
ms.date: 2026-10-31
---

## Opening Review State

Task 523 / capacity-page-523. Execution: pending independent assessment.
Frozen source commit 2bb4e561, synchronized topic HEAD 19d17abf, reviewed base
1330869ea675ff019958846330108b4f45e163ce. Supplied boundary is exactly one
47-line method in src/api/tests/test_procurement_api.py plus dated original RPI
evidence. Runtime/browser/fixture/manifests unchanged relative to reviewed main.

Plan/details P01/P02 completed; P03 independent Review, evidence commit, complete
publication gate and push/PR remain pending. Caller-required tests and Ruff pass;
raw logs and mutation evidence are available in external session files. Research
actually exercised SQL Server/Chromium with twelve manager routes. Axe NOT RUN,
321 existing API skips, live owner verification and human/hosted approval remain
explicitly separate. No review blocker established at opening.

Review may write only this record; no source/artifact edits elsewhere, nested
agents, heavy validation, credentials, live sign-in or remote changes.

* Interpreted review goal: execute the task's one original independent
  post-implementation Review, assessing regression semantics, backend ownership,
  evidence reconciliation and acceptance limits without implementing changes.
* Evidence readiness: supplied dated research, plan, details, original critique,
  changes and state form one unambiguous task set; raw executor logs and the
  mutation runner are available for read-only inspection.
* Acceptance basis: confirmed regression-only direction, plan P01/P02/P03 and
  follow-ups, original PC dispositions and recorded issue requirements; engineering
  evidence is not live acceptance or authorization to close #523.
* First comparison boundary: the complete 47-line source diff against reviewed
  main, then its owning fixture/runtime and original RPI/log evidence. No broad
  repository audit or new execution is in scope.
* Initial workspace state: branch fix/capacity-page-523; existing changes/state
  modifications and this untracked review record are retained, not adopted or
  moved. Only this review record may be written.

## Scope and Evidence

* Task ID: 523; task slug: capacity-page-523; review date: 2026-10-31.
* Assessment count: one original independent post-implementation RPI Review.
* Source boundary: the complete added method
  ProcurementApi.test_legacy_capacity_reads_survive_store_reopen_without_inventing_authority
  in src/api/tests/test_procurement_api.py, including inherited JSON execution.
  Against reviewed main there are exactly 47 additions and no deletions in
  executable source. The remaining topic diff is six dated RPI artifacts;
  this record is the seventh. Existing changes/state modifications were read
  as current supplied evidence and left untouched.
* Compared artifacts:
  .copilot-tracking/research/2026-10-31/capacity-page-523-research.md;
  .copilot-tracking/plans/2026-10-31/capacity-page-523-plan.md;
  .copilot-tracking/details/2026-10-31/capacity-page-523-phase-details.md;
  .copilot-tracking/reviews/plans/2026-10-31/capacity-page-523-plan-critique.md;
  .copilot-tracking/changes/2026-10-31/capacity-page-523-changes.md;
  .copilot-tracking/rpi-sessions/2026-10-31/capacity-page-523-state.json.
* Owning evidence: fixture and JsonProcurementApi in the changed test file;
  src/core/src/zava_forward/core/sqlstore.py,
  src/core/src/zava_forward/core/store.py,
  src/core/src/zava_forward/core/appointments.py,
  src/core/src/zava_forward/core/procurement.py; src/README.md and the
  clean_identity contract in tools/rpi-checks.py. Project index, memory and
  both case-study documents were consulted for context, not new acceptance.
* External supplied evidence inspected read-only: mutation.log,
  procurement.log, api-unittest.log and capacity523-mutation.py under the
  caller-supplied session files directory. The three raw log hashes match
  the changes record. No browser log or separate Ruff/mypy transcript was
  supplied here; those results retain their recorded-executor attribution.
* Issue/history and research browser results are assessed through the supplied
  Research C1-C7/W1-W3, not a fresh GitHub query, browser run or live sign-in.

## Execution Status

* Review execution status: Complete. The complete frozen source diff, current
  artifact set, original critique dispositions, owning storage paths, mutation
  identity, raw suite summaries and synchronized ancestry were assessed.
* Implementation execution status: P01/P02 Complete; full plan Partial because
  P03 publication work is pending. This record completes the independent
  assessment for P03-T01; the coordinator must persist completed markers/state.
* No tests, mutation, browser checks, gates, installs, credential operations,
  live verification or remote writes were performed by this reviewer. Read-only
  Git inspection and log hashing are reconciliation, not fresh test execution.

## Plan-to-Change Reconciliation

| Current plan scope | Changes/state evidence | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01/P01-T01, AC2 | One 47-line method, backend factory and SQL-only cleanup | Reconciled | Same accepted regression-only scope; no runtime/fixture/helper edits or new skips |
| P02/P02-T01, AC3/AC4 | Mutation, owning/API logs, reported Ruff/mypy, completed markers | Reconciled | Earlier 600-second admission timeout is superseded by the recorded successful 1200-second consolidated admission/run, not erased |
| P03-T01, AC5 | Original Complete/Revise critique retained; this one independent Review | Reconciled at closeout | Supplied plan/details/state still correctly describe Review as pending/active at intake; coordinator owns completion bookkeeping |
| P03-T02, AC6 | Source/evidence commit 2bb4e561 and topic merge 19d17abf exist | Partial | Review/current bookkeeping commit, full gate, verified receipt and independent exact-head assessment remain pending, RV-001 |
| P03-T03, AC6 | Topic/main-target publication is planned, not claimed | Pending | No push or PR result is established by this evidence, RV-001 |
| Follow-Up Items | Live owner verification and hosted/human approval remain open in changes | Reconciled | Separate from active implementation acceptance, RV-002/RV-003 |

The changes record's earlier "queued" validation wording preserves chronology.
Its Validation Record, Pre-Review Reconciliation and Return-to-Caller State
provide the later completed result; there is no unresolved test failure hidden
by that earlier paragraph. No stale handoff prevents this assessment.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 | src/api/tests/test_procurement_api.py | Add persisted legacy reopen coverage missing from the existing same-instance legacy read test | Complete diff; actual fixture/storage contracts; 34-test owning suite OK | Conformant within the bounded regression requirement |
| P02-T01 | No further source changes | Demonstrate original-defect sensitivity and preserve existing behavior | Matched raw mutation/owning/API log hashes; recorded lint/type checks | Conformant with disclosed opt-in skips and evidence provenance |
| P03-T01 | This review record only | Independently reconcile source, evidence and acceptance limits | One complete assessment, findings and routes below | Complete; no correction or second Review is requested |

### Semantic validity and backend ownership

* Setup first records valid capacity and issues a valid order with
  RESIDENT_BINDINGS. It removes only package contract_version under the owning
  lock and saves. Unlike the existing legacy test, it does not also remove
  resident bindings, so the missing contract metadata is the isolated cause.
* Reopening uses self.make_store(self.path), not a forced SqlStore constructor.
  ProcurementApiFixture.sql selects SQLite-backed SqlStore; JsonProcurementApi
  inherits the method with sql = False and selects Store. The saved original
  type check and SQL db_path assertion guard backend/path ownership.
* SQLite reopen is a real new connection to the already populated fixture DB.
  SqlStore._seed reads source JSON only when its cases table is empty;
  _proc_sync loads procurement from SQL meta. The post-reopen snapshot equality
  is therefore not a fresh JSON seed disguised as SQL persistence coverage.
  JSON Store loads saved live.json instead of the original synthetic seed.
* Original SQL connection cleanup remains registered. New SQL connection
  cleanup is registered before assertions can fail; JSON has no DB cleanup.
  The existing HTTP shutdown closes the server before original fixture
  disposal. Keeping the original connection open while opening another proves
  constructed-store reload, not a process crash/restart or live Azure SQL
  recovery; no stronger guarantee is claimed.
* Both self.store and self.app.store point to the reopened object before HTTP
  reads. The unchanged synthetic staff in the existing authentication fixture
  make its retained original provider reference immaterial to this regression;
  the HTTP handlers exercise the reopened procurement store.
* Each GET executes twice and checks 200 plus exact package/order identity.
  Null contract projections and Unknown appointment-control status preserve
  missing authority rather than inventing an authorization. Preserved resident
  bindings are explicitly checked in the current binding.
* Deep-copied procurement comparisons detect metadata/content changes; audit
  comparisons detect added entries on reads. SqlStore.audit_entries queries
  the actual ledger, while Store.audit_entries reads its persisted JSONL ledger.
  These are stronger than comparing response payloads alone. Audit is captured
  after reopen, so the assertion concerns GET invariance, not constructor-wide
  audit invariance.
* The final offer request asserts 403, the current-authority explanation and
  unchanged procurement. It intentionally does not assert that denied writes
  cannot generate audit; the plan's audit-invariance requirement concerns GETs.
* The counterfactual adds strict package["contract_version"] access to the
  inherited binding method only in the executor process. Its recorded stack
  reaches appointment_summary through /api/workorders at the new test's GET,
  raises exactly KeyError('contract_version') server-side and RemoteDisconnected
  client-side. The runner requires one executed unskipped test, exactly one
  error, no assertion failures and the exact missing-key identity before its
  sensitivity PASS. This is not an import/setup error or a success proxy.
  Mutation sensitivity was demonstrated for SQL; inherited JSON normal behavior
  is covered by owning-suite discovery, not by a second mutation claim.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence/user decision | Reconciliation and planning state | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01/P02-T01 | Clarify SQL and inherited JSON reopen/cleanup and execution | Original PC-001; compatible correction, no product decision needed | Plan, details, changes and actual method all use existing factory; original critique preserved | Applied correctly without scope expansion |
| P02 execution readiness | Retain shared lock and external environment/output use | Parent explicitly establishes absence of the alleged parent prohibition; recorded successful admission/pip/SQL execution | PC-002 rejection documented in plan/details/changes/state; no gate/lock bypass | Supported disposition; review-local restrictions are not retroactive parent rules |
| P03 ancestry | Commit then non-rewriting synchronization merge of current main | Main advanced while validation waited; clean_identity requires current-main ancestry | Plan/details/changes/state preserve historical initial base and current reviewed base | Compatible procedural update, not divergent runtime scope |

## Critique and Material Revision Assessment

* Exactly one original critique remains Complete / Revise, with PC-001 Medium
  and PC-002 High. Its adverse text and original base are preserved, not
  rewritten into a passing critique.
* PC-001 is applied and resolved by actual backend-preserving implementation.
  The owning suite's 34-test OK summary is not verbose per-test output, but
  normal unskipped unittest inheritance/discovery and the unchanged sql = False
  subclass establish both new instances; no JSON applicability skip was added.
* PC-002 is rejected, not silently resolved or converted into a gate pass.
  Its alleged temporary-directory prohibition is absent in the parent's
  context as explicitly supplied for this Review. The actual mandated shared
  lock/external operations are allowed there and recorded as successful.
  This review's own no-temporary-write boundary is obeyed and is not imported
  into historical parent execution. Publication still requires its real gate.
* Backend clarification and current-main synchronization preserve confirmed
  regression-only intent. No significant/unaccepted design decision or
  invalid product assumption requires rpi-plan; no dependent work resumed
  on an unresolved material product decision.
* Source commit 2bb4e5616042e3e3ff24d5d4916cae27ea084b70 has initial base
  5666bd33e1827670e5c07e3e3063bbbe989b59d3 as parent. Merge
  19d17abfabd6b7c1042f6744e411e9108f57c8f5 has that source commit and
  reviewed main 1330869ea675ff019958846330108b4f45e163ce as parents.
  Both commit messages retain the required Copilot trailer. Identity operations
  are recorded by the coordinator, not repeated or independently authenticated
  by this reviewer.
* Read-only comparison of initial base to reviewed main finds no src/api or
  src/core changes. Main's infra/workflow/gate/docs changes are unrelated to
  this test's runtime inputs, so the prior owning/API execution remains relevant.
  It is not an exact-head full gate on the new tooling/base or a publication
  receipt. The complete current source diff is still only the added method.

## Acceptance and Validation Evidence

| Criterion/check | Status | Evidence and limits |
| --- | --- | --- |
| AC1: current local manager capacity/recovery | Passed in supplied Research | Actual owned SQL Server/Chromium generated 980 fictional cases, 443 open, one package/601 orders; all twelve manager routes and failure/retry/draft/delayed-401/cancel/empty checks passed. Not rerun by Review |
| AC2: persisted legacy HTTP regression | Passed | Complete semantic comparison and owning 34-test log, 29.138s, OK; both SQLite and inherited JSON instances, no added skips |
| AC3: strict-lookup counterfactual | Passed as sensitivity | mutation.log shows expected one-error test failure, 0.893s; runner validates exact failure identity and reports PASS/exit 0. The intentional FAILED unittest is not a normal-suite failure |
| AC4: requested API discovery | Passed | From src/api, exact requested PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests; recorded discovery -s tests -q ran 1433 tests in 579.986s, OK (skipped=321) |
| ruff check . | Reported Passed | Changes record/consolidated executor result says all checks passed; separate raw Ruff transcript unavailable to this Review |
| ruff format --check . | Reported Passed | Recorded 65 files already formatted; not independently rerun |
| Focused mypy; git diff --check | Reported Passed | Recorded no issues in changed test file and whitespace check passed; supplemental, not a complete gate |
| Shared-lock initial admission | Failed admission, not test execution | Initial 600-second timeout exited 1 without tests; retained. Later 1200-second consolidated admission/run exited 0; no holder interruption or serialization bypass claimed |
| AC5: original independent assessments | Complete | One retained Complete/Revise critique with explicit dispositions and this one Complete original Review |
| AC6: final candidate/publication | Pending | Source/topic synchronization committed; final Review/bookkeeping commit, full post-commit gate, receipt verification, independent exact-head assessment and topic push/PR not completed here |
| Axe/accessibility acceptance | NOT RUN | Research supplied no axe and reported four scans NOT RUN. Neither the test-only change nor engineering checks establish WCAG, assistive-technology or whole Fluent acceptance |
| Live owner verification; hosted/human approval | Not performed/pending | Explicit separate follow-ups, not inferred from local SQL/browser or API results |

Matched raw log SHA-256 values:

* mutation.log: 5f0d1eafd0aa61eae128d35e076a387098aeea1f56f6e63e80e341f9177c1e90.
* procurement.log: ed5b8f801131a86b0c4fdf62ef31f957b1a542ce57965233f7e5aa70e2393709.
* api-unittest.log: 6637135a9b3f9002683b708e4a953a7a0b6a7a131580da254477d9a58795ef7b.

The 321 existing opt-in skips are disclosed, not counted as executed tests or
real SQL/browser/live checks. Research's real SQL Server exercise is separate
from the new SqlStore regression's SQLite coverage. No AI-configuration causal
claim, live service repair, operational authority or issue closure follows.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate implementation scope | Owner/next action | Assessment and route |
| --- | --- | --- | --- |
| Live employee-site verification | Requires separately authorized deployment and owner observation; no live sign-in in this task | Owner | Open distinct follow-up, RV-002; not added to P01/P02 |
| Hosted checks and human approval | Can occur only after legitimately gated publication and remain separate approval decisions | Coordinator then owner/reviewer | Open distinct follow-up, RV-003; not replaced by local checks |

The changes record mirrors both items. Missing axe is an explicitly disclosed
acceptance limit, not a newly invented mandatory test-only implementation task.
Any broader accessibility acceptance must be separately scoped and authorized.

## Findings

Severity summary: 0 Critical, 0 High, 1 Medium, 2 Low. These are remaining
publication/acceptance actions, not defects in the implemented regression.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Final publication qualification is still outstanding

* Related scope: P03-T02/P03-T03, AC6.
* Evidence: supplied changes/state and current dirty/untracked evidence inputs;
  src/README.md full gate protocol; tools/rpi-checks.py clean_identity.
  No final receipt or independent exact-head acceptance is supplied.
* Impact: implementation test passes cannot authorize push/PR. The current
  uncommitted Review/bookkeeping inputs are not a sealable final candidate.
* Destination: distinct coordinator-owned P03 publication action, not
  rpi-implement, rpi-plan or rpi-research.
* Smallest useful next action: reconcile P03-T01/state after receiving this
  record; commit the original Review and final bookkeeping with required
  privacy-safe identity/trailer; fetch main and run the required complete
  post-commit external gate against current reviewed origin/main. Verify its
  immutable receipt immediately before push and independent exact-head
  assessment. Any subsequent commit/input/base/tool change invalidates it.
  Publish only if all requirements pass, topic-only, PR to main with Refs #523.
  Do not merge, use a closing keyword or substitute partial/cloud evidence.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Live owner verification remains a distinct acceptance follow-up

* Related scope: plan Follow-Up Items; Research W1 and residual uncertainty.
* Evidence: research/changes explicitly leave employee-site live verification
  unchecked despite merged #528/#577 repairs and local SQL/Chromium success.
* Impact: whole-issue/live acceptance is unproven; no issue closure or live
  configuration-causation conclusion is supported.
* Destination: distinct owner-owned live verification follow-up after separately
  authorized deployment; not new active regression implementation.
* Smallest useful next action: owner records observed employee-site behavior and
  acceptance when authorized. Keep live status pending and Refs #523 meanwhile.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Hosted checks and human approval cannot be inferred locally

* Related scope: plan Follow-Up Items; P03-T03.
* Evidence: no published PR/checks or human approval results in this supplied
  task set; local requested validation and future full receipt are distinct.
* Impact: this original Review is neither hosted approval nor permission to
  merge, deploy or accept operational/legal/accessibility controls.
* Destination: distinct hosted/human approval follow-up, coordinator and
  owner/reviewer after RV-001's legitimate publication.
* Smallest useful next action: let actual PR checks run, preserve their outcomes
  and obtain the required human decision. Do not fabricate statuses or weaken
  protections to clear the follow-up.

## Defects and Routed Findings

* No demonstrated source defect, material decision gap or material research gap
  was found in the accepted regression-only boundary.

| Finding | Destination | Owner/next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 Medium | Coordinator P03 publication | Final evidence commit, complete gate, verified receipt, exact-head assessment then eligible topic push/PR | Planned qualification is pending, not an implementation defect |
| RV-002 Low | Distinct live verification follow-up | Owner, separately authorized employee-site observation | Operational acceptance outside immediate regression scope |
| RV-003 Low | Distinct hosted/human approval follow-up | Coordinator and owner/reviewer after publication | Independent approvals cannot be synthesized locally |

Later implementation of any separately routed work does not require this
original Review to run again. Independent exact-head publication assessment is
still required and is not a second original implementation Review.

## Blockers and Remaining Work

* No blocker to this Review or P01/P02 regression acceptance is established.
* Publication is not yet eligible: RV-001 qualification is pending; final
  Review/current evidence are uncommitted at closeout. A later actual gate
  failure or missing prerequisite must be retained as a publication blocker.
* P03-T01 assessment is complete in this record. Coordinator owns plan/details/
  changes/state completion markers and final commit; this reviewer changes none
  of them.
* P03-T02/P03-T03 remain active planned work. RV-002/RV-003 remain separate
  follow-ups. Axe NOT RUN and live/human limitations remain visible.

## Outcome

* Outcome: Residual work.
* Outcome rationale: bounded P01/P02 implementation is conformant and no source
  correction is recommended. The task's full publication/acceptance boundary
  still has the explicit RV-001/RV-002/RV-003 actions. Complete Review execution
  does not make P03 publication complete, establish a full gate pass or close #523.
* Review recommendation: return this original record to the active coordinator
  for the planned publication steps and separate follow-up ownership; no
  rpi-implement/rpi-plan/rpi-research invocation is warranted by this finding set.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defect | None | No demonstrated defect in the complete scoped diff |
| Decision gap/invalid assumption | None | Compatible PC-001 correction and PC-002 rejection are reconciled |
| Material evidence gap | None in regression boundary | Preserve executor attribution, skipped checks and acceptance limits |
| Remaining planned qualification | Coordinator P03, RV-001 | Commit, full gate, receipt verification and exact-head assessment before eligible publication |
| Non-blocking residual acceptance | Distinct follow-ups, RV-002/RV-003 | Live owner verification and hosted/human approvals |

* Execution status: Review Complete; P01/P02 Complete; full plan Partial.
* Outcome: Residual work; regression-only implementation conformant.
* Validation coverage: matched mutation/owning/API raw evidence, reported
  Ruff/format/type results, supplied actual local SQL/Chromium research;
  no reviewer reruns, no axe/live/hosted/human acceptance or final receipt.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/capacity-page-523-research.md](.copilot-tracking/research/2026-10-31/capacity-page-523-research.md) | Original research and local SQL/Chromium evidence |
| [.copilot-tracking/plans/2026-10-31/capacity-page-523-plan.md](.copilot-tracking/plans/2026-10-31/capacity-page-523-plan.md) | Current accepted scope, criteria and follow-ups |
| [.copilot-tracking/details/2026-10-31/capacity-page-523-phase-details.md](.copilot-tracking/details/2026-10-31/capacity-page-523-phase-details.md) | Backend, validation and publication details |
| [.copilot-tracking/reviews/plans/2026-10-31/capacity-page-523-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/capacity-page-523-plan-critique.md) | Retained original Complete/Revise critique |
| [.copilot-tracking/changes/2026-10-31/capacity-page-523-changes.md](.copilot-tracking/changes/2026-10-31/capacity-page-523-changes.md) | Implementation and executor validation record |
| [.copilot-tracking/rpi-sessions/2026-10-31/capacity-page-523-state.json](.copilot-tracking/rpi-sessions/2026-10-31/capacity-page-523-state.json) | Supplied active-parent state |
| [src/api/tests/test_procurement_api.py](src/api/tests/test_procurement_api.py) | Complete changed method and owning backend fixtures |
| [.copilot-tracking/reviews/logs/2026-10-31/capacity-page-523-review.md](.copilot-tracking/reviews/logs/2026-10-31/capacity-page-523-review.md) | This one original independent Review |

## Next Steps

Active coordinator receives this result and completes RV-001's planned
bookkeeping/commit and full publication qualification before any push/PR.
Keep RV-002/RV-003 with their distinct owners and live/axe/approval limitations
explicit. This reviewer stops here; no user action, second original Review,
source correction or new RPI stage is requested.
