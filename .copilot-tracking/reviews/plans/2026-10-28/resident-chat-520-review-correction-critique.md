---
title: Resident chat review correction final-candidate plan critique
ms.date: 2026-10-28
---

## Metadata

* Task ID: 520-review-correction
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/resident-chat-520-review-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-520-review-correction-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Fixed requirements: server-bound per-login identity and record-use permission across tabs; punctuation-safe morning/afternoon selection; visible manual retry/loading focus; preservation of typed-ahead drafts; no automatic search or focus theft from dismissed delayed appointment answers.
* Supplied evidence: the plan, phase details and .copilot-tracking/research/2026-10-28/resident-chat-520-review-correction-research.md, including C1-C7 and the parent's reported five PR #525 findings.
* Bounded source verification: src/api/src/zava_forward/api/resident_demo/app.py, src/api/src/zava_forward/api/resident_demo/chat.py, src/api/src/zava_forward/api/resident_demo/web/demo.js, src/api/src/zava_forward/api/resident_demo/web/assistant.js, src/core/src/zava_forward/core/resident_showcase.py, src/api/tests/test_resident_chat_api.py, src/api/tests/test_resident_demo_api.py and src/api/checks/resident_assistant_browser_check.py.
* Context: original case study, addendum, reference index, memory, sector primer and src/README.md publication guidance. No legal-currentness assessment was needed.
* Constraints assessed: continue PR #525 on feat/resident-chat-520; canonical HTTP/client and browser/axe ownership; no removals; at most eight added unit methods; extend the existing harness; no resident-authority expansion, Azure, secrets, .env or private datasets.
* Dependencies and acceptance: P01 protocol/UI correction precedes P02 regression evidence; original independent implementation Review and committed evidence precede the exact-head complete gate and publication. Current-main receipt verification, independent exact-head assessment and normal topic push remain separate requirements.
* Boundary: assess implementation readiness, not whether the unimplemented candidate passes. No new research, external source retrieval, agent dispatch, test execution or source modification was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Per-login binding; C1-C4; P01-T01 | Partial | Verified cookie plus opaque sid and response fencing are appropriate; notification and session-establishment races lack a defined contract, PC-001. |
| Strict server validation; P01-T01; P02-T01 | Partial | Missing/wrong/old sid cases are planned; malformed and ambiguous headers are not, PC-002. |
| Punctuation periods; C5; P01-T01; P02-T01/T02 | Covered | Shared word-token semantics and actual morning/afternoon HTTP/browser offered-slot assertions are specified. |
| Manual retry/loading focus; P01-T02; P02-T02 | Covered | Visible callback/sign-in/retry selection with launcher fallback and explicit focus assertions. |
| Typed-ahead draft; P01-T02; P02-T02 | Covered | Compare original untrimmed submission on success; preserve subsequent input and failures. |
| Dismissed delayed appointments; P01-T02; P02-T02 | Covered | Current-generation and open-panel checks precede automatic search/focus; both Escape and outside-focus dismissal are exercised. |
| Resident authority and consent | Covered | Sid is not an identity selector or credential; explicit record-use and specific booking/cancellation confirmation remain; withdrawal does not cancel accepted reservations. |
| Canonical tests and budget; C7; P02 | Covered | Existing Client and actual Chromium/pinned-axe harness are retained, no removals, maximum eight added unit methods. Findings can be covered with parameterized cases and existing browser scenarios. |
| Validation environment; P02-T03 | Partial | Explicit temporary-directory venv conflicts with execution constraints, PC-003. |
| Original Review, exact-head gate and publication; P03 | Covered | Original adverse outcomes retained; current-base clean committed gate, external receipt, independent assessment and ordinary push required. Lock-admission retry is bounded and distinguished from failed checks. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: All five requested corrections have credible implementation and regression ownership. Three direct planning corrections are required: complete the asynchronous identity-transition contract, specify strict malformed-header denial, and remove the prohibited validation environment. No significant or divergent user decision is necessary.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Session notifications and session-establishing replies need an explicit race contract

* Related IDs: C1-C4, P01-T01, P02-T02, per-login binding acceptance criterion.
* Evidence: .copilot-tracking/details/2026-10-28/resident-chat-520-review-correction-phase-details.md:12-24 specifies clearing on broadcasts and fencing view/assistant replies; :47-51 tests A-then-B login and held view/chat responses. src/api/src/zava_forward/api/resident_demo/web/demo.js currently establishes state through start/session and login callbacks as well as loadView, with additional logout success/failure continuations.
* Concern: The proposed generation fence explicitly covers protected replies but does not define whether pending session/login/logout continuations may subsequently restore or clear state. Nor does it define handling of delayed or reordered cross-tab login/logout notifications. An older login notification can arrive after a newer local login; blindly clearing every notification then discards the valid current session. Conversely, an old session response or error continuation can run after reset and restore stale state or erase newly established state. These are missing planning guarantees, not claims that a proposed implementation already has these bugs.
* Impact: Ordinary rapid sign-ins or delayed messages can produce stale session adoption, lost current permissions/state, or unusable sign-in loops despite correctly rejecting mismatched protected requests.
* Smallest useful change: Define one tab identity-transition generation covering session discovery, login, logout, protected responses and failure continuations. Specify notification handling that invalidates stale state without treating message arrival order as authoritative login order; payloads must contain no personal facts, cannot grant permission and cannot select resident identity. Revalidation, if used, must be fenced and must not silently carry record-use permission into another login. State how delayed notifications after a newer local login are handled.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T01 and P02-T02 defining those transitions and adding deterministic scenarios in src/api/checks/resident_assistant_browser_check.py for a held session response across login/reset, a stale failure/logout continuation after a newer transition, and delayed notification delivery after a newer login. Assertions must show no stale repaint or permission restoration, no inappropriate loss of the current login, and continued same-CSRF pre-opened sign-in usability. Preserve the existing A/B and same-resident re-login scenarios and pinned axe coverage.
* Decision route: Direct planner correction. The fixed user requirement already selects per-login binding; no new identity provider, credential, authority or user choice is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The sid header requires strict shape and multiplicity validation before comparison

* Related IDs: C1-C2, P01-T01, P02-T01, strict server validation.
* Evidence: .copilot-tracking/details/2026-10-28/resident-chat-520-review-correction-phase-details.md:12-14 calls for constant-time comparison; :39-42 lists missing/wrong/old sid tests. src/core/src/zava_forward/core/resident_showcase.py issues sid with secrets.token_hex(8). src/api/src/zava_forward/api/resident_demo/app.py uses HTTP header access and converts unexpected dispatch exceptions into 503.
* Concern: The plan does not specify a single canonical header value or malformed-input handling. Passing a non-ASCII header string directly to Python's string compare_digest raises TypeError rather than producing a clean mismatch; accepting only one value from repeated headers also leaves the new binding contract ambiguous. Existing negative cases do not explicitly cover either condition.
* Impact: Attacker-controlled malformed input can become a server-error path instead of deterministic authentication denial, or receive inconsistent interpretation across request handling.
* Smallest useful change: Require exactly one X-Resident-Session header with the codec-issued sid shape, reject malformed/duplicate/comma-joined values before comparison, and return a documented denial without personal reads, model invocation or agenda mutation. Retain cookie verification as authentication and retain existing CSRF, exact request-shape, use_record-is-True and specific-action confirmation checks.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 states canonical validation and denial behavior; P02-T01 parameterizes missing, empty, wrong-length, non-hex, non-ASCII, duplicate and joined headers alongside stale/correct sid cases in the owning HTTP tests. Assertions cover view, assistant and agenda rejection with no personal reader/provider/agenda effects and no 500/503 fallback. The full valid sid still cannot authenticate without a verified cookie. Fit cases into existing or at most eight added unit methods, extending Client only as needed for real repeated-header requests.
* Decision route: Direct planner correction. This tightens validation of the selected binding, without changing resident authority or the core codec.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The named validation venv is prohibited by the execution boundary

* Related IDs: P02-T03, P03-T02, validation contract.
* Evidence: .copilot-tracking/plans/2026-10-28/resident-chat-520-review-correction-plan.md:99 explicitly selects a venv under the system temporary directory. Current execution instructions prohibit any file operations in temporary directories, not just creating a new scratch directory there.
* Concern: The named interpreter/packages cannot be used under this boundary. Existing test and browser fixtures also use tempfile helpers, so removing the explicit venv path alone does not ensure compliant validation.
* Impact: The implementer cannot execute the planned targeted checks and complete gate as written without violating the environment constraint.
* Smallest useful change: Replace the forbidden venv selection with an approved non-temporary environment, without copying or inspecting the prohibited directory. Specify a task-owned project-relative scratch root and configure temporary-file creation there for existing fixtures and child processes; keep authoritative reports/receipts outside the candidate checkout in an approved non-temporary location. Preserve package pins, missing-dependency installation rules, retention controls and clean-candidate gate requirements.
* Action owner: Planning parent.
* Exact resolving evidence: Updated validation contract records the approved interpreter and scratch/output placement, makes temporary-file placement explicit before Python/browser startup, and separates scratch from clean final-gate inputs. If no compliant environment is available, record the affected validation/publication as blocked rather than claiming success or using a forbidden fallback.
* Decision route: Direct planner correction; user response is not required to comply with the existing execution constraint.

## Strengths and Residual Risk

* Reusing the verified random per-login sid avoids core schema/codec changes and does not expose a signed session cookie.
* Both server binding and client generation fences are required; notification-only and CSRF-rotation-only alternatives are explicitly rejected.
* The five UI corrections remain bounded behavior changes with native controls, manual routes, synthetic proposals and resident confirmation retained.
* The test contract preserves existing coverage and actual HTTP/browser evidence rather than substituting mocked DOM checks or a new harness.
* Deferred human, assistive-technology, native-zoom and real-model acceptance remain explicitly unmet; engineering and axe results must not be presented as those acceptances.

## Questions or Blocking Evidence Gaps

* None requiring a user decision. PC-001 and PC-002 require specific planner-owned contracts, not another research cycle.
* A compliant validation environment must be identified under PC-003 before execution; its availability was not tested during this critique.

## Limitations

* The exact five remote review threads were represented by the supplied requirements and research; no remote thread or PR state was reread.
* Source was inspected only to substantiate the bounded planning concerns. No implementation result, executable validation, browser/axe outcome, gate receipt or publication readiness is asserted.
* Existing untracked plan/research/state inputs were left unchanged. Only this critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise P01-T01/P02-T02 to define and exercise the complete identity-transition and notification-race contract; incorporate PC-002 and PC-003 in the same direct revision.
* User response required: No.
* Handoff: Preserve this original Revise verdict and disposition all three findings with exact resolving evidence. Finalize directly after correction; do not dispatch another critique.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/resident-chat-520-review-correction-plan.md](.copilot-tracking/plans/2026-10-28/resident-chat-520-review-correction-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-28/resident-chat-520-review-correction-phase-details.md](.copilot-tracking/details/2026-10-28/resident-chat-520-review-correction-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-28/resident-chat-520-review-correction-research.md](.copilot-tracking/research/2026-10-28/resident-chat-520-review-correction-research.md) | Supplied evidence and decisions |
| [.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-review-correction-critique.md](.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-review-correction-critique.md) | Original Complete / Revise critique |

## Next Steps

Planning parent: correct and disposition PC-001 through PC-003, then finalize without another critique. No user action is required.
