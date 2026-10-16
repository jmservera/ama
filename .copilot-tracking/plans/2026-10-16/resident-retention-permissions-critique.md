---
title: Resident retention and permissions final-candidate critique
description: One bounded evidence-grounded assessment of the issue 86 follow-up
ms.date: 2026-10-16
---

## Metadata

* Task ID: issue-86-resident-retention-permissions
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/resident-retention-permissions-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/resident-retention-permissions-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate assessment; no implementation or agent dispatch.

## Inputs and Criterion Boundary

* Caller requirements: full src-only implementation, with requested documentation/log and tracking exceptions; five calendar years from first recorded resident contact, including withdrawn decisions and expired authority; confirmed field matrix; local unit, ruff, mypy and application evidence before real Azure SQL in ama/uksouth; authorized cost cleanup; commit/push/PR using Refs #86, never Closes.
* Planning evidence: the supplied plan, phase details and .copilot-tracking/research/2026-10-16/resident-retention-permissions-research.md, including W1-W3 and C1-C5. Owner choices recorded there and in the caller's instruction are accepted, not independently reopened.
* Repository context: docs/case_study_48_original.md; relevant exercise rights and retention sections of docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md.
* Necessary code evidence: resident_decisions.py, controls.py, projection.py, store.py, doc_controls.py, sqlstore.py and mssqlstore.py under src/core/src/zava_forward/core; existing core resident tests/dataset; src/api/tests/test_resident_api.py; relevant src/api/src/zava_forward/api/server.py routes and web/panels.js; existing core/API validation guidance and project configuration.
* Criterion boundary: correctness, preservation of existing safeguards and credible acceptance evidence. This is not legal certification, an Azure execution, an implementation review, a UI style review or an expansion of issue #86.
* Dependencies: P01 local evidence precedes P02 Azure evidence; Azure evidence precedes group deletion and delivery. The authorized group wipe and existing role mapping are not pending approvals.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| W1; P01-T01 calendar schedule | Partial | Calendar years, leap day, earliest evidence and unknown history are explicit; the distinct safe-contact path and invalid historical dates need an executable contract, PC-002. |
| C3; P01-T01 retention deletion | Partial | Existing manager/legal-hold boundary is appropriate; exact payload and retained-copy evidence is incomplete, PC-001. |
| W1; P01-T01 overdue reliance | Partial | Work gating is planned, but representative disclosure checks are a separate reliance path, PC-004. |
| W2; C1; P01-T02 registered-human recording | Covered | Named identity equality and resident/legacy endpoint coverage are explicit; manager/support read-only is preserved. |
| W2; C1; P01-T02 staff viewing | Partial | Separate rights are explicit, but the second recursive redaction pass can still suppress authorized decision notes, PC-003. |
| W2; C4; P01-T02 contractors | Covered | Per-measure resident_gate reuse, conservative Hold and no private reasons preserve the selected boundary. |
| W2; C5; P01-T02 agents | Covered | Allow-listed task inputs and private authority/wishes/safe-route prompt/citation canaries are specified; no human writer role is granted. |
| P01-T03 local unit/ruff/mypy/application evidence | Partial | Existing suites, red/green evidence and real loopback HTTP are credible; default fixture scratch paths violate the current execution restriction, PC-006. |
| P02-T01 synthetic real Azure SQL | Partial | Isolated database, existing ama/uksouth server, Entra token and restart checks are appropriate; historical SQL deletion claims need qualification, PC-005. |
| W3; P02-T02 costs and cleanup | Covered | Full group deletion is authorized, also on verification failure, with group nonexistence verification. |
| P02-T03 documentation and delivery | Covered | Core/API README, reference index/log, single implementation Review, privacy-safe identity, trailer, push and Refs #86 are specified; no merge or issue closure. |
| Source scope and deferred acceptance | Covered | src-only implementation with explicit exceptions; no private resident input, operational acceptance, legal certification or cross-case identity invention. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 4 High, 2 Medium, 0 Low.
* Rationale: The selected implementation is coherent and the confirmed choices are sufficiently resolved. Six bounded corrections are needed to make deletion, first-contact capture, field visibility, representative reliance and validation claims testable without violating existing storage or environment boundaries. All are planner-owned corrections, not new product decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Define the deletion inventory and account for legacy decision content

* Related IDs: W1, C2, C3, P01-T01, P02-T01.
* Evidence: Phase details P01-T01 says to remove decision/authority/wishes/contact-reference payloads while preserving complaints and unrelated contact history. src/core/src/zava_forward/core/store.py:set_decision stores the legacy decision separately in c["decision"] and copies caller-supplied note text into the audit detail. resident_decisions.py also stores references in resident reviews and service requests, outside the principal authority/decision collections.
* Concern: The proposed purge has no exact retained/deleted field inventory or retained-copy assertion. Clearing measure_decisions and representative_authorities alone can leave legacy decision content or resident references; attempting to erase old audit entries instead would damage the immutable audit boundary.
* Impact: A successful purge test could assert empty primary collections while retained decision content remains, or implementation could remove complaint evidence that the plan explicitly preserves.
* Smallest useful change: In P01-T01 name the scheduled fields, legacy decision reset, references requiring removal or explicit preservation, and the minimal first-contact/tombstone metadata that survives. Prevent new legacy decision notes from entering immutable audit detail. Explicitly record inherited audit-content limitations without rewriting history or adding an unrelated audit migration.
* Action owner: Planning parent.
* Exact resolving evidence: A field inventory plus synthetic canary tests that inspect stored and projected state after purge and restart in JSON/SQLite, with the same assertions in Azure SQL; preserved complaint outcomes/unrelated contacts and an intact audit chain; no new resident note content in legacy decision audit entries. Previously retained audit content is identified as a limitation, not claimed erased.
* Decision route: Direct planner correction. The caller already confirmed retention scope; this does not require a new erasure platform or owner policy decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: First-contact capture must cover the separate evidenced safe-contact path

* Related IDs: W1, C2, P01-T01, P01-T03.
* Evidence: P01-T01 explicitly persists the marker on log_call. src/core/src/zava_forward/core/store.py:log_call appends contacts, whereas resident_decisions.py:_res_safe_contact_record independently records a resident-confirmed safe route, evidence source and timestamp in resident_contact_history. Representative workflows can use that path without calling log_call, as src/api/tests/test_resident_api.py demonstrates.
* Concern: Naming only log_call and unspecified historical contacts leaves a credible route where actual evidenced resident contact never starts the schedule. The historical-date contract also does not state how malformed or future contact dates are treated.
* Impact: A newly recorded or imported safe-contact confirmation could leave retention Unknown indefinitely or defer the five-year boundary incorrectly.
* Smallest useful change: Enumerate the evidenced contact collections and recording paths used for the earliest marker, including safe-contact confirmation where its recorded event establishes contact. Reject or ignore invalid/future evidence as unusable, keep genuinely missing history Unknown, and preserve the earliest valid marker through later contact, purge and restart. Do not infer contact from authority/decision/design dates.
* Action owner: Planning parent.
* Exact resolving evidence: Tests for safe-contact-only capture; earlier imported contacts versus later marker; invalid/future-only evidence; subsequent contact that does not reset the schedule; persistence across restart. Each test asserts the exact anniversary or Unknown, not merely the presence of a metadata field.
* Decision route: Direct planner correction implementing the already confirmed first-recorded-contact rule.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Separate rights must survive the recursive vulnerability redaction pass

* Related IDs: W2, C1, P01-T02, P01-T03.
* Evidence: src/core/src/zava_forward/core/projection.py:redact_staff_detail first removes resident evidence based on RESIDENT_ROLES/can_see_reason, then independently calls hold_notes when can_see_reason is false. hold_notes recursively replaces every note field. The default reason-role set excludes Retrofit Coordinator and Programme Support Officer. resident_decisions.py stores the supplied resident answer in note.
* Concern: Splitting resident view/write role sets or removing only the first reason-role condition does not deliver the confirmed resident-field matrix: authorized viewers can still receive a held marker instead of the resident's supplied decision note. Broadly bypassing hold_notes would instead expose unrelated vulnerability notes.
* Impact: Coordinator/support resident viewing remains incomplete, or a fix widens unrelated sensitive-field access.
* Smallest useful change: Specify field-aware handling that preserves authorized resident-decision fields independently of vulnerability-reason access, while retaining the existing vulnerability restriction elsewhere.
* Action owner: Planning parent.
* Exact resolving evidence: Core and authenticated HTTP assertions that coordinator and support see the exact supplied resident note/source/wishes/safe-route values allowed by the confirmed matrix while vulnerability and unrelated contact-note canaries remain held when reason access is absent. Repeat with ZF_REASON_ROLES excluding an otherwise authorized resident viewer; unrelated denied roles must not gain resident evidence.
* Decision route: Direct planner correction. Do not ask the owner to reconfirm the matrix or widen vulnerability rights.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Apply overdue authority denial to disclosure checks, not only work gates

* Related IDs: W1, W2, P01-T01, P01-T02.
* Evidence: The plan names overdue decision reliance and expired decisions releasing dependent work. src/core/src/zava_forward/core/resident_decisions.py:_res_disclosure_check calls authority_for directly; authority_for checks authority dates/status/task/context/safe-contact revision but does not call resident_gate. Legal hold can intentionally leave overdue authority records stored.
* Concern: An implementation confined to resident_gate can correctly return contractor Hold and block works, yet still validate an overdue representative's Receive information or Communicate task before deletion or while a legal hold preserves the payload.
* Impact: Retained overdue authority could still be represented as usable authority through an existing human-facing check. Retention preservation must not imply permission to rely on the record.
* Smallest useful change: Explicitly apply the shared first-contact expiry assessment at authority_for/disclosure reliance as well as resident/work gates; legal hold blocks deletion, not expiry. Preserve the documented Unknown-history behavior rather than introducing an unrequested policy.
* Action owner: Planning parent.
* Exact resolving evidence: At the exact five-year anniversary, long-dated representative authority fails disclosure_check and decision reliance before purge, both with and without legal hold; pre-boundary valid authority succeeds; denials do not mutate resident records or create successful disclosure audit events.
* Decision route: Direct planner correction; no new approval workflow or owner choice is needed.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Azure purge evidence must distinguish current rows from retained SQL history

* Related IDs: C3, P02-T01, P02-T03.
* Evidence: src/core/src/zava_forward/core/mssqlstore.py:_create_schema_serialized branches on is_ledger_on; audit is an append-only ledger table in that mode. src/core/README.md, Azure SQL store, explicitly warns that other tables in a ledger database retain row history relevant to retention and erasure.
* Concern: The plan's real Azure SQL purge/restart/audit checks do not distinguish removing resident content from the current case body from eliminating historical database copies. Passing a current-row assertion does not establish physical erasure.
* Impact: Delivery evidence could overstate retention deletion on the actual exercised database, even though this synthetic implementation works correctly.
* Smallest useful change: Record the isolated database's actual ledger/history mode and define the Azure acceptance claim as current-payload deletion with intact audit unless historical erasure is separately evidenced. Document any history limitation in the requested READMEs/evidence; do not add a ledger redesign or change an existing database.
* Action owner: Planning parent.
* Exact resolving evidence: P02 checks record database mode, assert current-row purge after reopening a fresh MssqlStore, and label historical-copy behavior accurately. Cleanup confirms deletion of ama; that exercise teardown is not presented as a reusable operational per-resident erasure mechanism.
* Decision route: Direct planner correction to evidence credibility, not a new owner decision about production erasure.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Existing fixtures need a project-local scratch root for this execution

* Related IDs: P01-T03, P02-T01.
* Evidence: Current execution instructions forbid file operations in /tmp and other temporary directories and require scratch files beneath the working directory. src/core/tests/test_resident_decisions.py and src/api/tests/test_resident_api.py use tempfile.TemporaryDirectory without a supplied dir.
* Concern: The planned unit/application commands inherit the host's default tempfile location unless explicitly redirected. The existing tests can therefore violate this execution boundary before feature assertions run.
* Impact: Required local validation can be rejected or performed outside the permitted filesystem scope; the Azure script may repeat the same mistake.
* Smallest useful change: Specify an absolute project-local scratch root via TMPDIR before starting Python validation processes, keep generated synthetic artifacts there, and remove only that run's scratch output afterward. Apply the same convention to any new Azure verification script; no dependency or tracked configuration change is required.
* Action owner: Planning parent.
* Exact resolving evidence: Validation commands show the project-local TMPDIR setting; a preflight tempfile.gettempdir assertion resolves beneath the worktree; commands/results and cleanup are recorded without generated data being committed.
* Decision route: Direct planner correction complying with the current environment restriction.

## Strengths and Residual Risk

* Calendar-year arithmetic, February 29 handling, withdrawn/expired coverage and an explicit Unknown outcome are preferable to silently inventing a date from a decision.
* Reusing manager-reviewed deletion, legal holds, existing role identities and resident_gate avoids unnecessary architecture expansion.
* The source boundary, JSON/SQL persistence model, loopback HTTP evidence and isolated synthetic Azure database are coherent.
* No confirmed choice is reopened. No additional live model invocation, broad role taxonomy, approval platform, real-resident data, complaints integration or second critique is required.
* Cross-case resident identity, missing historical evidence, human role-holder acceptance and operational legal approval remain declared limitations. The five-year policy is an owner-confirmed exercise choice, not a newly established legal retention requirement.

## Questions or Blocking Evidence Gaps

* No unresolved owner decision is identified within this slice.
* All PC findings are direct planner-owned corrections with bounded implementation evidence. The review is not Blocked merely because local/Azure validation has not yet run.
* Actual Azure availability, signed-in token permissions and deletion success remain execution-time evidence. This critique accepts the supplied authorization and inventory claims without making live Azure calls.

## Limitations

* Assessment is limited to the supplied materials and necessary local code trace. No external research, live tenant/database reads, test execution or legal-source currency check was performed.
* Existing code is evidence of implementation risks, not a claim that the planned changes have already failed tests.
* Plan, details and research sources remain unchanged. Only this critique artifact is written.

## Recommended Next Action

* Highest-impact finding: PC-001, deletion completeness and retained-copy honesty.
* Action owner: Planning parent for PC-001 through PC-006.
* Smallest next action: Revise the existing task details and acceptance assertions to disposition all six findings, starting with the explicit purge inventory; then continue the requested implementation and local-to-Azure validation sequence.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/resident-retention-permissions-plan.md](.copilot-tracking/plans/2026-10-16/resident-retention-permissions-plan.md) | Final candidate assessed |
| [.copilot-tracking/details/2026-10-16/resident-retention-permissions-phase-details.md](.copilot-tracking/details/2026-10-16/resident-retention-permissions-phase-details.md) | Task completion contract assessed |
| [.copilot-tracking/research/2026-10-16/resident-retention-permissions-research.md](.copilot-tracking/research/2026-10-16/resident-retention-permissions-research.md) | Supplied research and confirmed decisions |
| [.copilot-tracking/plans/2026-10-16/resident-retention-permissions-critique.md](.copilot-tracking/plans/2026-10-16/resident-retention-permissions-critique.md) | Complete single critique and finding set |

## Next Steps

The active planning parent should directly disposition PC-001 through PC-006 and finalize the plan without another critique. No user action is required. This critic stops here without implementation or agent dispatch.
