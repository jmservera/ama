---
title: Issue 122 continuity epoch and export original Review
description: Single independent bounded implementation Review
ms.date: 2026-10-18
---

## Scope and Evidence

* Task ID: 122. Review date: 2026-10-18.
* Assessment count: exactly one original independent RPI Review; no subagents, amended verdict, second Review or implementation correction.
* Current task requirements: the supplied reviewer prompt is authoritative, including all epoch, offline evidence, real SQL/manual validation, shared-file authorization and operational exclusions.
* Research: .copilot-tracking/research/2026-10-18/issue-122-continuity-epoch-export-research.md.
* Plan: .copilot-tracking/plans/2026-10-18/issue-122-continuity-epoch-export-plan.md.
* Phase details: .copilot-tracking/details/2026-10-18/issue-122-continuity-epoch-export-phase-details.md.
* Original critique: .copilot-tracking/reviews/2026-10-18/issue-122-continuity-epoch-export-plan-critique.md, Complete / Revise, two High findings; read unchanged.
* Changes: .copilot-tracking/changes/2026-10-18/issue-122-continuity-epoch-export-changes.md, including final validation and exact source hashes.
* Repository context read: docs/case_study_48_original.md; relevant addendum exercise, authority and continuity/RAI sections in docs/case_study_48_addendum.md; docs/reference/README.md index; docs/reference/memory.md; housing-association primer; API/core component guides. No new legal or company-authority conclusion is made.
* Exact implementation boundary: git diff against 99056cae7bc679d2ace3e42c75f28577cfce8887 for src/core/src/zava_forward/core/assistants.py, continuity.py, ai_tasks.py, store.py, src/api/pyproject.toml and src/api/README.md, plus untracked src/api/tests/test_continuity_epoch_export.py. The complete changed source/test boundary was read. Unchanged SQL writer, release/reference, projection, API handler and fixture dependencies were inspected only to trace changed behavior.
* Branch: fix/continuity-epoch-export-122. HEAD independently confirmed equal to the pinned base. Existing implementation/artifact modifications were preserved; no switching, committing, pushing or remote mutation.
* Issue relationship: supplied research/user context records blockedBy empty, parent #113 as hierarchy only, and PR #269 as merged baseline, not acceptance. No fresh GitHub lookup was performed.

## Opening Review State

* Interpreted review goal: assess the entire supplied bounded #122 epoch/export implementation once, preserving the original complete findings and verdict.
* Review scope: P01-P03, exact base and pre-review HEAD 99056cae7bc679d2ace3e42c75f28577cfce8887; four core modules, new focused test module, API packaging and guide.
* Evidence readiness: research, current plan/details/changes and original Complete/Revise critique are available and read; implementation source and supplied final validation require independent comparison.
* Acceptance basis: current task requirements, plan acceptance criteria and PC-001 atomic legacy publication / PC-002 independent offline verification dispositions. Operational #122 acceptance is excluded.
* First comparison boundary: source diff plus untracked test module, current artifact reconciliation, and safe synthetic local validation.
* Active read-only boundaries: write only this canonical Review record; no source, tests, plans, details, research, changes, critique or state edits; no delegation, PR, commit, new SQL container, private data, inference or Azure.
* Initial blockers: known authenticated HTTP export 403 in protected shared projection.py requires coordinator authorization/correction. This blocks acceptance, not the ability to review.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Permitted manager cannot reach continuity export over HTTP

* Related scope: P02-T01, P03-T01; actual HTTP export acceptance.
* Evidence: src/core/src/zava_forward/core/projection.py:36-37 omits both continuity and continuity_export from STAFF_GET; src/api/src/zava_forward/api/server.py maps and implements those endpoints but its outer authorization denies them. Independently executed src/api/tests/test_continuity_epoch_export.py:628-629 fails with 403 != 200 for the authenticated manager after completing the manual and stale-review assertions.
* Reproduction: run HttpTests.test_http_epoch_read_review_export_and_manual_actions with the installed distributions and test-helper PYTHONPATH. No projection bypass or patch is needed or permitted.
* Impact: the supplier-independent export cannot be obtained through the actual authorized service boundary; direct Store tests do not establish delivery. The continuity register GET is also affected by the same omission.
* Destination: rpi-implement, coordinator-owned correction only.
* Smallest useful next action: obtain explicit #87 shared-file authorization, then append only continuity and continuity_export to STAFF_GET in src/core/src/zava_forward/core/projection.py; retain inner manager/export and continuity-view role restrictions and contractor denial. Rerun actual permitted HTTP and negative-role checks. This Review does not grant that authorization.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Offline verifier accepts explicitly truncated or missing proposal evidence after outer digest recomputation

* Related scope: P02-T01, PC-002; independent completeness and release-reference verification.
* Exact affected file: src/core/src/zava_forward/core/continuity.py:329-410 and :412-444, particularly :337 and :426.
* Evidence: release_problems iterates bundle.get("assistant_proposals", []) and validates task-release counts but never validates the assistants proposal total/exported/truncated metadata. verify_export does not require assistant_proposals or assistants and ultimately trusts complete=true for this omission.
* Independently executed reproduction: build the existing serialized active-to-revoked OfflineTests.bundle fixture with one accepted proposal. First remove assistant_proposals while preserving assistants.total=1. Alternatively obtain service.export(limit=0) and continuity_export: the producer correctly marks complete=false, assistants={supported:true,total:1,exported:0,truncated:true}. In either case force complete=true, clear incomplete_reasons and recompute the ordinary outer digest. verify_export(bundle, separately_retained_original_head) returns valid=true, problems=[], complete=true in both cases. The ledger and externally held head are unchanged.
* Impact: removing the proposal section hides the retained task-release references from independent resolution, and a bundle explicitly declaring proposal truncation is still certified complete. This is a structural inconsistency with retained counts, not the documented impossibility of authenticating a wholesale consistent rewrite of unanchored release history.
* Destination: rpi-implement, later coordinator correction.
* Smallest useful next action: independently require/check the serialized proposal section and supported/unsupported source metadata, reconcile list length with exported/total counts, reject declared truncation or missing/unavailable required proposal evidence regardless of complete, and add both recomputed-digest negatives with the unchanged external head. Preserve legitimate unsupported JSON-store semantics. Do not solve this by trusting producer reasons or the outer digest alone.

## Execution Status

* Review execution status: Complete.
* Implementation execution assessment: P01/P02 source work and P03 validation/handoff executed; execution checkboxes do not assert successful acceptance. The retained failing HTTP boundary and newly found verifier defect prevent acceptance.
* This reviewer independently read the entire changed boundary and reconciled all supplied task artifacts, ran synthetic installed-source regressions and adversarial verifier probes, verified all seven source hashes and all 72 Store signatures, inspected the existing image ID and confirmed no issue-owned containers remain.
* Actual MSSQL and hardened-image test execution below is supplied implementation evidence, not newly executed by this reviewer. No new SQL container was permitted or created. That limitation does not prevent a credible original bounded Review verdict.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Epoch lifetime, durable gates, legacy publication/cache | Reconciled | Epoch-qualified identity and persisted reads preserve dispositions. Source inspection and independent tests support the covered lifetime paths. |
| P02-T01 | Retained release snapshot, lifecycle envelopes and verifier | Partial functional conformance | Referenced release checks are implemented and tested, but independent proposal completeness is bypassable: RV-002. Actual HTTP access is blocked: RV-001. |
| P03-T01 | Final host/SQL/manual/image/static evidence | Reconciled as execution, not acceptance | Changes explicitly preserve one HTTP failure in each affected environment and distinguish Unknown regulatory evaluation. |
| P03-T02 | Frozen source hashes and one original Review handoff | Reconciled | No shared-file bypass, source self-fix or knowingly defective PR. This record is the one original Review. |
| Follow-Up Items | Human/Azure gates and deployment/configuration limits | Reconciled | Outside this bounded source correction; distinct follow-up owners/actions below. |

## Completed Work Assessment

| Marker | Files | What changed and why | Completion/validation evidence | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/assistants.py | Creation epoch enters durable identity; claim/dispatch/complete/view/review/export check currentness. Pending/leased failures do not become current proposals; ready/accepted history remains. | Eight new EpochTests pass independently, including review/suspend overlap, provider-in-flight suspension/restart, old-process refresh, missing bindings, proactive scan identity and unknown usage reservation. Existing assistant/dispatch suites also ran. | Covered source contract supported; unsupported pre-gate deployments are not covered. |
| P01-T01 | src/core/src/zava_forward/core/continuity.py; ai_tasks.py; store.py | Refresh persisted epoch under lock; shared checked continuity-document publication fence; quarantine late legacy text/document/priority before publication; gate review/priority/cache. | Three LegacyTests pass independently. The deterministic save barrier allows an independent Store to commit suspend/restart before old publication; optimistic writer rollback/reload then local-only retry produces one quarantined record and manual/non-actionable return. | PC-001 implemented, not merely documented. Existing SQL writer checks and atomic rollback cover the added fence without shared adapter edits. |
| P02-T01 | src/core/src/zava_forward/core/assistants.py; continuity.py | Export active reference-time snapshots separately from current status/revision, with release-associated event ID/time/body/counts; resolve durable and legacy references offline. | Four OfflineTests pass independently, including eight recomputed-digest variants, offline store-access refusal, legacy release retention and producer missing/truncated/unavailable flags. Existing ledger-tail and external-head negatives also pass. | Release-specific portion of PC-002 supported. Full independent completeness remains defective under RV-002. |
| P03-T01 | src/api/tests/test_continuity_epoch_export.py | Sixteen new semantic test methods, inherited MSSQL runs and three inherited HTTP regressions; no test removals. Real HTTP/manual actions replace note-only claims. | Independent 307-test combined run: 257 passed, 49 opt-in SQL skips, one known HTTP export failure. | Test ownership/30-method ceiling met; adverse regression truthfully retained. The contractor-export assertion after the failing manager assertion is not reached by that new test. |
| P03-T01/P03-T02 | src/api/pyproject.toml; src/api/README.md | Narrow mypy fixture override and explicit epoch/export/compatibility/manual/operational limits. | Complete diff read; supplied static/image checks; independent whitespace, source hashes and signature checks. | No dependency changes, framework swap or UI change. Documentation honestly names the export blocker; it does not make that blocker acceptable. |

No new raw provider prompts/inputs, provider credentials or expanded role access were added by this diff. Existing capability-specific capture and permitted historical output/provenance remain. Manager-only export and contractor denial remain source-level controls; RV-001 requires a narrowly authorized shared-route correction, not disabling projection.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Update and rationale | Trigger / user decision | Reconciliation | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01/P03-T01 | Atomic legacy decision/publication using existing optimistic continuity writer; deterministic legacy overlap | PC-001 direct disposition; already required cross-epoch denial, no divergent user choice | Plan Critique Disposition, details publication rule, changes P01 and tests agree | Supported by actual code and independently passing SQLite overlap. Supplied actual MSSQL evidence is distinct. |
| P02-T01 | Independent release reference, snapshot and lifecycle-envelope validation, including recomputed outer digest | PC-002 direct disposition; no divergent user choice | Plan/details and changes agree on intended oracle | Implemented for retained references, but omission/truncation of the proposal collection still evades the verifier: RV-002. |
| P03 execution markers and handoff | Completed execution with preserved HTTP failure and protected-file restriction | Actual 403; current user explicitly requires coordinator authorization for #87 overlap | Plan final paragraph, details reconciliation, changes blocker and README all retain it | No hidden divergence or premature acceptance claim. Shared projection correction is not authorized by those prose updates. |
| P03 final verifier hardening/source freeze | Final offline checks, final image and exact hashes supersede earlier execution snapshots without erasing failures | Final changes evidence and supplied frozen source boundary | Seven hashes independently match; final image ID matches read-only inspection | Evidence is current for this Review. No second critique or Review was performed. |

## Critique and Material Revision Assessment

* The original Complete / Revise critique is retained intact. PC-001 and PC-002 were explicitly dispositioned in the plan/details before implementation according to the supplied artifact sequence. No independent historical filesystem timing proof is claimed.
* PC-001: addressed in actual implementation. continuity_publish surrounds the final decision and callback with the existing synchronized boundary; publication_fence forces _proc_write to compare the observed continuity document inside the same SQL write transaction that inserts the record. A committed competitor invalidates and rolls back the old append; retry is local, not another provider call. Text/document quarantine is present before add_record.save, not a later second status save. Priority uses the same publication mechanism. Deterministic SQLite races pass; actual MSSQL races are supplied passed evidence.
* PC-002: release-specific implementation is substantive: coherent assistant transaction reads full snapshots, mutable status/revision and event envelopes; offline checks independently recompute references, inspect task association, event IDs/timestamps/counts and current lifecycle status. The supplied/new release-negative fixtures pass independently. The overall completeness boundary is not closed: RV-002 certifies a missing/truncated proposal collection and therefore avoids checking its retained references.
* No significant divergent architecture, general configuration-control expansion, protected-file edit or user-decision substitution was found. No additional planning or research stage is needed for the two defects; both fit the accepted direction.
* No unaccepted dependent-work resumption is inferred from the explicit direct dispositions. Review does not upgrade those dispositions to defect closure or operational approval.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Genuine OQ-017 named authority and witnessed authorized drill | Constructed fixture identities/authority strings cannot supply real delegation or witness acceptance | Project/control owners obtain genuine authority and witness the separately approved drill | Remains unmet, distinct operational follow-up; not a new source defect. |
| Immutable externally held Azure head and Azure SQL drill | Local ledger checks, local SQL Server and self-contained hashes do not establish external immutability or Azure recovery evidence | Authorized platform/evidence owners arrange external head custody and approved Azure SQL drill | Remains unmet, distinct operational follow-up; do not create Azure activity from this Review. |
| Pre-gate image exclusion | Refresh only protects code containing the gates; an old executable can still serve without them | Deployment owner stop/drain unsupported images or enforce external serving exclusion before relying on the control | Explicit residual deployment prerequisite; no claim current source can retrofit old images. |
| Wider serving configuration reversibility | Register entries and reversals are evidence, not serving configuration controls | Coordinator/product/platform owners define a separate bounded work item if required | Outside active P01-P03; no acceptance credit from the general change register. |

Unresolved plan follow-ups remain distinct from active defects and do not expand this bounded implementation. Their current unmet state is mirrored in changes and documentation.

## Defects and Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001, High | rpi-implement | Coordinator obtains #87 authorization, applies only the shared-route allowlist correction and validates positive/negative HTTP access | Implemented delivery remains unreachable for its permitted user. |
| RV-002, High | rpi-implement | Coordinator assigns independent proposal collection/completeness checks and the two unchanged-head negative regressions | Offline verifier contradicts retained evidence metadata despite a recomputed valid outer digest. |

These are the complete findings from this one original Review: 0 Critical, 2 High, 0 Medium, 0 Low. Later coordinator correction evidence is separate; it must not rewrite this verdict or findings or require another original Review. Maximum two later coordinator correction rounds are permitted by the user; this Review performs none.

## Residual Work

The four distinct follow-ups above remain open with their named owner roles/next actions. Self-contained hashes cannot authenticate a wholesale consistent rewrite of task-release events that the application ledger does not bind. Externally supplied ledger heads remain necessary and were preserved/tested; they do not authenticate that separate release history. No remote cancellation, exactly-once billing, live approvals, real inference, regulatory compliance or full #122 operational acceptance follows.

## Blockers and Remaining Work

* Acceptance blockers: RV-001 and RV-002. No coordinator authorization was available for the protected projection.py change; this reviewer neither supplies nor invents it.
* Remaining bounded corrections: only the routed defect work, under the coordinator's later implementation authority. P03's completed execution markers remain truthful but are not universal Pass evidence.
* No knowingly defective PR should be published. No PR, commit or source fix was made during this Review.
* Full issue acceptance remains outside scope. Genuine authority, witnessed authorized drill, external immutable Azure head and Azure SQL drill remain unmet regardless of subsequent bounded corrections.

## Validation Evidence

### Independently performed by this reviewer

All Python tests used .venv/bin/python with installed src distributions and PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests. PYTHONDONTWRITEBYTECODE=1 was set for test/probe runs. tempfile.tempdir was explicitly set to the current worktree before fixtures ran, so synthetic test files stayed local and were removed by fixture cleanups; no external datasets were read.

| Command / boundary | Result | Meaning |
| --- | --- | --- |
| git status --short; git branch --show-current; git rev-parse HEAD; complete git diff against pinned base and direct new-test reads | Passed inspection | Exact requested branch/base and source boundary; existing modifications preserved. |
| Combined unittest loader selectors: test_continuity_epoch_export.EpochTests, LegacyTests, OfflineTests, HttpTests; test_continuity; test_ai_tasks; test_assistants; test_assistant_release; test_assistants_dispatch; test_workflows; test_mvp; test_sqlstore; test_governance; test_recovery; test_role_matrix | Failed overall: 307 run in 76.150s, 257 pass, 49 opt-in MSSQL skip, one failure | Failure is test_continuity_epoch_export.HttpTests.test_http_epoch_read_review_export_and_manual_actions at line 629: 403 != 200. Counts reconcile the supplied 220 targeted plus 87 existing regressions. |
| OfflineTests.bundle fixture, serialize, remove assistant_proposals; force complete=true, clear reasons and recompute digest; verify with unchanged separately retained ledger head | Unexpected valid=true, problems=[], complete=true | Independent RV-002 reproduction; proposal metadata still says total=1. |
| Same fixture, actual service.export(limit=0) through continuity_export; retain total=1/exported=0/truncated=true; force complete=true, clear reasons, recompute digest; verify with unchanged separately retained ledger head | Producer incomplete as expected; verifier unexpectedly valid=true | Second independent RV-002 reproduction, without deleting or rewriting contradictory metadata. |
| AST argument-signature comparison of Store methods with git show pinned base | Passed, all 72 identical | No Store method signature drift. |
| SHA-256 of seven frozen source/test/config/doc files | Passed, all seven equal changes evidence | Exact reviewed snapshot recorded below. |
| git diff --check | Passed | No whitespace errors in current tracked patch. |
| docker image inspect zf-issue122-api:local | Passed read-only inspection | Final image ID is sha256:7ad70d5c969ec33fd1b88ae38d53c3a5aaaa34f76af5c3ca339a0944b85040ce. No reviewer image execution claimed. |
| docker ps -a --filter name=zf-issue122- | Passed, no matching containers | No issue-owned containers remain; none created by this Review. |

The real HTTP/manual test reached and passed manual case call, resident complaint/challenge, hazard raise/refer/receive/accept/repair, self-release refusal and blocked retrofit advance during suspension, then stale detail/list/review assertions, before failing manager export. The synthetic App has no law store; logs explicitly say rule checks Unknown. Independent hazard/authority gates ran, but no regulatory evaluation Pass is claimed. The final contractor denial assertion in that test is after the failure and was not executed.

### Supplied implementation evidence, read and assessed but not rerun here

| Evidence recorded in changes | Actual recorded result | Review treatment |
| --- | --- | --- |
| Five failing-first epoch tests before source correction | 5 run / 5 fail | Historical failing-first evidence, not independently rerun against the frozen corrected source. |
| Final targeted host suites | 220 run / 170 pass / 49 opt-in MSSQL skip / one HTTP export failure | Independently reproduced within combined run above. |
| Existing store/recovery/governance/role suites | 87 run / 87 pass | Independently rerun within combined run above. |
| Final focused epoch/legacy/offline/continuity after verifier additions | 30 run / 30 pass | Same selectors covered in independent combined run, not a separate 30-test rerun by reviewer. |
| Actual uniquely owned loopback SQL Server 2022 RTM-CU27-GDR 16.0.4305.5, four new MSSQL classes plus existing selected contracts | 66 run / 65 pass / one identical HTTP export failure / no skips | Source test fixtures really open independent SQL connections, with deterministic barriers and UUID-owned databases. Supplied actual SQL, not SQLite emulation or reviewer-created SQL. |
| Final actual local MSSQL offline checks after verifier additions | 4 run / 4 pass / no skips | Supplied final release-verifier execution; does not include the reviewer-discovered missing-proposal negatives. |
| Ruff, format and mypy in API/core/agents; final API/core checks | All pass; mypy 57/122/23 files respectively | Supplied static evidence; not newly run by this reviewer. |
| Final source-context image/check-container and security negatives | Final 7ad70d5c image; hardening, plain/hardened startup and negative probes pass | Image ID independently matches; original runtime checks supplied only. |
| Affected tests in final installed nonroot/read-only image | 19 run / 18 pass / one HTTP export failure | UID/GID 10001, zero capabilities, no-new-privileges, writable tmpfs only; no false all-pass claim. |
| Four installed image source hashes | Match worktree | Supplied image parity; host source hashes independently matched, image file parity not rerun here. |

No browser was run because no UI changed. No new SQL container, Docker build, Azure SQL/Azure activity, live inference, private data, real notices, external approval or external ledger-head storage occurred during Review. Local SQL Server is not Azure SQL. No optional SQL skip was treated as a SQL pass.

### Frozen source hashes

| File | SHA-256 independently verified |
| --- | --- |
| src/core/src/zava_forward/core/assistants.py | 878bdff0b7cd981f3ae7337ba18796de60d12477dccc85dcad42c11438b63600 |
| src/core/src/zava_forward/core/continuity.py | dc15e394a8d7eacf7f25d7a5bf2d06f10ab544e48ec7ca64ae5a26a555f1f92e |
| src/core/src/zava_forward/core/ai_tasks.py | c66d591851b40cffb3eba2f2eb2acae4386ffba31d1ed08d85e6a27eac9eb02c |
| src/core/src/zava_forward/core/store.py | 3dac9b7269bf3b24f65bb439523d865bccdc198a92946d4539e535bcd6989055 |
| src/api/tests/test_continuity_epoch_export.py | 50f20761cc88c3c3fb4b531136b5946f8965e7b124374ac7c89a6e122d2545b9 |
| src/api/pyproject.toml | 828a5ab401afeb1cedb60bd507c6e1ef6c423c3597619cf87153b432d5edbebf |
| src/api/README.md | e35df30af38b092ddfcefeab032f78f2d1d768cb49ae3a592d6b5e899bae17fa |

## Outcome

* Original outcome: Not accepted.
* Rationale: substantive durable/legacy epoch enforcement and retained release-specific offline validation are implemented and covered, but the actual export endpoint denies its permitted manager and the offline verifier accepts structurally missing/truncated proposal evidence. Both are material acceptance failures, not justified scope divergences. Passing source/component tests do not make this source accepted.
* Original execution status: Complete. Validation failures and unavailable fresh SQL/image reruns are explicitly distinguished from review execution.
* This is the complete original verdict and finding set. Later correction evidence must not amend or replace it.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defects | rpi-implement | Coordinator owns RV-001/RV-002, obtains protected shared-file authorization first for RV-001, and applies no more than the permitted two later correction rounds. |
| Significant decision gap / invalid assumption | None found requiring a new planning stage | Existing intent already requires both corrections; authorization is not inferred. |
| Material research gap | None requiring rpi-research for this bounded verdict | Supplied real SQL/image evidence is clearly attributed; operational authority/Azure evidence remains distinct. |
| Non-blocking residual work | Distinct operational/deployment/configuration follow-ups | Named control, evidence/platform and deployment owners as listed in Plan Follow-Up Assessment. |

* Review execution: Complete.
* Original outcome: Not accepted.
* Severity: two High findings.
* Validation: independent 307-test run and two verifier negatives; supplied real SQL and hardened-image evidence retained, including failures.
* Publication blocker: do not publish a knowingly defective PR. No live or full #122 acceptance is granted.

## Next Steps

Return this one original Review to the parent coordinator. The coordinator must obtain #87 shared-file authorization and own later rpi-implement correction of RV-001/RV-002, preserving this record and the original critique unchanged. No worker self-fix, second Review, PR or commit is authorized by this handoff. The separate human/Azure/deployment follow-ups remain open.
