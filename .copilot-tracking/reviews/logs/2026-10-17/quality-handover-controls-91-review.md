<!-- markdownlint-disable-file -->
# Review: Quality and handover controls #91

## Scope and Evidence

* Task ID: issue91 / quality-handover-controls-91
* Review date: 2026-10-17
* Review scope: One independent post-implementation review of the whole current uncommitted diff against b5d4c840.
* Plan: .copilot-tracking/plans/2026-10-17/quality-handover-controls-91-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/quality-handover-controls-91-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-17/quality-handover-controls-91-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/quality-handover-controls-91-changes.md
* Research: .copilot-tracking/research/2026-10-17/quality-handover-controls-91-research.md

## Opening Review State

* Interpreted review goal: Assess implementation against exact issue criteria and reconcile the complete supplied RPI artifact set without implementation.
* Review scope: Whole supplied diff, including identity/rollback, repeat and legacy independence, same-measure supersession, fresh resident/handover checks, financial-state invariance, and #84/#94/#90 guards.
* Evidence readiness: All supplied artifact paths are available; implementation reports combined tests, isolated SQL, Chromium and configured static checks. Their claims remain to be compared with source and receipts.
* Acceptance basis: Contractors submit evidence only, never acceptance, defect closure or payment; remediation requires independent reverification; replacing accepted evidence invalidates dependent handover. Existing staff assistance and default-denied contractor writes remain intentional.
* First comparison boundary: Plan/detail/critique/change reconciliation followed by complete changed-source review and smallest local in-memory probes where needed.
* Active read-only boundaries: Only this canonical review record may be written. No fixes, additional review passes, delegation, other worktrees, private datasets, Azure, paid AI, IAM or live orders. Parallel #95 feature files remain unchanged.
* Initial blockers: None established.

## Execution Status

* Execution status: Complete.
* Review execution evidence: One continuous independent comparison on 2026-10-17 of all five supplied artifacts, all ten changed tracked files, applicable unchanged helpers and supplied validation receipts. No implementation or delegated agent was used.
* Reviewed branch: fix/quality-handover-controls-91, base b5d4c840.
* Reviewed tracked diff SHA-256: c1a44e0501dad8a72cf975c54f96a9a7ddb8f96ce2893fd5d35c693ee2f30b19, obtained with git diff b5d4c840 | sha256sum. This identifies the implementation diff, not the separately read untracked RPI artifacts.
* This is the original completed Review. Later authorized corrections must retain this verdict and findings and record their execution/closure evidence separately; no second Review is requested.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 / A1 | Current registered actor; contractor denial; separate finance | Reconciled | All seven quality writes enter the current-actor scope. Authenticated HTTP authority and default-denied contractor writes are unchanged. No payment capability was introduced. |
| P01 / P01-T01 / A2 | Retained identity aliases, repeated remediation and legacy contributors | Partial | New-record histories and populated name/email/code/OID aliases are covered. RV-001 identifies a known legacy earlier recorder omitted from resolution. |
| P01 / P01-T01 / A2 | Nonempty remediation and Fixed-only reinspection | Reconciled | Blank evidence and legacy Fixed records without remediation refuse. Independent acceptance remains separate from provider correction. |
| P01 / P01-T01 / A3 | Retire every active same-measure predecessor | Reconciled | Accepted/HANDED, multiple legacy HANDED and mixed HANDED/Accepted predecessors are retired. Evidence/history/aftercare remain historical; other measures and financial fields remain unchanged. |
| P01 / P01-T01 / non-functional recovery | JSON preimage/ledger restoration; SQL quarantine and legitimate prefix preservation | Partial | Covered pre-commit failures pass. RV-002 identifies a post-commit refresh exception that requeues an already committed prefix and reports a plain failure despite committed acceptance. |
| P02 / P02-T01 | Minimal ops.js feedback, replacement confirmation/history, core/API guides and KB continuation | Reconciled | Changed-file source review and supplied Chromium journey support the bounded behavior. Existing form/navigation gaps remain explicit external follow-up, not complete accessibility acceptance. |
| P03 / P03-T01 / A4 | Combined 357, actual SQL Server 36, actual Chromium, configured checks | Reconciled as execution evidence | Receipts substantiate the reported runs and limitations. They do not cover RV-001 or RV-002. The reviewer independently executed seven canonical methods using in-memory SQLite adaptations and the two focused defect probes, not SQL Server or Chromium. |
| Follow-Up Items | Competent-human/Azure acceptance and untouched web gaps | Reconciled as distinct work | Kept outside active implementation completion; explicit next owners/actions are recorded below. |

The phase checklist, detail phase index, changes summary and implementation
handoff all consistently mark P01-P03 complete and Review next. These markers
describe executed work, not proof that no defects remain. No missing artifact
or stale marker prevented comparison. No active implementation blocker was
reported; this Review supplies the concrete residual defects.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/quality.py | Current staff checks; identity snapshots/legacy resolution; remediation; strict indices; supersession; JSON/SQL recovery | Complete production diff and existing actor/transaction/persistence trace | Five canonical in-memory SQLite methods pass; two additional canonical methods pass; two focused defect probes reproduce | Substantially implemented; RV-001 and RV-002 remain |
| P01-T01 | src/core/tests/test_quality_procurement.py | Nine new core methods, meaningful updates to two existing fix calls; inherited SQL replay without aliases | Named methods match the locked matrix and remain within the 18-method cap | Supplied combined and SQL receipts; seven reviewer-run canonical methods with memory-only adaptations | Good coverage of listed normal/pre-commit paths; legacy repeated recorder and post-commit refresh boundaries missing |
| P01-T01 / P03-T01 | src/api/tests/test_role_matrix.py | Two real authenticated HTTP methods, within the four-method cap | Contractor and foreign-case denial, forged-body rejection, remediation, replacement and financial invariance | Supplied 357-test receipt; source inspection | No new contractor portal or body-controlled authority |
| P01-T01 | src/core/tests/test_resident_decisions.py | Missing-binding replacement now refuses before mutation | Existing positive scoped workflow and withdrawal tests remain; no skip/deletion | Supplied combined receipt and source comparison | Compatible tightening, not a weakened validator |
| P02-T01 | src/api/src/zava_forward/api/web/ops.js | Remediation label/status/focus; busy controls; historical evidence state; replacement confirmation | Complete changed-file review against freshly retrieved Web Interface Guidelines | Supplied real Chromium journey; reviewer-run node syntax check | Bounded UI implementation; no browser, screen-reader or WCAG acceptance independently asserted |
| P02-T01 | src/core/README.md; src/api/README.md | Explain authority, evidence, invalidation and actual validation limits | Complete documentation diff and source comparison | Link/anchor inspection and diff whitespace | Main contract is accurate in intent, but unqualified legacy/recovery claims need correction alongside RV-001/RV-002 |
| P02-T01 | docs/reference/README.md; docs/reference/log.md; docs/reference/research/ux/customer-journeys/programme.md | Existing synthesis/index/append-only history updated | Original log prefix retained; existing routes untouched; programme date updated | Complete changed documentation review | Correct placement and evidence classification; no company, regulatory or operational acceptance fabricated |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 / A3 / replacement matrix | Every prior active same-measure decision, not one predecessor, must be retired | PC-001; reachable legacy multi-record states | Current plan functional requirements, detail algorithm and replacement test agree | Original critique Revise retained; PC-001 disposition recorded before implementation | Compatible correction within exact issue criterion; no new user decision required |
| P01/P03 / validation lock | Exact named regression/backend matrix and inherited MSSQL owner | PC-002; pending-prefix and recovery fault obligations | Plan matrix, P03 details, source methods and changes evidence agree | Original critique preserved; PC-002 disposition recorded | Compatible planning correction; no duplicated MSSQL aliases or added framework |
| P01-T01 / resident regression | Refuse unbound replacement immediately rather than create an unacceptably unbound record | Replacement's explicit current-context requirement; changes Amendments and Divergences | Current functional requirement, source and changed resident assertion agree | No material scope change; no fresh planning/critique gate required | Preserves consent boundary and confirmed user intent |
| P03-T01 / SQL harness | Add src/api to the fixture import path after missing tests module | Recorded failed harness attempt followed by actual successful run | Corrected command and cleanup are disclosed | Execution adjustment, not architectural divergence | Compatible; no dependency or acceptance inflation |
| P02/P03 / validation limits | Keep pre-existing form/navigation gaps and configured migration exemptions visible | Changed-file review and pyproject configuration | Plan Follow-Up Items, changes and component guides distinguish engineering from human acceptance | No blanket deferral or claimed WCAG acceptance | Justified boundary, not completion of unrelated requirements |

## Critique and Material Revision Assessment

* Latest critique dispositions: PC-001 and PC-002 both have explicit direct-planner dispositions. The original Complete execution / Revise verdict remains intact.
* PC-001's all-prior-active legacy retirement contract is present in the final plan/details and runtime source/tests. The in-memory canonical replacement method also passed all four Accepted/HANDED/legacy combinations.
* PC-002's exact method/backend mapping, inherited test_mssqlstore.MssqlProcurement selector, prefix preservation and recovery fault cases are present. Six common, one JSON-only and two SQL-only new core methods plus two HTTP methods respect the caps.
* RV-001 and RV-002 are implementation defects within accepted scope, not reasons to retroactively reopen either planning disposition.
* Material revisions: No significant divergent authority, risk policy, payment, fixture, portal, shared-schema or persistence-helper decision was found. No new material plan revision requiring an unrecorded user decision was identified.
* Dependent-work pause assessment: Current artifacts record Ready planning after both dispositions and implementation completion afterwards. No contrary dependent-work evidence was found; exact execution chronology beyond those supplied records was not independently reconstructed.
* Justification assessment: The immediately relevant resident assertion and SQL import-path correction preserve confirmed intent. No rpi-plan or rpi-research destination is needed for the two reproduced defects.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Competent-human quality acceptance | Fictional staff roles do not establish competence, actual delegation, inspection sufficiency or resident understanding | Parent retains a distinct quality-owner/professional validation gate before operational use | Open external validation, not an implementation defect or a new active Pxx task |
| Azure SQL acceptance | An owned disposable local SQL Server proves neither deployed Azure behavior nor tenant/application acceptance | Parent/deployment owner retains distinct authorized Azure acceptance work | Open external validation; no cloud action authorized by this Review |
| Existing quality/work-order form names/autocomplete, draft-navigation and broader web gaps | Exact issue controls do not authorize a workbench redesign or complete accessibility programme | Parent routes a distinct UX/accessibility follow-up to the existing workbench owner | Open non-blocking follow-up, mirrored in changes; not silently added to P02 |

The plan names these boundaries but not individual people. The role/next-action
routing above is a handoff, not a claim that a real person accepted ownership.
Unresolved follow-up items remain outside active implementation and acceptance
claims.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: A known earlier legacy fix recorder is incorrectly treated as unresolvable

* Related scope: P01-T01, A2, retained independence across repeated corrections and legacy records.
* Evidence: src/core/src/zava_forward/core/quality.py:127-139. The code collects all FIXED-history recorders in recorders, but builds identities only from the original/latest participant names and original/latest codes. An earlier recorder whose name appears only in FIXED history is not looked up in the current staff list. The subsequent resolution check calls that still-registered person unknown.
* Concrete reproduction, executed using the real SqlStore on an isolated in-memory SQLite database and the existing fictional STAFF/resident fixture:
  1. Sam submits evidence; Quil returns it.
  2. Quin records correction by SYN fitter 1 with SYN photo 1.
  3. Pam fails reinspection; Sam records correction by SYN fitter 2 with SYN photo 2.
  4. Remove only participants and save, representing a legacy record that predates this new field. All original/latest fields, both defects and FIXED histories remain; Sam, Quin, Quil and Pam remain registered.
  5. Pam, who neither submitted, recorded nor fixed the work, calls reinspect_quality(..., "pass", "SYN independent review").
* Observed result: PermissionError: A contributor's identity is unknown. Ask the quality owner to resolve it before acceptance. The record remains Fixed, awaiting reinspection. The actual current staff list includes Quin Inspect, whose name is retained in the first FIXED history.
* Expected result: Resolve the known earlier recorder from retained history/current staff, include their populated identity aliases in the exclusion set, deny that contributor or their aliases, and permit the genuinely independent Pam. Continue refusing genuinely unresolved legacy identities.
* Impact: A reachable legacy repeated-remediation workflow is permanently denied despite available identity evidence. The documented quality-owner resolution advice cannot solve the lookup omission merely by confirming the already present staff record. This is an availability/correctness defect, not evidence that a non-independent acceptance succeeded.
* Coverage gap: test_quality_identity_history checks repeated cycles with participants and a separate single-submission legacy record. It does not combine legacy absence of participants with different earlier/latest fix recorders.
* Destination: rpi-implement.
* Smallest useful next action: Include historical recorder names/codes in conservative legacy staff resolution, add this combined legacy/repeat regression plus earlier-recorder alias denial, and replay through existing JSON/SQLite/MSSQL owners. Keep unknown-identity denial and all current authority checks.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Post-commit refresh failure reports failure and replays an already committed audit prefix

* Related scope: P01-T01, P03-T01, SQL rollback/current cache/legitimate pending-prefix contract.
* Evidence: src/core/src/zava_forward/core/quality.py:64-78 unconditionally restores prior pending audit for every SQL exception. The existing src/core/src/zava_forward/core/sqlstore.py:611-627 updates committed snapshots, clears pending/touched, then can call _sync after COMMIT when another completed write advanced the sequence after entry synchronization. An exception in that refresh is therefore not a rolled-back write. The changed wrapper does not distinguish that state.
* Concrete reproduction, executed against real in-memory SQLite transactions, not a mocked save result:
  1. Submit a valid scoped quality record with Sam.
  2. Enter a legitimate outer store.lock and queue one audit action SYN_legitimate_prefix.
  3. Immediately before the original save, advance meta.seq by one using a committed SQL UPDATE. This models the relevant sequence effect of an unrelated completed writer between entry synchronization and BEGIN IMMEDIATE; no target-case conflict is introduced.
  4. Wrap only db.execute. Let the original acceptance transaction, case write, audit inserts and COMMIT execute. Raise OSError("SYN post-commit refresh read failed") once on the next SELECT value FROM meta during the post-commit _sync; subsequent recovery reads succeed.
  5. Quil independently accepts the work. Catch the resulting OSError and exit the legitimate outer lock.
* Observed output:

```text
PREFIX_POST_COMMIT: OSError('SYN post-commit refresh read failed') notes= []
PREFIX_POST_COMMIT pending before outer exit: ['SYN_legitimate_prefix']
PREFIX_POST_COMMIT persisted audit actions:
['quality_submitted', 'SYN_legitimate_prefix', 'quality_accepted', 'SYN_legitimate_prefix']
PREFIX_POST_COMMIT duplicate prefix count: 2
PREFIX_POST_COMMIT committed state: Accepted
PREFIX_POST_COMMIT ledger intact: True
```

* A companion execution without a prefix likewise returned the plain OSError with no uncertainty note while committed and cached states remained Accepted and one quality_accepted audit existed.
* Expected result: Distinguish confirmed pre-commit rollback from committed/uncertain outcomes. Never requeue an audit prefix already included in the committed transaction. Do not present a committed quality decision as an ordinary failed operation with no reload/outcome guidance.
* Impact: A transient post-commit read failure can produce misleading retry semantics and duplicate a legitimate audit event while the hash chain still verifies. Passing pre-commit rollback probes does not establish the broader documented failure contract. This finding does not allege self-acceptance or payment execution.
* Coverage gap: test_quality_sql_failures covers pre-save, case-write and audit-insert failures, followed by recovery-read faults. Every such failure precedes a successful COMMIT. It does not exercise a successful commit followed by refresh failure.
* Destination: rpi-implement.
* Smallest useful next action: Add a quality-scoped committed-outcome/prefix regression and correct the wrapper's outcome handling without weakening rowversions, writer-time actor checks, pre-commit rollback or prefix preservation. Keep #95 shared-helper ownership unchanged unless a separately authorized dependency proves unavoidable; do not edit finance.py as a shortcut.

### Reproduction boundary

Both findings used this no-filesystem construction with existing fictional
fixture data; no private data, network service, Docker, Azure or paid model was
used:

```python
import copy
import io
import json
from unittest.mock import patch

import dataset
from test_quality_procurement import STAFF
from zava_forward.core.sqlstore import SqlStore

data = copy.deepcopy(dataset.DATA)
data["staff"] = copy.deepcopy(STAFF)
for case in data["cases"][:2]:
    dataset.supplied_resident_fixture(case)
with (
    patch("builtins.open", return_value=io.StringIO(json.dumps(data))),
    patch("zava_forward.core.sqlstore.os.makedirs"),
    patch("zava_forward.core.sqlstore.open_document_store"),
    patch("zava_forward.core.sqlstore.open_scanner"),
):
    store = SqlStore("synthetic-review-only.json", ":memory:")
```

The mocks prevent filesystem/docstore setup only. The reviewed quality
methods, identity resolution, SQLite schema, transactions, save, audit,
quarantine and lock-exit code execute normally. Probe execution used
PYTHONDONTWRITEBYTECODE=1 and
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests with
.venv/bin/python. Each connection was closed. No probe script, dataset,
scratch directory or test output file was written.

## Defects

* RV-001: Known legacy earlier-recorder resolution omission; rpi-implement.
* RV-002: Post-commit failure misclassification and duplicate pending-prefix replay; rpi-implement.
* Severity summary: 0 Critical, 0 High, 2 Medium, 0 Low.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent's implementation owner adds conservative historical-recorder resolution and combined legacy/repeat tests | Defect within already accepted A2 direction; no policy or authority decision needed |
| RV-002 | rpi-implement | Parent's implementation owner separates committed outcome handling from rollback and tests exactly-once prefix preservation | Defect within accepted SQL recovery/audit direction; no research needed to reproduce |

Later implementation of these routed findings does not require another
Review. The parent owns any already authorized correction cycle and separate
execution/closure evidence, preserving this original review.

## Residual Work

* Distinct human/professional and Azure acceptance gates remain open as described under Plan Follow-Up Assessment.
* Existing broader web-guideline/accessibility work remains a distinct workbench follow-up.
* These external/non-blocking items are not RV defects and do not expand active P01-P03 scope.

## Blockers and Remaining Work

* Review blockers: None. The evidence boundary supports a completed review and credible original verdict.
* Remaining executed-plan markers: None; P01-P03 were executed. Their checked markers do not close RV-001/RV-002.
* Acceptance blockers: Resolve the two reproduced defects through the parent's authorized continuation. No user question, new authority, policy decision or research gap is required.
* No fixes, plan/detail/critique/change/research edits, additional review pass, commit, push or PR action was performed by this reviewer.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Supplied combined unittest command in changes; quality91-final-tests.log receipt | Quality/provider/resident/stock/finance/SQL-store/API/assistant/workflow selection | Passed, supplied execution | Receipt confirms 357 run, 308 pass, 49 existing opt-in skips. Not independently rerun wholesale. |
| Supplied ZF_TEST_MSSQL=1 test_mssqlstore.MssqlProcurement; quality91-sql-final.log and SQL harness inspection | Actual disposable local SQL Server quality/provider replay | Passed, supplied execution | 36 run, 36 pass; actual SELECT 1 readiness and exact owned-container cleanup recorded. Reviewer inspected harness/receipt, did not rerun Docker/SQL Server or independently query container state. |
| Supplied quality91-browser.py/log inspection | Real application Chromium changed quality journey | Passed, supplied execution | Return, missing remediation focus/input retention, keyboard correction, reinspection, handover, replacement cancel/confirm, historical state/no old action, fresh acceptance/handover, three widths and reduced motion. Browser was not rerun by this reviewer. |
| In-memory MemoryQuality adaptation, five named canonical methods | Current actor, aliases/repeated identity, remediation, indices, resident/safety | Passed, reviewer executed | 5 tests in 0.066s. Uses real SqlStore SQLite memory backend with fictional fixtures and no filesystem setup. |
| In-memory MemorySqlQuality adaptation, test_quality_replacement_dependencies and test_quality_sql_failures | Four replacement subcases and pre-commit failure/recovery matrix | Passed, reviewer executed | 2 tests in 0.123s. reopen uses SQLite backup into another memory database and reload, not file restart/durable reopen. Does not replace supplied file/SQL Server evidence. |
| Legacy repeated-recorder probe | Combined legacy/multiple-fixer independent acceptance | Failed expected behavior, reviewer executed | Known Quin remains registered but independent Pam is refused as unknown contributor: RV-001. |
| Successful COMMIT followed by one refresh-read fault, with/without prior pending prefix | Quality outcome and exactly-once legitimate audit | Failed expected behavior, reviewer executed | Committed Accepted state and success audit survive a plain failure; prefix is requeued and recorded twice: RV-002. |
| Supplied configured core/API Ruff, formatter and mypy runs | Existing configured package checks | Passed as reported; configuration inspected | Core counts 58 format-managed/111 mypy source files; API 21/53. quality.py and inherited test files have existing formatting/type exemptions and lint ignores; a configured pass is not strict typing of changed quality code. No new exemption was added. These tools were not independently rerun. |
| node --check src/api/src/zava_forward/api/web/ops.js | Changed JavaScript syntax | Passed, reviewer executed | No syntax error. |
| git diff --check b5d4c840 | Whole tracked implementation diff | Passed, reviewer executed | No whitespace errors. |
| Fresh Web Interface Guidelines source retrieval and complete ops.js read | Changed web file against current rule categories | Completed source review | Native buttons, labels/ARIA status, error focus and confirmation retained; no introduced animation/media/font/image work. Pre-existing form metadata, save-progress and draft-navigation gaps remain disclosed below. No visual/screen-reader/conformance inference. |
| Full discovery, opt-in assistant SQL, Azure, screen reader and real human acceptance | Broader/external validation | Skipped / not run | Not required to execute this bounded Review; no shared persistence helper changed. Supplied 49 skips comprise one Azure acceptance, one existing stock browser and 47 assistant SQL tests; separate quality browser and quality/provider SQL runs do not close those skips. |

### Changed web file findings and retained follow-up

Fresh guideline source:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
All fetched categories were considered for the scoped changed file; unrelated
application surfaces were not audited. Existing Fluent 2 foundations, plain
ASCII/sentence-case content and no-conformance limits remain controlling.

```text
## src/api/src/zava_forward/api/web/ops.js
src/api/src/zava_forward/api/web/ops.js:27 - existing defect/owner inputs lack name/autocomplete; distinct UX follow-up.
src/api/src/zava_forward/api/web/ops.js:82 - existing evidence form fields lack name/autocomplete; distinct UX follow-up.
src/api/src/zava_forward/api/web/ops.js:105 - existing Save evidence path lacks busy progress and field-local server-error focus; distinct UX follow-up.
src/api/src/zava_forward/api/web/ops.js:197 - unchanged work-order note/binding inputs lack name/autocomplete; distinct UX follow-up.
src/api/src/zava_forward/api/web/ops.js:21 - existing workbench draft-navigation warning absent; distinct UX follow-up.
```

The supplied browser log also contains explicitly unknown law-store checks and
server-side BrokenPipeError messages around navigations. The final script
asserts zero browser pageerror events, not zero server log errors. This Review
does not relabel unknown regulatory checks as passed or infer a new quality
defect from the disclosed unrelated log noise.

## Outcome

* Outcome: Not accepted.
* Outcome rationale: Execution is complete and the exact contractor/evidence/supersession architecture is substantially preserved, but material correctness gaps remain in accepted legacy remediation and the promised SQL recovery/audit boundary. RV-001 and RV-002 are independently reproduced, implementation-routable defects. Broad passing suites and actual supplied SQL/browser receipts do not cover those combined edge cases.
* A1 assessment: No contractor approval, closure or payment capability found; staff-assisted evidence and own-case isolation remain intentional. No quality source mutation of finance/grant/payment state was found.
* A2 assessment: Current/new-record independence and remediation controls pass the selected checks. Known repeated legacy recorder resolution is defective under RV-001; no unauthorized successful acceptance is alleged.
* A3 assessment: Every active same-measure acceptance/handover is invalidated; evidence/history and siblings remain; new acceptance and resident handover are required. Existing stale rowversion and resident/safety protections remain. RV-002 limits confidence in unqualified failure/rollback claims, not the normal supersession algorithm.
* A4 assessment: Required implementation evidence was actually supplied with honest skips/exemptions and external limits. Reviewer execution adds bounded in-memory evidence and defect reproduction, not invented independent SQL Server/browser/human/Azure/WCAG acceptance.
* #84/#94/#90/#95 boundary: Current stock/current-actor, separate finance and merged provider safeguards are retained in source and supplied regression selection. finance.py, dataset.py, app.js, server.py, scenario manifest and shared SQL helpers have no diff against the supplied base. No other worktree or private dataset was inspected.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Parent continues with RV-001 and RV-002 under the already authorized concrete correction allowance; retain original verdict and separate execution/closure evidence |
| Decision gap or invalid assumption | None | No significant/divergent decision or new authority required |
| Material evidence gap | None | Existing supplied evidence and focused reproductions are sufficient to route the defects |
| Non-blocking residual work | Distinct human/Azure and workbench UX follow-ups | Parent preserves external acceptance gates and existing UX ownership; no expansion into active P01-P03 |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: Seven canonical methods passed using disclosed in-memory adaptations; both focused defect probes reproduced; syntax and diff checks passed. Supplied 357-test, 36-SQL-Server and Chromium results inspected but not independently repeated.
* Blockers: No review blocker; RV-001/RV-002 block accepting the delivered bounded recovery/legacy contract.
* Original verdict preservation: This canonical record closes the task's one independent Review. Corrections do not overwrite it or imply a new review mode/pass.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/quality-handover-controls-91-research.md](.copilot-tracking/research/2026-10-17/quality-handover-controls-91-research.md) | Research evidence |
| [.copilot-tracking/plans/2026-10-17/quality-handover-controls-91-plan.md](.copilot-tracking/plans/2026-10-17/quality-handover-controls-91-plan.md) | Accepted implementation direction |
| [.copilot-tracking/details/2026-10-17/quality-handover-controls-91-phase-details.md](.copilot-tracking/details/2026-10-17/quality-handover-controls-91-phase-details.md) | Phase completion context |
| [.copilot-tracking/reviews/plans/2026-10-17/quality-handover-controls-91-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/quality-handover-controls-91-plan-critique.md) | Original critique and dispositions |
| [.copilot-tracking/changes/2026-10-17/quality-handover-controls-91-changes.md](.copilot-tracking/changes/2026-10-17/quality-handover-controls-91-changes.md) | Implementation validation/handoff |
| [.copilot-tracking/reviews/logs/2026-10-17/quality-handover-controls-91-review.md](.copilot-tracking/reviews/logs/2026-10-17/quality-handover-controls-91-review.md) | Original completed Review |

## Next Steps

Return this one completed Review to the active parent. The parent owns the
already authorized rpi-implement continuation for RV-001/RV-002, preserving this
original Not accepted verdict and separate correction evidence. No new user
decision, additional Review or reviewer-side implementation is required.

## Implementation-owner closure addendum (2026-10-17)

The independent Review above is preserved verbatim. Its original execution is
Complete and original outcome Not accepted; this is not a repeated Review or
independent regrade. Original prefix SHA-256:
28e92d3b759320a29f52a4468c303c778af7f2d0a8a293ce9ed2d8bf04dd62cc.

Caller-authorized implementation continuation P04-T01 reproduced both findings
before production correction and corrected both:

| Finding | Implementation correction | Local closure evidence |
| --- | --- | --- |
| RV-001 | Historical FIXED recorder names enter actual legacy staff lookup, retaining alias exclusion/unknown refusal | Shared JSON/SQLite and inherited actual SQL Server combined legacy/repeated-recorder test denies earlier recorder/alias for independence and permits independent Pam |
| RV-002 | Confirm own committed snapshot before shared recovery; never requeue committed prefix; explicit quality outcome error and HTTP 503 committed/reload response | Real second-store unrelated commit, actual own COMMIT then transient/persistent read fault, with/without legitimate prefix; exactly-once success/prefix, original cause, clean cache and reopened state; authenticated HTTP 503 and actual Chromium notice/reload |

After production correction, 361 selected tests ran: 312 pass, 49 existing
opt-in skips. Final overlapping focused quality/HTTP/content/design/route
selection: 101 pass. Final actual isolated SQL Server inherited replay: 38 pass,
zero skip; exact owned loopback container removed. Actual Chromium full quality/
handover/replacement and committed-refresh error/reload journey passed with zero
page errors. Configured core/API Ruff, format, mypy and JS/whitespace checks pass.
External human/Azure/screen-reader/WCAG limits remain unchanged.

Detailed commands, fail-before/correction receipts and scope reconciliation:
.copilot-tracking/changes/2026-10-17/quality-handover-controls-91-changes.md.
No implementation findings remain locally open; no independent Pass is claimed.
