<!-- markdownlint-disable-file -->
# RPI Plan Critique: Bounded pending-document rescans

## Metadata

* Task ID: 117
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/issue-117-document-rescan-scheduler-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/issue-117-document-rescan-scheduler-phase-details.md
* Critique execution status: Complete
* Candidate base: ebc8dab87ae9bd6a33380b85e86f38be5ed9f213
* Branch inspected: feat/document-rescan-scheduler-117
* Execution boundary: exactly one final-candidate Plan critique; no implementation, original Review, nested delegation or second critique.

## Inputs and Criterion Boundary

* Caller requirements: bounded existing-pattern offline SQL rescan invocation;
  pending, unavailable, malformed and failed results never become clean;
  no worker deletion or hold-release authority; preserve scan-before-availability,
  owner-controlled retention, merged102 audit/progress corrections and resident/
  sensor guards. Maximum two new test files, owned by core and orchestrator,
  without test removal or generated targets. Actual owned loopback SQL, offline
  CLI and hardened Docker execution are required.
* Candidate inputs: the plan and phase-details paths above, plus
  .copilot-tracking/research/2026-10-17/issue-117-document-rescan-scheduler-research.md.
  Research C1-C8 and W1-W2 were considered as supplied evidence; historical
  GitHub claims were not independently refreshed.
* Current source checked: src/core/src/zava_forward/core/doc_controls.py,
  src/core/src/zava_forward/core/sqlstore.py,
  src/core/src/zava_forward/core/mssqlstore.py,
  src/core/src/zava_forward/core/change_provenance.py,
  src/core/src/zava_forward/core/factory.py,
  src/core/src/zava_forward/core/documents.py,
  src/core/tests/test_progress_event_capture.py,
  src/orchestrator/src/zava_forward/orchestrator/source_monitor.py,
  src/orchestrator/Dockerfile, src/orchestrator/pyproject.toml,
  src/check-container.py and the core/orchestrator READMEs.
* Project boundary checked: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md,
  docs/reference/memory.md, ADR 0002 decision 2 and the current PRD DH-003
  source excerpts. No new regulatory interpretation is made.
* Decisions assessed: SQL-only delivery; limit 1..100; exclusive composite
  cursor and repeat sweeps; configured scanner with explicit synthetic opt-in;
  non-deleting worker mode; per-document CAS and audit recovery; deferred
  Defender activation, hosted schedules and human approval gates.
* Dependencies and acceptance: P01-T01 -> P01-T02 -> P02-T01 -> P02-T02,
  FR1-FR6, all non-functional requirements and AC1-AC6.
* Assessment can establish candidate credibility and identify source-grounded
  design gaps. It cannot establish implementation correctness, executed SQL/
  Docker results, real Defender assurance or operational authorization.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI and single critique/Review constraint; AC6 | Covered | Candidate preserves the original verdicts and prohibits an additional Review or unauthorized corrections after it. This artifact is the sole critique. |
| FR1; C1-C3; P01-T01/T02 | Partial | Composite keyset pages, missing/pending eligibility, SQL-only scope and limit are explicit. Continuation and incomplete exit interaction require PC-002. |
| FR2-FR3; C1,C7; AC2 | Covered | Touch through `_case`, per-document lock recheck, exact clean and non-deleting bad verdicts address the legacy helper's persistence/deletion hazards. Manual behavior stays separate. |
| FR4; C4-C6; AC3 | Partial | Prior-prefix recovery and committed-refresh separation are required, but the proposed snapshot-change detector is not a valid own-commit witness: PC-001. |
| FR5-FR6; C2,C3; AC1 | Partial | Safe counters, no private exception diagnostics, explicit data/store/scanner and local opt-in are sound. PC-002 resolves incomplete exits; PC-003 covers construction-time cleanup. |
| Attempt bound, fairness, retry and success-once requirements | Covered with corrections | Candidate requires at most the requested attempts, later pages despite persistent pending records, subsequent full sweeps, independent-connection races and no duplicate successful transition audit. PC-001/002 must be incorporated into those tests. |
| Existing availability, retention, hold, progress, resident and sensor behavior | Covered | Explicit preservation and relevant existing regressions are included; no authority expansion or new retention period is proposed. |
| C8; W1-W2; architecture/non-goals | Covered | A schedulable module rather than Azure timer/Defender activation meets the bounded task. Historical evidence is not treated as current execution. |
| P02-T01; AC1-AC4; test ownership | Covered with corrections | Core runner/recovery plus orchestrator CLI only, at most two new test files; semantic and existing regression coverage, real loopback SQL and real SQLite CLI are specified. Add PC-001/002/003 cases within those owners. |
| P02-T02; AC5; documentation | Covered | Actual changed job in the built orchestrator image supplements the startup-only checker; UID10001, read-only root, drop-all and NoNewPrivs are explicit. Existing synthesis/index/log and component guides are the correct documentation targets. |
| Validation prerequisites and evidence reporting | Covered | Installed distributions, existing tools, owned databases/container cleanup, actual commands and disclosed skips/failures are required. Missing mandatory SQL/CLI/image evidence must remain unmet acceptance, not be converted into a Pass. |

## Verdict

* Verdict: Revise
* Rationale: The narrow architecture and safety boundary are credible, but the
  concrete proposed committed-outcome detector can confuse another writer's
  successful change with this worker's rejected write and bypass prior-audit
  restoration. Two additional contract gaps affect truthful incomplete-run
  reporting and guaranteed connection cleanup. All three are direct planner
  corrections within confirmed user direction; no significant user decision
  or new research phase is needed.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* This is the original final-candidate verdict. Planner disposition and later
  implementation evidence must not rewrite it or trigger another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Snapshot change does not prove that this worker committed

* Related IDs: FR4, AC3, C4-C6, P01-T01, P02-T01.
* Evidence: P01-T01 in the phase details says to compare SQL snapshots to detect
  a save that committed before refresh failure, raise `CommittedOutcomeError`,
  and avoid the staff validation context.
  src/core/src/zava_forward/core/sqlstore.py:593-616 automatically invokes
  `_discard()` on `ConflictError` when controlled validation contexts are
  absent. Its `_discard` implementation at lines 640-671 clears failed pending
  audit and reloads persisted case snapshots; `_load_case` updates `_snap`.
  The comparable snapshot detector in
  src/core/src/zava_forward/core/change_provenance.py:86-137 runs under
  `change_validation`, unlike the proposed worker.
* Concern: Consider two independent connections loading pending snapshot A.
  The competing connection commits A1 while the worker scans A. The worker's
  CAS fails. Existing `save()` recovery loads A1 and changes `_snap`, even
  though the worker did not commit. Comparing the old and new snapshot now
  incorrectly classifies that conflict as the worker's committed outcome.
  Moreover, the automatic `_discard()` used no prior pending prefix; if the
  worker takes the committed branch before `_discard(prior)`, that prefix is
  not restored. Recovery can also fail after updating the snapshot, so the
  failed-recovery seam needs the same distinction.
* Impact: False committed reporting, incorrect reconciliation/retry advice
  and lost prior audit contradict FR4 and merged102 preservation. A test that
  merely checks final clean state or one success event can miss this defect,
  since the winner legitimately produced both.
* Smallest useful change: Specify an unambiguous own-operation commit witness
  or equally reliable transaction-outcome boundary, distinct from any snapshot
  refreshed by conflict recovery. Explicitly require restoration of the
  captured pending prefix on rejected CAS even when existing save recovery
  already ran or failed. Do not solve this by adopting staff authority or
  treating a fresh competitor snapshot as proof of own success.
* Action owner: Planning parent for P01-T01 and P02-T01; implementation owner
  subsequently implements the chosen bounded recovery mechanism.
* Exact resolving evidence: Revised details identify the witness and recovery
  ordering. Within the core-owned test file, an independent-connection test
  captures a prior pending audit, commits a competing case change during the
  worker scan, and proves the worker reports rejection/failure rather than
  own committed success, preserves the winning case and original conflict,
  retains the prior audit exactly once, and never flushes the failed rescan
  success event. Include recovery failure after competitor reload. Keep the
  separate real own-COMMIT/refresh-failure test proving one success event and
  truthful committed reconciliation.
* Decision route: Direct planner correction. Current user direction already
  requires these outcomes; no user response is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: An incomplete all-clean page has contradictory exit semantics

* Related IDs: FR1, FR5-FR6, AC1, P01-T01/T02, P02-T01/T02.
* Evidence: AC1 requires nonzero incomplete/error runs. FR1 permits continuation
  when more candidates exist, but FR6 and P01-T02 define exit 2 only for
  pending, exit 1 for failure/reconciliation and exit 0 for a settled page.
  No explicit rule covers a page whose attempted documents are all clean but
  whose `next_after` is non-null. P01-T01 also describes continuation as based
  on "attempted selection" while requiring skipped results after rechecks.
* Concern: The implementation can reasonably return 0 after cleaning the
  first bounded page despite outstanding candidates, violating AC1's
  incomplete-run requirement. The ambiguous attempted/selected distinction
  also leaves cursor advancement underspecified when another writer resolves
  or removes every selected document before its locked eligibility recheck.
* Impact: A caller that relies on exit status can mistake partial work for a
  completed sweep. A cursor tied only to actual scan calls can fail to advance
  across a page that races to skipped state, undermining fair completion.
* Smallest useful change: Define exit precedence explicitly: failure or
  committed reconciliation is 1; otherwise unresolved pending or non-null
  continuation is 2; otherwise 0. Define cursor advancement using the last
  selected/consumed key, including candidates skipped at recheck, with the
  existing "only when more candidates exist" rule. Document that pending
  earlier in a sweep requires a later cursor-free sweep even if its terminal
  page itself has no pending results.
* Action owner: Planning parent for FR1/FR6, AC1 and P01-T01/T02; implementation
  owner for the core/orchestrator tests and CLI guide.
* Exact resolving evidence: Aligned plan/details and exit documentation;
  core tests for an entirely skipped selected page with later candidates;
  actual offline CLI coverage where limit 1 cleans the first of multiple
  candidates, emits continuation and exits 2, followed by a terminal settled
  invocation exiting 0. Test failure/reconciliation precedence over pending
  and continuation. Keep all additions within the two owned test files.
* Decision route: Direct planner correction aligning an existing acceptance
  criterion, not a significant or divergent user decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: A finally block cannot close a store whose construction failed

* Related IDs: FR6, C3, P01-T02, P02-T01.
* Evidence: P01-T02 requires safe configuration failure and "Close db in
  finally." src/core/src/zava_forward/core/factory.py:9-25 returns a fully
  constructed store. src/core/src/zava_forward/core/sqlstore.py:141-171 opens
  the connection before schema/migration, document-store and scanner setup.
  src/core/src/zava_forward/core/documents.py:202-210 and
  src/core/src/zava_forward/core/doc_controls.py:97-104 can raise during that
  setup, after the database is open. MssqlStore reuses this construction path.
* Concern: If `open_store()` raises after opening the connection, the CLI has
  no returned store object for its ordinary finally block to close. Rejecting
  local mode without opt-in before creation addresses only one failure path;
  incomplete Blob settings, incompatible Defender storage and SQL setup
  failures remain relevant initialization paths.
* Impact: The promised guaranteed closure is not established, including on
  failure paths important to repeated one-shot execution and owned SQL
  cleanup. Constructor exception text can also bypass the intended safe CLI
  marker unless initialization is inside the error boundary.
* Smallest useful change: Specify ownership and cleanup for partially
  initialized stores/connections, with construction inside the sanitized CLI
  failure boundary. Prefer the smallest reusable close-on-construction-error
  guard in the existing construction path; preserve existing successful
  factory behavior and all explicit scanner/data preflight checks. Merely
  adding `if store is not None` to CLI finally is insufficient.
* Action owner: Planning parent for target/cleanup scope in P01-T02 and test
  obligations in P02-T01; implementation owner for the narrowly scoped guard.
* Exact resolving evidence: Revised details identify who owns the connection
  before `open_store()` returns. Tests inject an error after the actual SQL
  connection opens and before construction returns, assert closure without
  masking the original failure, and assert a nonzero safe CLI failure marker
  without paths, credentials or private supplied exception diagnostics.
  Include the successful command's closure check and preserve existing
  factory/configuration regressions.
* Decision route: Direct planner correction needed to meet FR6, with no user
  decision or authority expansion.

## Strengths and Residual Risk

* The plan correctly rejects a wrapper over unbounded `rescan_pending`, uses
  `_case` to register SQL changes, and preserves the existing scan service
  rather than inventing a second scanner stack.
* Non-deleting infected/mismatch handling is explicit. Availability remains
  exact-clean-only, generated documents are excluded, and no worker path is
  authorized to delete bytes, release holds or approve retention.
* SQL-only acceptance and actual independent connections are appropriate for
  success-once and CAS claims. JSON is not promoted into cross-process proof.
* Persistent pending results do not justify an unbounded in-page retry.
  Starting later sweeps without a cursor is explicitly required.
* Real loopback SQL, actual CLI and the actual changed job in the hardened
  image are specified separately from unit fakes and ordinary image startup.
  All remain future evidence, not completed checks.
* The maximum two new test files and no-removal/generated-target constraints
  are maintained. The listed regression areas preserve tightly coupled
  merged102 progress/provenance and resident/sensor guards without expanding
  the implementation into those workstreams.
* An attempt bound is not a latency or memory SLA; the research acknowledges
  that distinction. No additional performance target is inferred here.
* Real Defender activation, account/Blob verification, recurring hosted
  schedule ownership/cadence/monitoring and retention approvals remain
  explicitly deferred gates. Synthetic clean is not real antivirus assurance.

## Questions or Blocking Evidence Gaps

* None requiring a user answer. PC-001 is resolvable from the supplied current
  SQL transaction and recovery evidence. The planner must select and record
  the technical outcome witness rather than delegate it as an unresolved
  authority or product decision.
* Required actual SQL/CLI/image checks that cannot execute must be reported
  as unmet acceptance, with their concrete blockers. Documenting a skip does
  not satisfy the corresponding required criterion.

## Limitations

* This critique performed source inspection only. It did not implement the
  job, execute tests, provision SQL, build/run containers or contact cloud
  services. Proposed failure examples are source-grounded traces, not claimed
  runtime reproductions.
* The shell `rg` executable was unavailable; direct file reads and the
  provided search tool supplied the source evidence instead.
* No private dataset, other worktree or legacy implementation tree was read.
  No plan, details, research, state or original Review record was modified.
* The three findings are the complete actionable set identified within this
  supplied candidate boundary; cosmetic preferences and unrelated existing
  defects are not findings.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct P01-T01's own-commit detection and prefix
  restoration contract and add the discriminating race/recovery test
  obligation; reconcile PC-002 and PC-003 in the same direct revision.
* User response required: No.
* Preserve this Revise verdict. Record each PC disposition in the planning
  artifacts, finalize without another critique, then allow the active parent
  to proceed through the already authorized implementation and one original
  Review. This critique itself invokes neither stage.

## Next Steps

The active planning parent directly resolves PC-001 through PC-003, records
the exact dispositions and finalizes the plan without a second critique.
No user action is required.
