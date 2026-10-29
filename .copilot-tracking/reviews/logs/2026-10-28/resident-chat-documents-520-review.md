---
title: Resident chat documents correction independent RPI Review
description: Original post-implementation review for task 520-documents-correction
ms.date: 2026-10-28
---

## Scope and Evidence

* Task ID: 520-documents-correction / resident-chat-documents-520.
* Review date: 2026-10-28.
* Review scope: Complete current correction diff, including the two untracked core source/test files, against the owner-added issue 520 criterion and PR 525 boundary.
* Plan: .copilot-tracking/plans/2026-10-28/resident-chat-documents-520-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-documents-520-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-28/resident-chat-documents-520-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-28/resident-chat-documents-520-changes.md
* Research: .copilot-tracking/research/2026-10-28/resident-chat-documents-520-research.md

## Opening Review State

* Interpreted review goal: Perform the one original independent post-implementation Review, recording findings without correction or closure verification.
* Review scope: Own-case document questions, grounded rules/facts, deterministic AI-off/unavailable parity, authorization and revocation, SQL projection, typed routing and no-approval boundaries.
* Evidence readiness: Artifact paths and tracked/untracked correction inventory identified; detailed comparison and independent focused validation pending.
* Acceptance basis: Owner criterion requires missing documents, how to provide them and all recorded warnings/errors from only the resident's own case/document metadata, grounded/cited rules and facts, no acceptance/compliant claims and staff referral.
* First comparison boundary: Current plan, details, changes and original critique, followed by complete correction source/test diff.
* Active read-only boundaries: Only this canonical review record may be written. No source, plan, changes, critique, research, state, Azure, secrets, environment files or private datasets.
* Initial blockers: None identified. P03 publication and exact-head gates are explicitly outside this pre-commit Review execution.

## Execution Status

* Execution status: Complete.
* Review execution evidence: One independent Review on 2026-10-28 of the current working-tree correction against HEAD 216e7436, on feat/resident-chat-520. All ten tracked changed files and both untracked source/test files were read, along with the five task artifacts. This is a working-tree assessment, not an exact-head or post-gate assessment.
* Plan execution distinction: P01/P02 implementation and focused validation are recorded complete; P03 remains pending. Complete describes this Review, not publication or full-plan execution.
* Only this record was written. No fixes, second Review, closure verification, nested delegation, commits, rebase, remote writes or heavy gate were performed.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Typed document facts, SQL view/reader, authorized row and mandatory answer | Reconciled as implementation performed | Nested positive-projection defect remains RV-001; completion markers do not establish conformance. |
| P02 / P02-T01 | Semantic core/SQL/API tests, browser assertions, component README | Reconciled as evidence recorded | Eleven added methods across three test files, one new test file, no test removals or dependency changes; within the locked bounds. Nested raw-view privacy coverage is missing as part of RV-001. |
| P03 / P03-T01 | Review followed by commit, authorized rebase, clean exact-head gate and normal push | Correctly pending | This original Review supplies findings, not a future gate pass. No premature completion is inferred. |
| Follow-Up Items | Human/resident/content/AT and real-model acceptance still pending | Reconciled | Distinct original acceptance follow-up, RV-002; not added to P01/P02. |

The changes record's opening implementation-start paragraph is historical opening
state. Its completion and reconciliation sections, plan markers, phase details
and handoff consistently identify P01/P02 complete and P03 pending. No stale
state prevents a credible review boundary.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/resident_documents.py | Immutable bounded requests/documents/issues; deterministic missing/provision/scan/issue explanations | Strict parser and renderer read completely | Five new core methods cover facts, refs, empty/unknown, generated placeholders, scans, malformed/bounded input and inert quoted text | Rules behavior is supported; receipt and clean scan do not approve content. |
| P01-T01 | infra/sql/resident-showcase.sql; src/core/src/zava_forward/core/resident_showcase_sql.py; src/core/src/zava_forward/core/resident_showcase.py | Add documents_json and typed own-case snapshot to existing fixed view/reader | Source scalar-type/length validity checks, explicit invalid markers, strict projected shape and unchanged view-only SELECT | Three new source-through-SQL methods; reported real disposable SQL pass | Broad source invalidity and exact-boundary proof added; nested allowlist guarantee is incomplete, RV-001. |
| P01-T01 | src/core/src/zava_forward/core/resident_assistant.py; src/api/src/zava_forward/api/resident_demo/app.py | Extend mandatory host-owned rules answer using freshly authorized row | Same snapshot feeds CaseProgress; before-answer authorization and after-answer fresh view authorization retained | API parity and inference-time revocation tests | No input-selected case, raw file access, model prose or document action introduced. |
| P01-T01 | src/api/src/zava_forward/api/resident_demo/chat.py | Route document explanations before generic status/send refusal | Safety and injection/other-person refusals still precede document routing | Typed missing/provide/send/error questions and cross-session negative cases | Bounded explanation only; document route cannot send files or select a callback action. |
| P02-T01 | src/core/tests/test_resident_documents.py; src/core/tests/test_resident_showcase_sql.py; src/api/tests/test_resident_chat_api.py | Add constructed semantic, privacy, parity and revocation regressions | Complete added-test diff and new file reviewed | Supplied focused core/API and real SQL outcomes; independent syntax pass | No tests removed; existing raw-view privacy assertion misses nested private fields, RV-001. |
| P02-T01 | src/api/checks/resident_assistant_browser_check.py | Exercise selected/typed document answers, citations, isolation and narrow enlarged-text flow | Real browser assertions, document-facts axe scans and screenshot path in source | Supplied real Chromium/pinned-axe pass; raw external assets not inspected | Engineering evidence only; not human/AT/native-zoom acceptance. |
| P02-T01 | src/api/README.md | Document source contract, limits, fallback/manual route and separate view application | README agrees with intended contract and deployment boundary | Direct documentation/diff review | Private-field projection claim is not fully true until RV-001 is corrected. |

### Behavior and authority assessment

* Requests are explicit own-case metadata, not derived from the staff evidence checklist. A missing request list is unknown; an empty list means no requests recorded. Matching kind requires a nongenerated document and establishes presentation only.
* Every parsed resident issue is quoted, with warning/error labels and a document reference; there is no truncation of valid facts. Pending, infected, mismatch, clean and unknown scan results have distinct text. Generated placeholders do not satisfy request presence. The common conclusion rejects acceptance/compliance inference and refers requirements, flags and a secure provision route to the housing officer.
* Sources contain stable request/document references. They are record citations, not a legal determination or proof that the underlying resident-facing instructions are correct. Current legal rules and scanner/clinical decisions are not extended by this correction.
* AI-off uses document_answer through advise. Existing src/api/src/zava_forward/api/resident_demo/aoai.py constructs the identical rules base first and can append only locally owned guidance selected by ID; unavailable/oversized-payload fallback retains the base and sources. The existing model payload cap is not enlarged and mandatory facts are not shortened to fit it.
* The supplied API parity test checks AI output starts with the entire rules answer and has identical sources; unavailable output equals the rules answer and sources. Scan-code completeness is separately proved in the core table-driven test. The complete base travels through the same path for each code; live-model behavior is not claimed.
* src/api/src/zava_forward/api/resident_demo/app.py accepts only the topic/question plus explicit use_record contract, resolves case identity from the verified session, authorizes before using the row and rechecks after inference. The new revocation test expects 401 without answer after revocation inside the fake transport. Other-session data and header-selected case attempts remain excluded.
* Document routing takes precedence over generic case status and permits how-to-send explanations, while safety, injection and other-person refusals remain ahead of it. Returned action is appointments only for that separate typed route; the document answer explicitly cannot upload or send.
* Existing src/api/src/zava_forward/api/resident_demo/web/assistant.js renders answer and sources via textContent. Quoted issue text is not inserted as HTML or used as an action instruction. No web assets, design system or UI controls changed.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01/P02 source validity | Require original-type/length validation and real source-through-view proof | PC-001; no new user decision required | Plan acceptance, P01/P02 details, source marker and SQL tests added | Original Revise critique preserved and directly disposed, no repeat critique | Substantive original-type proof improved; separate nested-projection defect is RV-001. |
| P01/P02 scan matrix | Enumerate infected/mismatch alongside pending/clean/unknown | PC-002 and canonical doc_controls scan meanings | Plan/details, SCAN_TEXT, table-driven core tests and README agree | Direct correction within confirmed intent | Reconciled; constructed historical/anomalous rows are not a claim about ordinary upload persistence. |
| P03 base contract | Pin reviewed main and explicit --base for run and receipt verification | PC-003; existing owner-authorized publication direction | Details require fetch, reviewed main SHA, moved-main stop/rerun and exact-head checks | Direct correction; publication not executed here | Reconciled as a pending execution contract, not a passed gate. |
| P01/P02 known-empty SQL | Preserve [] rather than normalizing it to unknown | Changes record reports first real SQL failure and subsequent correction | COALESCE empty-array projection, unknown/empty source regression, current completion evidence | Implementation refinement within approved empty/unknown semantics; not material divergence | Justified and recorded; original failed run is not described as passing. |
| P01/P02 environment/lint | Existing pinned external environment and local formatting/type annotation corrections | Missing installed distributions and targeted checks | Changes record names failure, recovery and passing focused results | No manifest, model authority, test contract or user-intent change | No new planning decision needed. |

## Critique and Material Revision Assessment

* PC-001: Disposed in the current plan/details and implemented source-through-real-view test matrix. Wrong-type containers/scalars, oversized values/lists and exact valid limits are assigned to actual SQL, not merely mocked rows. The reported initial empty-list failure and corrected rerun demonstrate the distinction. The additional raw nested-field exposure in RV-001 means the intended positive projection still fails; it does not erase the original critique or disposition.
* PC-002: All four canonical scan states plus unknown/null have distinct deterministic explanations, citations and staff referral. Tests exercise each; normal uploads reject infected/mismatch and rescans remove affected files, so anomalous fixtures do not imply a new persistence route.
* PC-003: P03 details now include reviewed-main --base for --all and current-main --base for --verify-receipt, nonblocking lock and invalidation on identity/base changes. It remains unexecuted at this pre-commit boundary.
* Material revisions: No significant or divergent authority/scope decision was found. Preserving type validity, adding scan distinctions and fixing empty-array semantics directly preserve the accepted plan. No fresh user decision or expanded model authority is implied.
* Dependent-work pause assessment: The original critique was retained and current plan/details record the direct corrections before the implementation handoff. No unresolved significant decision is recorded as bypassed. The Review does not independently reconstruct unrecorded chronological events.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Original human/resident/content/assistive-technology and real-model acceptance | Local synthetic/fake-transport/browser checks do not constitute user or operational acceptance | Parent/owner to arrange named acceptance owners and record actual results in distinct follow-up work | Open, explicitly preserved; RV-002. Not a P01/P02 defect or silent scope extension. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Nested request and issue JSON bypasses the SQL positive projection

* Related scope: P01-T01, P02-T01; named-field projection and private-field exclusion.
* Evidence: infra/sql/resident-showcase.sql:84 copies rq.[value] unchanged into requests; infra/sql/resident-showcase.sql:97 copies iss.[value] unchanged into issues. A request containing the three allowed fields plus staff_notes, or a resident issue containing severity/message plus scanner_detail, therefore carries those extra fields into documents_json. The same applies to a wrong-type object containing arbitrary data. infra/sql/resident-showcase.sql:147 grants the restricted principal SELECT on this view. The document's outer fields are individually projected, but these two nested containers are not.
* Impact: The least-privilege view discloses non-allowlisted metadata to its reader before Python validation. src/core/src/zava_forward/core/resident_documents.py rejects extra keys, so this is not evidence that the HTTP assistant renders them; that later denial does not restore the promised database projection boundary. The README's assertion that staff/scanner details are not projected is too broad. Existing SQL privacy assertions cover document-level private fields, not private keys inside requests or resident_issues.
* Destination: rpi-implement.
* Smallest useful next action: Project only id/kind/how_to_provide and severity/message at the SQL boundary, preserving source type, shape and length invalidity through non-sensitive markers rather than raw containers. Extend the existing source-through-view tests with extra private fields and malformed containers at both nested locations; assert their values are absent from raw restricted-principal SELECT results and malformed facts still fail closed. Keep exact-limit, empty/unknown, grants and parity coverage. No source fix is performed in this Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Original acceptance work remains a distinct follow-up

* Related scope: Plan Follow-Up Items and original issue/PR acceptance boundaries.
* Evidence: Plan Follow-Up Items and changes-record reconciliation explicitly leave human/resident/content/AT and real-model acceptance pending. Browser source uses a constructed row, rules provider, root font-size enlargement and automated axe; API AI coverage uses a fake transport.
* Impact: Engineering results do not prove understandable resident content, assistive-technology use, native browser zoom, actual model/service acceptance or whole-issue approval. This is known, non-blocking residual work for the correction's bounded engineering scope, not an implementation defect.
* Destination: Distinct original-task acceptance follow-up.
* Smallest useful next action: Parent/owner retains the pending acceptance item, assigns the relevant human/technical acceptance owners and records observed results separately before any whole-issue or accessibility acceptance claim.

## Defects

* RV-001 is the implementation defect. No additional source defects are asserted on the supplied evidence.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent implementation owner: enforce nested SQL allowlists and add raw restricted-view privacy regressions | Accepted design already requires positive projection; no new product decision or open-ended research is needed. |
| RV-002 | Distinct original-task acceptance follow-up | Parent/owner: preserve and assign human/resident/content/AT and real-model acceptance | Known residual acceptance work outside P01/P02, not a correction defect. |

These are the single routes for the two findings. Later implementation does not
require this Review to run again. No rpi-plan or rpi-research handoff is needed.

## Residual Work

* RV-002 remains outside active correction implementation and completion claims.
* Source-only view changes require separately authorized application before deployment with the reader. This existing operational dependency is documented, not a new task requirement or evidence of live application.
* No whole-issue closing keywords, model-service success, operational readiness or accessibility conformance can be inferred from this Review.

## Blockers and Remaining Work

* Acceptance blocker: RV-001 prevents acceptance of the correction's promised SQL projection boundary.
* Review-progress blockers: None; the evidence supports this bounded verdict despite not rerunning external suites.
* Remaining active work: Parent owns any later RV-001 implementation. P03 remains pending commit with original dated evidence and privacy-safe identity, authorized remote-topic reconciliation/rebase, final clean candidate, full nonblocking locked gate, fresh receipt verification against fetched main, independent exact-head assessment and normal push. None was run or waived here.
* Preserve original first-pass artifacts, critique Revise verdict, reported failed SQL attempt and this original Review outcome. Do not rewrite these as later successes.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| git diff --check | Complete tracked correction whitespace | Passed, independently executed | No whitespace errors; new Python files separately syntax-parsed. |
| Python ast.parse over changed/new Python files | All ten changed/new Python files | Passed, independently executed | All parse successfully; no bytecode or other files written. This is syntax evidence, not behavior testing. |
| Core focused unittest: test_resident_documents test_resident_assistant test_resident_showcase test_resident_showcase_sql | Core parsing, answers, showcase and SQL renderer | Passed, reported in changes and supplied handoff; not rerun here | 82 tests, 22 opt-in skips. Skips are not SQL integration evidence. |
| API focused unittest: test_resident_chat_api test_resident_assistant_api test_resident_aoai test_resident_demo_api | HTTP authorization, routing, parity, fallback and revocation | Passed, reported; not rerun here | 70 tests, no skips. Fake advisor, no actual Azure/model call. |
| Actual disposable-loopback SQL execution | All showcase SQL methods including source-through-view | Passed, reported; not rerun here | 32 tests, no skips after known-empty source-view correction. First harness interpreter failure and first SQL empty-list failure remain historical failures. No SQL/container/heavy gate launched by reviewer. |
| checks.resident_assistant_browser_check with pinned axe | Actual Chromium, selected/typed document facts/citations, isolation and long-answer reflow | Passed, reported; raw report/screenshots not independently inspected | Supplied external final-browser run exit 0. Source assertions inspected. 320 CSS px/200% root text and reduced-motion checks are not native zoom or human/AT acceptance. |
| Targeted Ruff/check-format line length 100; core/API mypy | Changed code and core/API typing | Passed, reported; not rerun here | Core 156 files; API 94 files. No claim of an independently rerun full suite. |
| Fresh Web Interface Guidelines source retrieval | Changed browser-check/web-facing answer boundary only | Passed | Current source fetched on 2026-10-28; changed browser check read against applicable content, focus, semantic, reflow and empty-state rules. No HTML/CSS/JS asset change; no unrelated UI audit. Repository plain ASCII/Fluent conventions take precedence over generic typographic preferences. |
| System Python package availability probe | Feasibility of in-place focused unittest rerun | Unavailable | zava_forward is not installed in system Python. No dependency installation or alternative environment mutation was performed; supplied external-venv runs remain reported evidence. |
| Full local gate, receipt verification, exact-head assessment | Committed final publication candidate | Skipped as explicitly pending | Pre-commit Review is before P03 publication. Running a heavy gate/SQL was prohibited by the supplied review boundary. |
| Human/resident/content/AT/native zoom and real-model acceptance | Original issue acceptance | Not run | Distinct follow-up RV-002; no synthetic result is substituted. |

### Web guideline reporting

* src/api/checks/resident_assistant_browser_check.py: passes the applicable changed-file review; no separate UI-rule defect identified. New checks exercise typed/selected content, empty/unknown state isolation and reachable citations with enlarged text.
* Raw external browser report and screenshots were not opened, so there is no independent visual or raw-axe-results verification claim. The passed-browser statement is supplied implementation evidence only.

## Outcome

* Outcome: Not accepted.
* Severity summary: 0 Critical, 1 High, 0 Medium, 1 Low residual follow-up.
* Outcome rationale: Most bounded document-answer behavior, parity, own-case authorization, no-approval wording and critique reconciliation are supported. Nevertheless, the SQL view's raw nested container copies contradict the accepted positive projection and private-field exclusion requirements. Passing existing tests does not establish that missing boundary. RV-001 is sufficient to block correction acceptance; RV-002 separately preserves original acceptance work.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | RV-001 route recorded above | Parent implementation owner continues the accepted projection contract. |
| Decision gap or invalid assumption | None | No significant/divergent user decision required. |
| Material evidence gap | None requiring research | Supplied focused evidence is distinguished from independently executed checks; external/browser and exact-head limitations are explicit. |
| Non-blocking residual work | RV-002 distinct follow-up recorded above | Original acceptance owner/parent, outside active correction scope. |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: Complete supplied diff/artifact comparison; independently passed whitespace and ten-file Python syntax checks; reported core/API/SQL/browser/lint/type outcomes reviewed with the limits above.
* Blockers: RV-001 blocks acceptance. P03 gate and publication remain pending, without substitute approval.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/resident-chat-documents-520-research.md](.copilot-tracking/research/2026-10-28/resident-chat-documents-520-research.md) | Correction research and source/authority decisions. |
| [.copilot-tracking/plans/2026-10-28/resident-chat-documents-520-plan.md](.copilot-tracking/plans/2026-10-28/resident-chat-documents-520-plan.md) | Current requirements, markers, critique dispositions and follow-up. |
| [.copilot-tracking/details/2026-10-28/resident-chat-documents-520-phase-details.md](.copilot-tracking/details/2026-10-28/resident-chat-documents-520-phase-details.md) | Execution contract and pending publication controls. |
| [.copilot-tracking/reviews/plans/2026-10-28/resident-chat-documents-520-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/resident-chat-documents-520-plan-critique.md) | Preserved original Complete / Revise critique. |
| [.copilot-tracking/changes/2026-10-28/resident-chat-documents-520-changes.md](.copilot-tracking/changes/2026-10-28/resident-chat-documents-520-changes.md) | Implementation history and reported validation. |
| [.copilot-tracking/reviews/logs/2026-10-28/resident-chat-documents-520-review.md](.copilot-tracking/reviews/logs/2026-10-28/resident-chat-documents-520-review.md) | This single original independent Review. |

## Next Steps

Return this one Review to the active parent. The parent owns later rpi-implement
continuation for RV-001 and the distinct RV-002 acceptance follow-up, while
preserving P03 as pending until its actual committed-candidate gates execute.
No second Review, source fix, closure verification or user action is performed
by this reviewer.
