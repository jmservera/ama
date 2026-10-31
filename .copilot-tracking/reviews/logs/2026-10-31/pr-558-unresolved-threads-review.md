---
title: Independent RPI Review - PR 558 unresolved threads
description: Original independent review of the source-binding correction and qualified delivery evidence
ms.date: 2026-10-31
---

## Scope and Evidence

* Task ID: pr-558-unresolved-threads-2026-10-31.
* Review scope: one original independent Review of the complete supplied source boundary.
* Observed HEAD: ed888a91f6da20165f84ddf220386f103721635d.
* Observed origin/main: 368d3bb8d0a9ad2dc221be6cf108b5cf2a8fa7cd.
* Branch: tmp/fabric-558-merge.
* Evidence: supplied research, plan, phase details, critique, changes, unstaged source/docs, new Test-SourceHashes.ps1, prepared external PR body and external validation evidence.

## Opening Review State

* Interpreted review goal: compare the four LF-normalized text hashes, actual delivered-deck verification and receipt refresh against owner intent, inherited guard behavior, critique dispositions and explicit disclosure boundaries.
* Review scope: complete task source boundary; publication and complete local gate remain later parent-owned actions.
* Evidence readiness: supplied artifact paths and external evidence identified; working tree/source boundary and actual origin/main confirmed. Detailed evidence comparison is pending.
* Acceptance basis: supplied owner scope, current artifact acceptance criteria and critique dispositions; no native Windows, hosted execution, UI conformance or publication approval may be inferred.
* First comparison boundary: current plan/details/research/changes and critique against the complete unstaged source/docs and new regression test.
* Active read-only boundaries: only this canonical review record may be written; all other files are evidence-only. No remote mutation, source fixes, second Review, automatic rebase or merge.
* Initial blockers: none established for source review. Complete gate, commit, publication and thread operations are explicitly pending.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one original independent comparison on 2026-10-31 of the complete supplied source boundary and all named artifacts. No nested reviewers, second Review or source corrections.
* Implementation execution state: P01 complete; P02 partially prepared and still unchecked. Review completion does not mean the complete implementation/publication plan executed.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Canonical source helper and one regression script | Reconciled | Exactly four textual calls changed; no binary/media or deck edits. |
| P01-T02 | Actual Verify, receipt refresh, native checks, runner tests, guide/index/log | Reconciled | External logs and independent current-byte bindings support completion. |
| P02-T01 | External PR body prepared; original Review and commit pending | Reconciled for this handoff | This record supplies the original Review only; commit remains parent-owned. |
| P02-T02 | Complete gate, exact-head assessment, normal push and thread operations pending | Reconciled | No passing final gate or publication is claimed. Actual current main is used, not older PR base metadata. |
| Follow-Up Items | Windows 5.1/Office and direct human acceptance unavailable | Reconciled | Explicit separate environment-dependent acceptance; RV-001. |
| Plan Handoff and changes Validation Record | Older next-step/future-tense prose survives alongside current completion sections | Minor inconsistency | Markers, Pre-Review Reconciliation and detailed completion evidence establish current state; RV-002. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | tools/capstone/Invoke-Capstone.ps1 | Added Get-CanonicalSourceHash and replaced manifest/catalog/builder/native-helper hashing only | Complete unstaged diff and owning verifier read | Semantic log and independent current-byte recomputation | Conformant: strict UTF-8 decoding retains U+FEFF; re-encoding preserves valid UTF-8 bytes apart from CRLF/CR replacement. Get-ByteHash remains the existing SHA-256 helper. |
| P01-T01 | tools/capstone/Test-SourceHashes.ps1 | One owning-helper regression, with semantic-only and post-refresh modes | Entire new script read | Semantic and default-mode logs | Conformant: LF/CRLF/lone CR equivalence; space, case, final newline and BOM significance; empty input and invalid UTF-8 refusal; four source bindings, convention and exact delivery binding. Only its GUID-owned fixture is cleaned. |
| P01-T02 | tools/cowork-native-recovery/Invoke-StoryReview.ps1; tools/capstone/Test-NativeShapes.ps1 | Retained inherited finite correction instead of redundant edits | All four guards and all 32 test assertions read; aedc6713 ancestry confirmed | External 32-check success | Conformant: geometry, pie, polygon and outline use IsNaN/IsInfinity; no IsFinite call remains in the shared helper. Windows compatibility is source-level plus portable execution, not direct Windows acceptance. |
| P01-T02 | docs/capstone/source/validation.json | Refreshed source verification and builder binding after delivered-package Verify | External successful report; all shared package fields independently equal receipt fields | Report SHA, four current source hashes, all receipt tool hashes and exact delivery bytes checked | Conformant: historical preview/native fields remain unchanged and explicitly qualified; publication_gate_passed remains false. |
| P01-T02 | docs/capstone/source/README.md; docs/reference/README.md; docs/reference/log.md | Documented normalized source contract, test sequence and qualified durable evidence | Complete changed prose, existing guide context and append-only diff | Markdown/diff review; git diff --check | Conformant: no unnecessary global attributes rule; exact binary/media bindings preserved; log appended rather than rewritten. |
| P02-T01 | External prepared files/pr558-body.md | Disclosed January authority, SQL renewal, assistant/UI and hosted execution | Complete external body read; owning policy/SQL/workflow and existing API guide checked | Historical run and exact browser success independently retrieved read-only | Conformant preparation, not applied PR body. No closing reference syntax found. No new current-task UI change or fresh UI conformance claim. |

The verifier computes the expected revision from the pinned template, manifest and media, compares every candidate package member and bytes, checks notes/timing/navigation/protected cost content, and only then emits canonical source hashes. Verify does not invoke Build. The external verified PPTX equals both current working delivery and HEAD delivery byte-for-byte. This is actual source-to-delivery verification, not substituting four digests or validating a freshly built replacement.

Strict UTF-8 decode/re-encode is justified here: valid UTF-8 has a unique byte encoding for the represented code points, the decoder rejects invalid sequences, and it does not strip the BOM. Normalization changes only CRLF and remaining CR. Binary delivery/template/media hashing paths remain unchanged.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 | Separated semantic tests from receipt assertions | PC-002 identified necessarily stale builder hash before refresh | Plan/details require semantic/native checks, actual Verify, receipt refresh, then default bindings; changes/logs match | Original critique preserved; direct compatible correction | Applied and supported; no divergent owner decision needed. |
| P01-T02 | Selected immutable Microsoft runtime, preflight and isolated execution | PC-003 identified missing runtime provenance | Plan/details, receipt and changes identify digest; PowerShell log records 7.4.6; local Docker inspect independently confirms the exact immutable image | Original critique preserved; compatible Docker implementation | Applied. Isolation/UID/mount settings are documented requirements and supplied execution attestations, not independently reconstructed argv from the abbreviated logs. |
| P02-T02 | Rejected worker-only blanket path constraint without altering runner | PC-001 imported its own execution restriction; supplied parent context expressly retains the shared lock | Disposition appears in plan, details, changes and session state; src/README.md and tools/rpi-checks.py confirm actual shared lock contract | Original adverse critique and Revise verdict preserved | Justified divergence; do not promote this review worker's restrictions into parent authority. No wrapper, skip, lock relocation or protection change is authorized. |
| P01/P02 | Marked verified source complete and publication pending | Actual verification logs, external body and fetched-main divergence | Phase checklist/details/changes/state consistently separate source completion from later publication, apart from RV-002 prose | No scope expansion or unresolved significant decision | Ready for source Review; future publication remains conditional. |

## Critique and Material Revision Assessment

* PC-001: rejection is correct for the supplied parent boundary. The critique's claimed blanket prohibition is worker-specific, while the parent repository deliberately specifies the unchanged shared lock. This reviewer does not execute the lock-using gate or import its own execution restrictions as parent authorization. All real publication gates remain intact.
* PC-002: applied correctly. The first log shows semantics, 32 native checks and actual Verify; the separate default-mode log shows semantics and four receipt bindings afterward. Current report/receipt/source equality independently corroborates the refresh result. The builder changed to 4c168289a7352017e6c9cb9456fe9fe1436e8ad38ca3721268366c85492829d4.
* PC-003: immutable image and actual version are evidenced, not merely a mutable tag or historical runtime claim. Digest is mcr.microsoft.com/powershell@sha256:62300a213a9293916333df2b014cd3a8f22fb0b0b65f2bb446aaf436bcf8c868; recorded runtime is 7.4.6. Full Docker invocation/exit metadata is not present in the supplied abbreviated log files; documented read-only/no-network/owned-output settings are accepted as supplied execution evidence, with that inspection limit disclosed.
* Material revisions: no unapproved source scope, runtime authority, SQL/UI implementation or deck changes were introduced. Test sequencing and runtime provenance refine the accepted direction. Rejecting a non-applicable constraint does not grant permission to bypass any genuine parent control.
* Dependent-work pause: source completion is supported; P02 publication has not prematurely resumed. Neither this Review nor the original critique is repeated.
* Original critique count: one. Original critique remains unchanged, including PC-001 and Revise; no historical adverse outcome is relabelled successful.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Direct Windows PowerShell 5.1/Office acceptance | Current Linux/container environment cannot establish native platform or human acceptance | Owner/native Windows validation environment | Open distinct follow-up; RV-001. It is not a source defect or active P01 acceptance criterion. |

The changes record mirrors this follow-up. Direct accessibility/human checks, live deployment, live SQL migration and resident acceptance also remain unestablished; the prepared body appropriately avoids claiming them.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Native platform and human acceptance remain a distinct open follow-up

* Related scope: plan Follow-Up Items; P01-T02 validation boundary.
* Evidence: docs/capstone/source/validation.json explicitly records current native execution false, historical native current-candidate validation false and human acceptance false; external powershell.log reports Linux PowerShell 7.4.6; plan/details/changes and prepared body retain Windows 5.1/Office limitations.
* Impact: portable guard success and delivered-package verification cannot be promoted to Windows PowerShell 5.1, PowerPoint, direct accessibility or human acceptance.
* Destination: distinct follow-up - native Windows/Office and direct human acceptance.
* Smallest useful next action: owner arranges the appropriate native environment and qualified human checks when that acceptance is needed; retain the existing unperformed status until actual evidence exists. This does not block the bounded source correction or require another Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Obsolete handoff prose should not misdirect parent continuation

* Related scope: plan Handoff; changes Validation Record versus Completed Work and Pre-Review Reconciliation.
* Evidence: .copilot-tracking/plans/2026-10-31/pr-558-unresolved-threads-plan.md still says "Next: P01 after critique dispositions" although P01 markers are checked. .copilot-tracking/changes/2026-10-31/pr-558-unresolved-threads-changes.md still says container execution "will be isolated" although Completed Work and logs record successful execution.
* Impact: an agent reading only those older summaries could restart completed verification or mistake completed evidence for a planned check. This is a minor handoff inconsistency, not stale evidence preventing a credible verdict: current markers/details/Pre-Review Reconciliation and actual logs resolve the state.
* Destination: distinct follow-up - parent handoff/state synchronization during P02-T01 continuation.
* Smallest useful next action: use P02-T01 as the next active marker; reconcile superseded next-step/future-tense prose in the normal parent-owned pre-commit evidence update while preserving historical critique/results. No source repair, new Review, separate implementation scope or gate bypass is needed.

## Defects

* None found in the supplied changed source boundary.
* No significant unaccepted decision gap or material missing source-binding evidence was identified.
* Severity summary: 0 Critical, 0 High, 0 Medium, 2 Low residual findings.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct native acceptance follow-up | Owner and native Windows/human validation environment | Environment-dependent acceptance outside immediate source scope. |
| RV-002 | Distinct parent handoff synchronization follow-up | Parent continuing P02-T01 before commit | Non-blocking superseded prose; current completed evidence is credible. |

Later handling of routed findings does not require another Review.

## Residual Work

* RV-001 and RV-002 remain explicitly routed, not converted into source defects.
* P02 is remaining active planned work, not a new residual feature or an implicitly approved publication. Parent owns evidence reconciliation, authenticated privacy-safe commit with trailer, full gate, receipt verification, independent exact-head assessment and permitted normal push/body/reply/resolution operations.
* The prepared body contains the four required disclosure categories and no closing references. Applying it and proving the three thread resolutions are future operations, not completed evidence.

## Blockers and Remaining Work

* Source-review blockers: none.
* Publication prerequisites remain unmet: candidate is uncommitted/dirty with untracked original evidence; no final complete local gate or final receipt exists for the later committed head; no independent exact-head assessment or current-head hosted approval is established.
* Actual origin/main is 368d3bb8d0a9ad2dc221be6cf108b5cf2a8fa7cd; merge base is 5666bd33e1827670e5c07e3e3063bbbe989b59d3; current main is not an ancestor of HEAD. This is a disclosed ancestry boundary, not permission to merge, rebase or rewrite. The unchanged source gate may assess current main; reconcile any actual integration problem only under owner authority.
* Fetch main again before the future final verification. Commit original Review and dated evidence before running the complete external gate. Any later commit, correction, rebase, base movement or changed source/tool/image/dirty/untracked/ignored input invalidates that receipt.
* Gate failures, foreign-lock contention, missing SQL/browser/scanner prerequisites or stale receipt verification block publication without cloud fallback, skip tokens, fabricated status or protection changes.
* Complete gate is deliberately not executed by this Review: the supplied owner boundary requires it after original Review and commit, and this stage permits only the canonical record write.

## Validation Evidence

External evidence root (supplied, outside workspace): /home/azureuser/.copilot/session-state/3f277200-3588-49c9-90f5-ce212f05d397/files/pr558-validation-zurEhA.
External prepared body: /home/azureuser/.copilot/session-state/3f277200-3588-49c9-90f5-ce212f05d397/files/pr558-body.md.
These paths locate external evidence; they are not committed receipts or workspace-relative source artifacts.

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Supplied powershell.log | Semantic fixtures, native guards, actual delivered-deck Verify | Passed; inspected | Version 7.4.6; semantics passed; 32 checks passed; Verify passed 54 slides/notes/assets/navigation/timing/protected cost content. |
| Supplied receipt-bindings.log | Post-refresh regression | Passed; inspected | Four canonical source bindings, convention and exact delivered hash passed. |
| Supplied rpi-unit.log; python3 -m unittest discover -s tools -p 'test_rpi_checks.py' -q | Requested runner tests | Passed; inspected | Ran 37 tests, OK. Negative-fixture failures/skips/timeouts are intentional unit-test evidence, not actual gate failures or an executed complete gate. |
| python3 -B read-only assertions in this Review | Current source/report/receipt/delivery/tool bindings | Passed; independently executed | All shared package fields match report; four current canonical digests match; every receipt tool hash matches; delivery equals HEAD and external verified copy; report SHA matches. |
| git diff --check; git ls-files --eol | Changed prose/source and four source input line endings | Passed; independently executed | No whitespace errors; index/working inputs LF with root LF policy. |
| docker image inspect immutable digest | Local runtime provenance | Passed; independently executed read-only | Exact Microsoft digest exists locally. No container execution was repeated by this Review. |
| gh api historical run and API job log | Prepared body's hosted execution assertion | Passed; independently retrieved read-only | Run 41189834160 succeeded at 3e2a751958699cb422fc787adecad948b2f38728; src-api job 124504185383 succeeded. Exact selector was skipped during discovery at 09:44:33, invoked with ZF_BROWSER_TESTS=1 at 09:49:26 and reported "... ok" at 09:51:07. |
| Native Windows 5.1/PowerPoint and human acceptance | Separate acceptance boundary | Unavailable/unperformed | Linux portable execution is not native or human acceptance; RV-001. |
| Fresh standalone UI/accessibility review | Current task | Not applicable | No changed UI files in this task; inherited disclosure was checked against owning guide/workflow, not presented as new UI conformance. |
| Complete --all local gate and final --verify-receipt | Future committed exact head/current-main publication | Not run here; pending | Required after original Review and parent commit; no current success inferred from focused tests or historical CI. |

* Verified report SHA-256: f5f2e2b19e727d91267de273d7d781a8ad89a0dafcc044be3333177881f3e0d3.
* Exact unchanged delivery SHA-256: 4c57e17a8b71e30df787d2fa06e769c45be24f1645a2b5d26dc9e36effdfd8a3.
* Verified builder canonical SHA-256: 4c168289a7352017e6c9cb9456fe9fe1436e8ad38ca3721268366c85492829d4.
* Read-only scope maintained: no test fixtures, generated outputs, source/artifact corrections, remote mutation or publication operations were created by this Review.

## Outcome

* Outcome: Conformant with justified divergence.
* Outcome rationale: the complete supplied source correction and prepared disclosure meet their bounded acceptance basis; PC-001 rejection correctly preserves parent authority and the unchanged real gate. PC-002/003 refinements are reconciled and current source-to-delivery bindings are independently verified. Two Low residual findings do not constitute source defects.
* This verdict is limited to reviewed source/preparation. Whole-plan P02 completion, publication permission, exact-head acceptance and hosted/native/human approvals remain unproven future conditions. It is not approval to push.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No source repair identified. |
| Decision gap or invalid assumption | None | PC-001 disposition justified; do not import worker authority. |
| Material evidence gap | None for current source binding | Full invocation metadata was not independently reconstructed; supplied isolation attestations are explicitly qualified. |
| Non-blocking residual work | RV-001 native acceptance; RV-002 handoff synchronization | Owner/native environment; parent P02-T01 continuation. |

* Execution status: Complete for this one Review; implementation plan Partial because P02 remains pending.
* Outcome: Conformant with justified divergence for the supplied source boundary.
* Validation coverage: supplied semantic/native/actual Verify/post-refresh/37-unit evidence inspected; current bindings/report/delivery/tool hashes and historical hosted browser execution independently verified read-only.
* Blockers: none for source Review; unmet commit/full-gate/current-base verification/exact-head/hosted conditions prevent publication claims.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/pr-558-unresolved-threads-research.md](.copilot-tracking/research/2026-10-31/pr-558-unresolved-threads-research.md) | Research boundary and C1-C7/W1 evidence |
| [.copilot-tracking/plans/2026-10-31/pr-558-unresolved-threads-plan.md](.copilot-tracking/plans/2026-10-31/pr-558-unresolved-threads-plan.md) | Current scope, criteria, dispositions and pending publication |
| [.copilot-tracking/details/2026-10-31/pr-558-unresolved-threads-phase-details.md](.copilot-tracking/details/2026-10-31/pr-558-unresolved-threads-phase-details.md) | Source verification sequence and later gate procedure |
| [.copilot-tracking/reviews/plans/2026-10-31/pr-558-unresolved-threads-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/pr-558-unresolved-threads-plan-critique.md) | Unchanged original critique |
| [.copilot-tracking/changes/2026-10-31/pr-558-unresolved-threads-changes.md](.copilot-tracking/changes/2026-10-31/pr-558-unresolved-threads-changes.md) | Completed source evidence and open publication |
| [tools/capstone/Invoke-Capstone.ps1](tools/capstone/Invoke-Capstone.ps1) | Owning verifier and four normalized hashes |
| [tools/capstone/Test-SourceHashes.ps1](tools/capstone/Test-SourceHashes.ps1) | New semantics and post-refresh binding regression |
| [tools/capstone/Test-NativeShapes.ps1](tools/capstone/Test-NativeShapes.ps1) | Existing 32 native guard checks |
| [tools/cowork-native-recovery/Invoke-StoryReview.ps1](tools/cowork-native-recovery/Invoke-StoryReview.ps1) | Inherited four compatible finite guards |
| [docs/capstone/source/README.md](docs/capstone/source/README.md) | Source contract and documented test sequence |
| [docs/capstone/source/validation.json](docs/capstone/source/validation.json) | Refreshed report-bound receipt and preserved limitations |
| [docs/reference/README.md](docs/reference/README.md) | Related index clarification |
| [docs/reference/log.md](docs/reference/log.md) | Append-only durable evidence entry |
| [src/README.md](src/README.md) | Unchanged complete local publication gate |
| [.copilot-tracking/reviews/logs/2026-10-31/pr-558-unresolved-threads-review.md](.copilot-tracking/reviews/logs/2026-10-31/pr-558-unresolved-threads-review.md) | This task's one original independent Review |

## Next Steps

Parent: continue P02-T01, reconcile RV-002 handoff prose in the normal pre-commit evidence update and commit implementation plus dated original evidence and this Review. Then execute the unchanged complete external gate against fetched current main, verify the external receipt immediately before independent exact-head assessment and permitted normal publication. Preserve RV-001 as the separate native acceptance follow-up. Do not repeat this Review, silently merge/rebase, claim pending thread operations complete or substitute historical CI for the final gate.
