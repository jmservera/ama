---
title: Finance match controls 94 review
ms.date: 2026-10-17
---

## Opening Review State

Task #94, finance-match-controls-94; parent #93 hierarchy, no dependencies.
Scope: complete implementation, exact three issue criteria and plan PC-001/002
dispositions, including current permissions, persistence and identity evidence.
Evidence Ready: dated research, plan/details, one critique, changes and actual
focused test results. First comparison: criteria to production/test behavior.
Read-only source boundary; only this canonical record may be edited by reviewer.
Review execution: In progress. Outcome: not yet assessed.
P02-T02 remains pending for this Review and parent-owned delivery, not missing code.
No initial blocker known. No second full Review planned.

## Scope and Evidence

* Task: #94, finance-match-controls-94; review date 2026-10-17.
* Branch: feat/finance-match-controls-94; compared base: bab4bf3.
* Review scope: one complete independent post-implementation Review, including
  the working-tree diff and both new finance-owned test files.
* Acceptance authority: exact issue criteria supplied by the parent: nothing
  paid by the product, line-level match exceptions, preparer cannot approve.
  The accepted plan additionally requires ordinary-error JSON recovery,
  transactional SQL authority/independence, stale-write rejection, and
  preservation of approved budgets, commitments and held dispositions.
* Compared artifacts:
  .copilot-tracking/research/2026-10-17/finance-match-controls-94-research.md;
  .copilot-tracking/plans/2026-10-17/finance-match-controls-94-plan.md;
  .copilot-tracking/details/2026-10-17/finance-match-controls-94-phase-details.md;
  .copilot-tracking/reviews/plans/2026-10-17/finance-match-controls-94-plan-critique.md;
  .copilot-tracking/changes/2026-10-17/finance-match-controls-94-changes.md.
* Source evidence: complete finance.py and changed SQL save hook; new
  test_finance_match_controls.py and test_finance_match_api.py; existing
  finance/signoff fixture and changed tests; Store save/audit, SQL lock,
  save/discard and rowversions; change_provenance actor/transaction prior art;
  controls, SQL Server transaction adapter and HTTP finance dispatch.
* Documentation: complete changed component/Finance-journey sections,
  append-only log delta, reference-index delta, original case study, relevant
  addendum/index/memory sections and PRD FR-018/AC-021/AC-042.
* Current BRD FR-018/RULE-003 numbering is explicitly documented as stale in
  the issue: those current requirements concern handoff/hazard ownership.
  This Review does not relabel them or claim complete PRD acceptance.
* Source and task artifacts remained read-only. No delegation, delivery,
  cloud/AI/browser/private-data/payment operation or source fix occurred.

## Execution Status

* Execution status: Complete.
* All supplied task artifacts, changed production/configuration/documentation
  boundaries, new tests and relevant persistence/identity prior art were
  compared. A bounded in-memory reproduction confirmed RV-001.
* Complete describes Review execution, not acceptable implementation outcome.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Baseline 29 and failing-first 22 cases; 18 failures/5 errors, including subtests | Reconciled | Supplied chronology and checked regression ownership agree; the final JSON test does not reproduce persistent lower-level failure, RV-001 |
| P01-T02 | Finance-private line/identity/current-match changes and SQL validator hook | Reconciled with defect | Production targets match plan; JSON recovery guarantee remains incomplete |
| P02-T01 | Focused persistence/HTTP, SQL/role, local SQL Server, tools and documentation | Reconciled with defect | Reported passes remain evidence for their tested failure model; broad ordinary-error recovery claims overstate RV-001 |
| P02-T02 | Independent Review and parent-owned delivery deliberately pending | Reconciled | No missing production implementation inferred from this lifecycle marker; delivery must wait for the blocker correction |
| Follow-Up Items | Broader contract/allocation/accepted-evidence authority outside exact criteria | Reconciled | Acceptance limitation, not an incomplete active task or invented dependency |

## Completed Work Assessment

| Related marker | Files | Assessment and evidence |
| --- | --- | --- |
| P01-T01/T02: record-only | src/core/src/zava_forward/core/finance.py; src/api/tests/test_finance_match_api.py; src/core/tests/test_finance_match_controls.py | Closed action set mutates records only. Payment-status actions do not call an execution adapter or alter budget/commitment/grant cash. Tests compare retained ledgers through reopen, not just labels |
| P01-T01/T02: line exceptions | src/core/src/zava_forward/core/finance.py; src/core/tests/test_finance_signoffs.py; new core/API tests | Aggregate exceptions expand onto actual zero-based lines. Missing budget/commitment/milestone and ambiguous commitment block clean match; duplicate and over-commitment tests retain line-level assertions |
| P01-T01/T02: actual independence | src/core/src/zava_forward/core/finance.py; src/core/src/zava_forward/core/change_provenance.py; new core/API tests | Registered actor equality includes email/code/name/role/OID. Independence compares populated email/code/OID against preparer snapshots; unresolved legacy preparer refuses. Same-role distinct staff can approve; same staff, shared-code alternate email/OID, and shared-OID alternate staff/email cannot |
| P01-T02/P02-T01: current acceptance | finance.py; sqlstore.py; new core tests | Acceptance recomputes matching. SQL rowversion failure reloads case and removes pending audit. Two-store and barrier-synchronized acceptance tests cover conflicting writers; fresh role/OID checks query staff rather than cache |
| P01-T02/P02-T01: JSON recovery | finance.py; Store.save/audit; JsonFinanceChecks | Only partially established. Instance-method injection passes, but the recovery calls the same failing persistence primitive before removing success audit; reproduced RV-001 |
| P02-T01: preservation | new core/API tests | Held acceptance/status refusals retain hold and Keep on hold through reopen. Independent release/disposition and external-status notes retain budget/commitment/grant records |
| P02-T01: configuration/scope | src/core/pyproject.toml; src/api/pyproject.toml; changed guides/index/log | Scoped typed-harness overrides follow existing untyped-boundary settings; no new ignore_errors/dependency. Exactly two new tests, directly coupled existing assertions, no Store/server/web/signoff production edit |

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Update and reason | Evidence and decision | Reconciliation and assessment |
| --- | --- | --- | --- |
| P01-T01/P02-T01 | Explicit ordinary JSON recovery and ledger/held invariants | PC-001/PC-002; compatible accepted intent, no new human decision | Plan/details/changes reconciled; PC-002 implemented, PC-001 incomplete in production, RV-001 |
| P01-T02; test ownership | Duplicate acceptance now refuses until duplicate independently rejected | Current-input recheck intentionally invalidates earlier Matched label | Current plan names this directly coupled regression; test is strengthened rather than weakened |
| P02-T01; typed harnesses | Add narrowly named test modules/shared fixture to existing mypy scopes | Existing untyped migration boundary prior art | Reflected in plan/details/changes; no broad strictness reduction |
| P02-T01; SQL Server harness | Disconnect/drop only each owned UUID database | Initial pooled-connection cleanup failures, followed by reported 14-case pass | Cleanup remains isolated and test-owned; failure is disclosed, not counted as a pass |
| Shared production boundary | Two-line finance validator import/call in SqlStore.save | Need current staff/independence inside writer transaction | Disclosed possible #90 overlap; #84 untouched. Neither hierarchy #93 nor concurrent vocabulary creates dependencies |

## Critique and Material Revision Assessment

* One completed final-candidate critique returned Revise, with PC-001 High and
  PC-002 Medium. Both received explicit direct plan/detail dispositions before
  implementation; no new critique is requested.
* PC-002 is substantively resolved by core and HTTP ledger-invariance and
  persisted hold/disposition tests, together with the inspected closed action set.
* PC-001 is not completely resolved: the tested instance-save exception is
  bypassed by Store.save during restoration, but real persistent write failure
  also affects Store.save. The resulting success audit remains. RV-001 is the
  single implementation defect, not a request for new planning.
* No significant divergent engineering decision or unaccepted authority,
  currency, payment, dependency or scope model was introduced.
* No evidence of dependent implementation resuming before the recorded
  compatible critique dispositions. Material revision planning is not needed
  to correct the accepted recovery contract.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Broader PRD contract/home allocation and accepted-evidence authority | The exact issue is narrower than complete AC-021/AC-042 and cannot establish real delegation or accepted milestone authority | Parent/backlog owner retains the broader PRD acceptance boundary; select distinct work if pursuing it | Limitation retained, not a defect, active completion item, or prerequisite inferred for #94 |
| Real platform, human, browser/accessibility and operational acceptance | Backend synthetic local verification does not establish these | Existing acceptance owners if that work is separately selected | No new acceptance claim or active work added |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: A persistent JSON save failure leaves a durable success audit for the refused approval

* Related scope: P01-T01/P01-T02/P02-T01, plan NFR ordinary JSON recovery and
  AC5; unresolved implementation portion of PC-001.
* Evidence: src/core/src/zava_forward/core/finance.py:128-145 appends the
  success audit before save. On any save error, it restores the in-memory
  case, then calls Store.save(self) before reaching audit truncation and
  last_hash restoration. src/core/src/zava_forward/core/store.py:101-112
  shows that original save and recovery both use open/json.dump/os.replace,
  while audit has already durably appended its event.
* Focused reproduction: executed the real finance_action, Store.save and
  Store.audit against an entirely in-memory mocked filesystem, with
  os.replace consistently raising PermissionError. Independent budget
  approval refused; both in-memory and reopened budgets remained Proposed;
  os.replace was attempted twice; durable audit still contained
  finance_budget_approve; last_hash was not restored.
* The existing test at
  src/core/tests/test_finance_match_controls.py:215-242 injects failure on the
  instance save method. Recovery deliberately bypasses that mock by invoking
  Store.save directly, so its passing assertions do not cover persistent
  primitive-level I/O failures such as a nonreplaceable live file. This is a
  caught ordinary exception, not an excluded abrupt process/filesystem crash.
* Impact: a refused operation can falsely attest that an independent approval
  succeeded. The ledger remains internally hash-consistent but contradicts
  the durable finance state; the documented PC-001 guarantee and P02
  completion evidence are therefore not met.
* Destination: rpi-implement, owned by the active coordinator within the
  existing correction budget. This is a delivery blocker, not future-only work.
* Smallest useful next action: add a persistent primitive-level save-failure
  regression in the existing finance test file and make audit-tail/head
  recovery independent of a second successful state save. Preserve truthful
  handling when restoration itself cannot persist; do not hide an unknown
  durable outcome or weaken the ordinary-error contract. Keep production
  correction in finance.py, update the directly related recovery claims and
  changes evidence, and run bounded JSON recovery plus SQL/HTTP regression
  as appropriate. Do not expand Store/schema/payment scope.

## Defects

* RV-001 is the complete actionable defect set for this Review: High, blocking,
  destination rpi-implement. No additional material defect was substantiated.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent coordinator: bounded finance recovery correction and objective primitive-level regression | Implementation violates an already accepted ordinary-error/audit guarantee |

Later implementation of this finding does not require another Review.

## Residual Work

* No additional non-blocking implementation work identified within the exact
  issue. The plan's broader acceptance limitations remain distinct from RV-001.
* No decision gap to rpi-plan or material evidence gap to rpi-research.

## Blockers and Remaining Work

* Blocker: RV-001 must be corrected and objectively validated before delivery.
* Remaining lifecycle work: parent completes P02-T02 reconciliation,
  authenticated privacy-safe commit, push and PR only after correction.
  This Review does not perform delivery or mark those actions complete.

## Validation Evidence

| Check | Status | Evidence and limits |
| --- | --- | --- |
| Independent primitive-level JSON save-failure reproduction | Executed; defect reproduced | Real finance/Store methods, in-memory mocked filesystem, persistent os.replace PermissionError; no source/scratch/private files written; durable false success and unrestored audit head confirmed |
| Baseline existing finance/signoffs, 29 | Supplied passed | Changes/phase details report pre-edit baseline; not rerun by reviewer |
| Failing-first 22, 18 failures/5 errors | Supplied expected failure | Changes/details distinguish subtest cascades; not a final pass claim |
| Focused JSON/SQLite/existing finance/authenticated HTTP, 54 | Supplied passed | Test implementations inspected; does not cover persistent primitive failure in RV-001 |
| Existing SQL/role/endpoint inventory, 47 | Supplied passed | Shared hook regression evidence; no repeat suite needed |
| Isolated local SQL Server, 14 | Supplied passed after cleanup correction | Inherited SQL transaction/rowversion path and owned-database cleanup inspected; initial 14 cleanup errors remain disclosed; no reviewer server/cloud run |
| Final new JSON/SQLite/HTTP, 25 | Supplied passed | Changes Pre-Review reconciliation; broader failure-model limitation remains |
| Ruff/format/configured mypy 3+1 files; diff/link/log checks | Supplied passed | Scope/configuration and documentation diff inspected; not universal strict typing or runtime acceptance |
| Reviewer git diff --check | Passed | Finding anchors checked; no whitespace errors reported; no source edits made |
| Browser, cloud, real tenant, AI, private dataset or payment execution | Not run | Backend-only synthetic scope; neither needed nor claimed for this review boundary |

## Outcome

* Outcome: Not accepted.
* Exact criterion assessment: inspected record-only paths satisfy the no-product-
  payment boundary; exceptions are actual line-level records; registered
  email/code/OID comparisons and same-role positive/alias-negative tests support
  actual preparer independence rather than role-only denial.
* These strengths do not waive RV-001. The accepted ordinary-error state/audit
  requirement is materially unmet, so a Conformant verdict or delivery-ready
  claim would be incorrect.
* Full PRD AC-021/AC-042, actual milestone authority, legal/funding approval,
  human adoption and live-platform/browser acceptance remain unestablished.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Parent coordinator corrects RV-001 within at most two allowed correction batches and records targeted evidence |
| Decision gap or invalid assumption | None | No accepted-direction change needed |
| Material evidence gap | None | Reproduction supports a concrete implementation defect |
| Non-blocking residual work | Distinct broader PRD acceptance boundary | Parent/backlog owner, only if separately selected |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: full supplied boundary inspected; one bounded independent
  reproduction; prior executed suites/tools explicitly identified as supplied.
* Blockers: RV-001. No second full Review or new plan critique requested.
