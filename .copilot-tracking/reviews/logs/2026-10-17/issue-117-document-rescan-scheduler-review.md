<!-- markdownlint-disable-file -->
# Review: Bounded pending-document rescans

## Scope and Evidence

Task ID117; date2026-10-17. One original full-task Review, not coordinator
acceptance. Authorized base ebc8dab87ae9bd6a33380b85e86f38be5ed9f213;
working branch feat/document-rescan-scheduler-117.
Research, plan, details, critique and changes use the same dated
issue-117-document-rescan-scheduler slug and canonical state pointers.

## Opening Review State

Goal: compare the bounded SQL job and preserved controls with the full ready
plan, exact issue boundary, one-critique dispositions and actual execution.
Plan P01/P02 and details complete; changes record reconciled with actual SQL,
CLI, image and regression results. Acceptance basis FR1-FR6/AC1-AC6 and user
controls; no operational Defender/retention approval inferred.
First comparison: core scan/page/COMMIT/recovery and orchestrator configuration
against critique PC-001..003, then tests/docs and follow-up boundaries.
Read-only source/artifact boundary: write only this one Review record.
No initial evidence blocker. Review execution active; outcome not yet assessed.

## Execution Status

* Execution status: Complete.
* Review execution evidence: One original full-task assessment on 2026-10-17.
  Compared the complete supplied research, ready plan, phase details, original
  critique and changes record with the current tracked diff and untracked
  issue-owned production/test files. Inspected supporting current SQL/store,
  factory, scanner, document-storage, audit and authority contracts.
* Outcome: Not accepted. Two Medium implementation defects remain in the
  promised safe failure/reporting boundary. Successful normal-path and
  transaction/recovery evidence does not resolve these defects.
* No coordinator Pass, operational acceptance, second Review or source
  correction is claimed. Implementation execution and this Review execution
  are complete; acceptance is not.

## Scope and Compared Artifacts

Canonical compared task set:

* .copilot-tracking/research/2026-10-17/issue-117-document-rescan-scheduler-research.md
* .copilot-tracking/plans/2026-10-17/issue-117-document-rescan-scheduler-plan.md
* .copilot-tracking/details/2026-10-17/issue-117-document-rescan-scheduler-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-17/issue-117-document-rescan-scheduler-plan-critique.md
* .copilot-tracking/changes/2026-10-17/issue-117-document-rescan-scheduler-changes.md

Candidate assessed, including untracked files:

* src/core/src/zava_forward/core/doc_controls.py
* src/core/src/zava_forward/core/sqlstore.py
* src/core/src/zava_forward/core/document_rescan.py
* src/orchestrator/src/zava_forward/orchestrator/document_rescan.py
* src/core/tests/test_document_rescan.py
* src/orchestrator/tests/test_document_rescan_job.py
* src/core/README.md
* src/orchestrator/README.md
* src/api/README.md
* docs/reference/research/retrofit-synthetic-data/README.md
* docs/reference/README.md
* docs/reference/log.md

Supporting evidence included docs/case_study_48_original.md,
docs/case_study_48_addendum.md, docs/reference/memory.md,
docs/reference/research/sector/housing-association-primer.md,
docs/adrs/0002-pilot-readiness-architecture.md decision 2,
docs/prds/zava-forward-retrofit-programme-demonstrator.md DH-003/PR-003,
src/core/src/zava_forward/core/store.py,
src/core/src/zava_forward/core/factory.py,
src/core/src/zava_forward/core/mssqlstore.py,
src/core/src/zava_forward/core/documents.py,
src/core/src/zava_forward/core/change_provenance.py and existing component
configuration. These establish the engineering and human-authority boundary;
no legal-currentness or real-service conclusion is drawn.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01; FR1-FR4 | Bounded core runner, non-deleting scan mode, own-COMMIT witness and prior-prefix recovery | Reconciled | Stable sorted composite selection; selected-key continuation; locked recheck; `_case` touching; real save; no worker deletion. Unsupported verdict strings fail explicitly. RV-002 identifies an unhandled malformed-result shape. |
| P01-T02; FR5-FR6 | Explicit configured SQL CLI, synthetic opt-in, counters/exits and constructor cleanup | Partial acceptance, completed implementation | Normal configuration and outcome paths align. RV-001/RV-002 contradict the unconditional sanitized-diagnostics/report promise. |
| P02-T01; AC1-AC4 | Two owned test files and component/regression receipts | Reconciled, with identified coverage gaps | Actual backend and command receipts support the exercised claims. Failure-recovery tests do not inspect all emitted diagnostic text; scanner tests cover unknown strings and selected exceptions, not non-iterable returns. |
| P02-T02; AC5 | Existing image checker, actual hardened job, matching installed hashes; component/KB docs | Reconciled | Actual receipts support the engineering claims. Documentation's safe-diagnostics promise remains stronger than implementation at RV-001/RV-002. |
| AC6; original critique and original Review | Original Revise retained with direct dispositions; no outcome presumed | Reconciled | This is the single original Review, with adverse result retained. No source changes or repeated review are performed here. |
| Follow-Up Items | Defender/Blob, hosted scheduling, DPO/Legal/owner approvals | Reconciled | All remain separate operational work, not missing active implementation tasks or forced defects. |

The plan/detail completion markers, changes completion/handoff, blockers and
validation state agree that implementation ran. Their statements that there
is no engineering blocker are implementation-stage statements, not evidence
that Review must accept the candidate. The research header still says
"In progress", but its cycle disposition, self-check and final Planning
Readiness explicitly say Complete; all Q1-Q3 are answered. This stale header
does not prevent a credible comparison or create a material research gap.

## Completed Work Assessment

| Marker | Completed work and evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Runner restricts limits to exact integers 1..100, excludes generated/resolved records, orders `(case_id, doc_id)`, rechecks under the SQL lock and advances skipped selections. `_scan_stored` performs its own `save()` inside `_attempt`, before context exit. | FR1/FR2 and bounded attempt contract supported. Full candidate collection is not bounded memory/latency; the plan explicitly does not claim such an SLA. |
| P01-T01 | `remove_bad=False` retains infected/mismatch records and bytes; exact-clean read guard remains unchanged. No retention approval, deletion or hold-release call is introduced. | FR3/AC2 safety and authority boundary supported for exercised outcomes. Malformed result remains unavailable in the Review repro, but lacks the required controlled failure report: RV-002. |
| P01-T01 | `SqlStore.save()` invokes the thread-local rescan witness immediately after successful COMMIT, before other post-commit hooks. `_attempt` restores prior pending audit on rejected attempts, quarantines failed success audit before recovery, and separates own committed reconciliation. | FR4/PC-001 substance supported by current source and actual SQL receipts. A competitor's refreshed snapshot is not treated as own commit. Raw nested recovery logging remains RV-001, not an own-commit classification defect. |
| P01-T02 | CLI preflight requires explicit data/store/scanner, refuses JSON and implicit local use, supports composite cursor, gives failures/reconciliation precedence over pending/continuation, closes a returned connection. Constructor guard closes an opened connection on initialization failure without replacing the original exception. | PC-002/PC-003 implemented for tested paths. Safe diagnostics and malformed per-document report coverage remain incomplete. |
| P02-T01 | Seventeen core semantic methods shared by SQLite/MSSQL, six orchestrator methods; no test removals or third new test file. Existing progress/provenance, resident, sensor, store/recovery and API selections recorded. | Receipts support the executed scope. Not all exception paths are proven by passing tests; the two Review repros distinguish remaining defects. |
| P02-T02 | Related READMEs, existing synthesis/index and append-only log describe offline mechanism, cursor-free sweeps and operational gates. Image receipt matches all four candidate source hashes. | Appropriate scope and placement. No public web change, new resource, paid-service activation or authority expansion. No broader issue closure is justified. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Trigger and decision basis | Reconciliation and assessment |
| --- | --- | --- | --- |
| FR4; P01-T01; P02-T01 | Explicit own-operation COMMIT witness replaces snapshot inference; prior prefix restored even after automatic recovery | PC-001, compatible with confirmed transaction/audit requirements | Current plan, details, source, tests and changes agree. No significant user decision or expanded worker authority was needed. |
| FR1/FR6; P01-T01/T02 | Incomplete continuation exits 2; all-skipped selected page advances cursor | PC-002, resolves existing AC1/FR1 contract | Reconciled across plan/details, tests and CLI documentation. Later sweep starts without cursor; terminal exit 0 does not certify earlier pending pages. |
| FR6; P01-T02 | Reusable partial-construction cleanup guard and sanitized factory boundary | PC-003, meets existing ownership requirement | Reconciled and exercised with a real opened SQLite connection followed by setup failure. No extra lifecycle authority. |
| P01-T01 compatibility refinement | Unknown verdict raises RuntimeError rather than ValueError | Legacy helper interprets ValueError as removal; preserving it avoids a false removed result | Changes and detail completion evidence record the rationale and regression assertion. This is an in-scope compatibility refinement, not a divergent decision requiring replanning. It does not cover malformed result shape: RV-002. |

## Critique and Material Revision Assessment

* Original critique execution Complete; original verdict Revise, one High and
  two Medium findings. It remains unchanged.
* PC-001: Applied and substantively resolved for transaction outcome,
  competitor conflict, failed recovery and prior-prefix preservation.
  Current code marks only the active thread-local own operation after COMMIT.
  Both actual MSSQL inherited tests and source distinguish real own commit
  from competitor refresh. RV-001 is a separate diagnostics gap on that
  recovery path, not a rewritten PC-001 verdict.
* PC-002: Applied and resolved. Continuation uses the last selected key,
  including an entirely skipped page. Actual CLI returns incomplete exit 2
  for an all-clean nonterminal page; failure/committed exit 1 takes precedence.
* PC-003: Applied and resolved for connection ownership during construction.
  `SqlStore.__init__` owns cleanup until the factory returns; then CLI owns it.
  The real-open/setup-failure test preserves the original exception and
  confirms closure.
* No significant or divergent decision gap or invalid plan assumption was
  found. The supplied ready artifacts incorporate the direct dispositions;
  changes identify them as pre-implementation corrections. Chronological
  claims beyond supplied artifacts were not independently reconstructed.
  Nothing inspected establishes premature dependent-work resumption.
* No second critique, fresh plan revision or second Review is required by
  this record. Later implementation is routed separately.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Defender account enablement and real Blob verification | No account activation, real scanner assurance or live-data authorization in this task | Service/security owner obtains explicit authorization and verifies the actual account/Blob tag path | Open distinct operational follow-up; not RV defect, not an active P01/P02 task |
| Hosted schedule ownership, cadence and monitoring | A one-shot schedulable mechanism was requested, not a deployed recurring timer | Delivery/operations owner defines cadence, continuation/sweep handling, failure reconciliation and missing-run monitoring under separate authorization | Open distinct scheduling follow-up; no Azure resource activation inferred |
| DPO/Legal periods, holds and owner approvals | Rescan worker has no deletion, hold-release or approval authority; engineering tests cannot approve policy | DPO/Legal and record owner approve periods/triggers/delegations and case-specific controls | Open distinct human-governance follow-up; retention listing never becomes automatic deletion |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Nested SQL recovery logs bypass the worker's safe-diagnostics boundary

* Related scope: FR4-FR6; P01-T01/P01-T02; P02-T01.
* Evidence: src/core/src/zava_forward/core/document_rescan.py:48-53 and
  100-112 use fixed worker markers, but
  src/core/src/zava_forward/core/sqlstore.py:614-631 still performs its own
  conflict `_discard()` and calls `logging.exception` on recovery failure.
  An active `document_rescan` context is not among the contexts suppressing
  that automatic recovery. The traceback is already emitted before the
  outer worker catches the conflict. The worker README promises no private
  transport/exception diagnostics.
* Discriminating Review repro: actual in-memory SQLite store seeded only from
  a deep copy of the existing small DATA fixture, one pending document,
  patched local byte retrieval. During the scanner call increment the SQL
  case rowversion directly, return clean, and wrap `_discard` so it performs
  normal recovery then raises
  `OSError("SYN_PRIVATE_SQL_RECOVERY_DIAGNOSTIC")`. Invoke the actual CLI
  `main(["--synthetic-local", "--limit", "1"])` with explicit synthetic
  configuration and capture the root logging stream in memory.
  Result: exit 1 and truthful failed=1/clean=0/committed=0, but captured logs
  contain both a traceback and the exact private sentinel. No filesystem,
  network, external SQL or container was needed.
* Existing coverage gap:
  src/core/tests/test_document_rescan.py:290-313 exercises essentially this
  conflict/recovery failure and captures root ERROR logs, but asserts only
  counters and persisted state, not redaction of all emitted diagnostics.
* Impact: The new worker's stated sanitized logging contract fails on an
  explicitly supported recovery seam. Real driver/recovery diagnostic text
  can reach scheduler logs, despite fixed outer markers. This does not
  establish actual credential disclosure, false availability, audit
  corruption or a wrong committed outcome.
* Destination: later `rpi-implement`.
* Smallest useful next action: Make automatic SQL conflict recovery/logging
  respect the worker-owned recovery boundary, or equivalently sanitize this
  nested worker path before any traceback is emitted. Preserve existing
  non-worker recovery and merged102 behavior. Extend the existing owned
  recovery test to assert no sentinel/traceback in the entire CLI logging
  stream while preserving prior prefix, original conflict and winner state.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: A malformed scanner result escapes both controlled failure boundaries

* Related scope: FR3/FR5/FR6; P01-T01/P01-T02; P02-T01.
* Evidence: src/core/src/zava_forward/core/doc_controls.py:163 unpacks the
  scanner return before validating its verdict. A non-iterable result such
  as None raises TypeError. The runner catch at
  src/core/src/zava_forward/core/document_rescan.py:100-108 does not include
  TypeError, and the CLI boundary at
  src/orchestrator/src/zava_forward/orchestrator/document_rescan.py:52-56
  does not include it either.
* Discriminating Review repro: actual in-memory SQLite fixture as above,
  patched local byte retrieval and scanner `return_value=None`; call
  `run(store, limit=1)`. TypeError escapes with
  `cannot unpack non-iterable NoneType object` instead of returning a report.
  A fresh locked read confirms persisted status pending and zero
  `document_rescanned` success events. In a separate actual CLI invocation,
  scanner `TypeError("SYN_PRIVATE_SCANNER_DIAGNOSTIC")` likewise escapes
  `main`, confirming the CLI has no final sanitizer for this error class.
* Existing coverage gap: the owned core unknown/outage test covers an
  unsupported verdict string, DocumentStoreError, OSError and RuntimeError;
  none covers a malformed non-iterable scanner return. The fixed unknown
  RuntimeError refinement therefore does not establish malformed-result
  reporting.
* Impact: A malformed result aborts the page without the required failed
  counter/JSON report and prevents later selected documents being consumed.
  Direct module execution exposes a Python traceback; an originating
  TypeError diagnostic can escape unchanged. Fail-closed persistence remains
  intact in the repro: this is not a false-clean or deletion defect.
* Destination: later `rpi-implement`.
* Smallest useful next action: Validate/normalize malformed scanner result
  shapes into a safe worker-recognized error before mutation, and keep a
  sanitized CLI boundary for the relevant error class. Retain RuntimeError
  rather than legacy removal-signalling ValueError for unsupported results.
  Add cases within the existing two owned test files proving malformed
  returns produce failed=1/clean=0, safe nonzero CLI output, no private
  diagnostic, unchanged pending state/audit and bounded continuation of the
  remaining selected documents.

## Defects and Routed Findings

Severity summary: 0 Critical, 0 High, 2 Medium, 0 Low.
The two findings have distinct emitting/handling boundaries; neither changes
the accepted scheduler direction or requires new research.

| Finding | Destination | Owner and smallest next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Later rpi-implement | Implementation owner contains nested worker SQL recovery diagnostics and extends existing recovery assertions | Implementation violates FR5's fixed-diagnostic contract on a supported failure seam |
| RV-002 | Later rpi-implement | Implementation owner normalizes malformed scan results and verifies per-document/CLI containment | Implementation omits a malformed-result report/error boundary |

Later implementation of these findings does not require another Review.
No fixes are made by this Review and no source-correction loop is started.

## Validation Evidence

Parent receipts were assessed as prior actual execution, not re-executed or
claimed as independent Review runs. The cited session stdout tails were
read directly; source hashes were independently recomputed in this Review.

| Command or evidence | Scope | Status and limits |
| --- | --- | --- |
| Configured core Ruff, format and mypy | Existing component configuration | Parent-reported pass: 67 formatted files and 120 mypy source files. Not rerun merely to duplicate the receipt. |
| Configured orchestrator Ruff, format and mypy | Existing component configuration | Parent-reported pass: 9 formatted files and 12 mypy source files. Not rerun. |
| Orchestrator unittest discovery | Complete orchestrator selection | Parent-reported 28 passed, no skips; source includes real SQLite subprocess CLI and connection ownership tests. |
| Combined core semantic/progress/provenance/stock/resident/sensor selection | Existing regression controls plus new worker | Parent-reported 277 run, 201 passed, 76 explicit backend/opt-in skips; disclosed sensor ResourceWarnings. Not a full repository suite or live-service acceptance. |
| API document/documents/progress selection | Existing API behavior | Actual session api117-tests.log: 57 run, 45 passed, 12 skips. |
| Store/read/queue/recovery selection | Shared SQL writer regressions | Actual session sqlstore117-regressions.log agrees with reported pass and constructed 60,000-case timing fixtures; changes records 57 passed, no skips. |
| Final document worker/API controls selection | Final source document paths | Actual session final117-doc-tests.log: 48 run, 31 passed, 17 opt-in skips. |
| Actual MSSQL worker class | Seventeen shared semantic tests, independent owned loopback connections | Actual session sql117-tests.log: 17 passed in 101.643s, separately covering the 17 final selection skips. Backend skips in other suites are not relabelled as executed. |
| Actual MSSQL module pages | Persisted command and sweep behavior | Actual session sql117-cli.log: exits 2/0/0 and clean 1/2/0. Changes/harness evidence reports three success events, intact ledger/hold/bytes, exact owned container stopped and removed. No restart or activation during Review. |
| Existing container checker and actual hardened module | Built installed candidate, not startup alone | Actual session image117-run.log: checker/negative probes/startup pass; actual pages 2/0/0 and 1/2/0 clean; intact ledger/hold/bytes. Parent identifies image sha256:26fa4bf5152291ba9f8f9ae9657ce20c79cc73fab79d993d2bd67d5fa6b4f9fd, UID10001, read-only, drop-all, NoNewPrivs and no network. No image build/run during Review. |
| sha256sum of the four production modules | Final candidate identity | Review-executed pass: all four match the final installed-image hashes in changes and image receipt. |
| In-memory SQL CAS plus failed recovery, through CLI | Discriminating untested diagnostic assertion | Review-executed defect reproduced: truthful exit/report but private sentinel and traceback leaked, RV-001. |
| In-memory malformed return and TypeError CLI seam | Discriminating malformed/error boundary | Review-executed defect reproduced: TypeError escaped, pending preserved and success events zero, RV-002. |
| git diff --check | Candidate whitespace | Review-executed pass. |
| Defender/live Blob/cloud/browser/human operational checks | Outside authorized engineering boundary | Not run; no account activation, paid service, hosted timer, current legal verification or operational approval authorized. Web/browser checks inapplicable because no web files changed. |

Session evidence location supplied by the parent:
/home/azureuser/.copilot/session-state/ba90bb56-8dbf-4c5f-8825-92041810af80/files/
with sql117-tests.log, sql117-cli.log, image117-run.log, api117-tests.log,
sqlstore117-regressions.log and final117-doc-tests.log. These are supporting
receipts, not additional Review records. No private dataset, mvp tree, other
worktree, SQL restart, cloud service or container activation was used.
Review repros used SQLite `:memory:`, mocked seed reads and local synthetic
byte responses; no fixture/scratch files or new test files were written.

## Residual Work

The three operational follow-ups in Plan Follow-Up Assessment remain outside
active acceptance. In particular, issue #117's wider operational obligations
are not completed by an offline engineering scheduler. No additional residual
engineering task, design decision gap or material research gap was identified
within this complete supplied boundary.

## Blockers and Remaining Work

* Review blockers: None; the evidence set is sufficient and assessment is
  complete.
* Remaining active implementation markers: None. Completed markers mean
  implementation execution, not defect-free acceptance.
* Acceptance blockers: RV-001 and RV-002 remain unresolved and are routed to
  later implementation, not corrected here.
* Publication and independent coordinator/owner continuation belong to the
  active parent. This record neither commits/pushes nor awards acceptance.

## Outcome

* Outcome: Not accepted.
* Rationale: The bounded scheduling direction, fair paging, explicit
  configuration, exact-clean/non-deleting safety, transaction outcome witness,
  prior-prefix recovery and exercised regression/image behavior are supported.
  Two reproduced Medium defects materially contradict the explicit safe
  failure/reporting contract. Passing normal-path and SQL state assertions
  cannot establish acceptance while these diagnostic/report gaps remain.
* Preservation: No finding alleges false clean, deletion, hold release,
  impersonated staff approval, lost winner state or failed-prefix corruption
  in the observed candidate. No original critique verdict is rewritten.
* Review writes: Only this existing canonical record was updated. No plan,
  details, research, critique, changes, state, source or test correction;
  no nested agent and no other Review record.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement | RV-001 and RV-002; parent retains adverse original Review and decides separately authorized implementation continuation |
| Decision gap or invalid assumption | None | No significant or divergent decision needing rpi-plan |
| Material evidence gap | None | No rpi-research handoff needed for this supplied engineering boundary |
| Non-blocking residual work | Three distinct operational follow-ups | Service/security owner for Defender/Blob; operations/delivery owner for recurring scheduling; DPO/Legal/record owner for policy and approvals |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: Prior actual component, core/API/regression, 17-test
  MSSQL, real CLI and installed hardened-image receipts assessed; matching
  candidate hashes and two in-memory failure repros independently executed.
* Blockers: No Review blocker; two unresolved Medium acceptance defects.
* Parent continuation: Return this single original Review result. Any later
  correction is separate rpi-implement work, not a new Review or self-awarded
  coordinator Pass.
