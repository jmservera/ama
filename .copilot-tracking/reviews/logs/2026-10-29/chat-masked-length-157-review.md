---
title: "Review: chat masked-length admission 157"
description: "Independent bounded post-implementation Review."
ms.date: "2026-10-29"
---

## Scope and Evidence

* Task ID: 157-chat-masked-length-2026-10-29
* Review date: 2026-10-29
* Review scope: One independent post-implementation Review of chat-masked-length-157.
* Assessed boundary: Diff relative to e833fc8c in src/core/src/zava_forward/core/chat_panel.py, src/core/tests/test_chat_panel.py, src/core/README.md and the supplied task-specific RPI evidence. No publication or exact-committed-head acceptance.
* Plan: .copilot-tracking/plans/2026-10-29/chat-masked-length-157-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/chat-masked-length-157-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/chat-masked-length-157-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-29/chat-masked-length-157-changes.md
* Research: .copilot-tracking/research/2026-10-29/chat-masked-length-157-research.md

## Opening Review State

* Interpreted review goal: Independently establish whether masked questions above MAX_QUESTION_CHARS receive the existing LIMIT_REACHED fallback instead of neutralise truncation while retaining raw-length admission and refusal behavior.
* Review scope: Supplied bounded implementation, regression coverage, README and task evidence only.
* Evidence readiness: Supplied artifact paths and modified implementation files are present in the worktree; substantive comparison is not yet complete.
* Acceptance basis: Exact synthetic raw977/masked2297 regression, all seven modes, no dispatch on overflow, stored fallback turns and complete exact-1000 masked dispatch; preserved raw guard and refusal behavior.
* First comparison boundary: Plan, details, critique, changes and research against the bounded diff from e833fc8c.
* Active read-only boundaries: Only this canonical review record may be written. No source/artifact corrections, other agents, second Review, az, push or rubric latest.json edits.
* Initial blockers: None established. Parent retains local commit after Review; human, hosted and publication approvals remain outside this assessment.

## Execution Status

* Execution status: Complete
* Review execution evidence: One independent Review on 2026-10-29; read supplied task artifacts, inspected the complete bounded diff and surrounding admission/finish/dispatch path, and executed independent focused checks. No other agents or repeat Review.
* Delivery execution is separate: P02-T02 local commit is still pending with the parent. This record assesses the worktree, not an exact committed head.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Exactly two StoredQuestionTests methods; pre-fix red and inclusive-boundary evidence | Reconciled | Exact supplied overflow fixture and seven modes; no test removals. |
| P01-T02 | Existing guard extended; core README clarified | Reconciled | One production conditional changes; existing fallback and refusal order retained. |
| P02-T01 | Core/API focused tests, Ruff, mypy and whitespace evidence | Reconciled | Counts and browser skip are explicit; independent smaller selector supports the implementation claim. |
| P02-T02 | Independent Review and local commit pending | Reconciled | Correctly unchecked at handoff; Review completes here, local commit remains the parent's next action, not an implementation defect. |
| Follow-Up Items | Existing publication/hosted/human/activation gates excluded | Reconciled | No unauthorized implementation or approval claim. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/tests/test_chat_panel.py | Regression for expanding redaction and distinct inclusive boundary | Overflow asserts 977 raw / 2297 masked, LIMIT_REACHED, workflow-only response, no citations/calls/prompts and both stored turns. Boundary asserts full masked Question suffix and one dispatch. Both iterate None, general and five REGISTRY modes with fresh permitted case-bound threads. | Parent records valid pre-fix red followed by green; independent memory-only selector confirms both behaviors across seven modes. | Meaningful coverage, not vacuous lack-of-sources rejection; invalid model JSON appropriately does not require an answer outcome at the boundary. |
| P01-T02 | src/core/src/zava_forward/core/chat_panel.py; src/core/README.md | Reject oversized masked questions before neutralise instead of truncating | Raw strict-greater-than check retained with OR masked strict-greater-than check. Refusal remains earlier; shared finish remains later. README accurately describes both admission limits. | Independent overflow, exact boundary, raw-only overflow and overflow-refusal precedence checks passed. | Conformant; storage, audit, limits, redaction, privacy checks and prompt escaping remain unchanged. |
| P02-T01 | Task changes/plan/details | Preserve original evidence and reconcile state | Core 85 tests/no skips; API 70 run/one opt-in browser skip; core-wide lint/format and mypy results recorded. | Supplied evidence distinguished from independent checks below. | Sufficient for bounded local fix, not publication or operational acceptance. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 fixture | Existing response key corrected from text to reply before valid red run | First attempt raised seven KeyErrors; owner intent unchanged | Changes record distinguishes fixture failure from subsequent actual regression failure | No material revision; original Complete / Pass critique retained | Supported ordinary fixture correction; no production defect inferred from KeyErrors. |
| P01/P02 completion markers and handoff | Mark implementation and validation complete, retain Review/commit pending | Recorded green validations and bounded diff | Plan, details, changes and supplied task-state JSON agree on continuation | No significant divergence or fresh decision requiring planning/critique | Reconciled. Historical in-progress wording inside the original validation narrative is superseded explicitly by its completed results table and current handoff; not a material evidence gap. |

## Critique and Material Revision Assessment

* Latest critique: One independent final-candidate assessment, Complete / Pass, Critical 0, High 0, Medium 0, Low 0; no PC findings awaiting disposition.
* Implementation matches the critiqued guard, two-method test design, refusal ordering, stored fallback and local-only delivery scope.
* No significant or divergent implementation decision, altered dependency or material revision was identified. No dependent-work pause or additional owner decision was required.
* Justification is supported by actual redaction expansion and neutralise slicing before escaping. The new guard prevents the over-cap masked text from reaching that call rather than changing the cap or weakening masking.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Existing publication/hosted/human/activation gates | Owner authorizes local-only commit, no push/cloud or operational activation | Parent/owner must independently authorize and satisfy relevant gates before any future publication or activation | Distinct existing follow-up; not a defect or additional active implementation scope. |

## Findings

No substantive RV-xxx findings within the supplied boundary. Severity counts: Critical 0; High 0; Medium 0; Low 0. No placeholder finding is created.

## Defects

* None identified in the bounded fix.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | Parent continues pending local delivery | No implementation, decision or material evidence gap requires a later RPI stage. |

Later implementation of any separately identified issue does not require this Review to run again.

## Residual Work

* Local commit and final local delivery verification remain P02-T02 work for the parent; they are intentionally subsequent to Review.
* Complete publication receipt, hosted checks, human approval, actual-provider acceptance and operational activation remain separately unmet/unestablished. No waiver or acceptance is implied by these checks.
* API opt-in browser scenario remains skipped in supplied validation. No UI change occurs in this diff; browser conformance is not claimed.

## Blockers and Remaining Work

* Review blockers: None for the bounded source/test/documentation assessment.
* Remaining active work: Parent records this actual outcome in its owned evidence, commits locally with the required authenticated privacy-safe identity and co-author trailer, then verifies local commit and worktree. No push is authorized.
* Scope inspection: Branch feat/agent-chat-157; tracked diff relative to e833fc8c names only the three allowed core files. Untracked paths are this task's research, plan, details, changes, critique, review and task-state JSON. PR 503/issue 157 lifecycle is supplied context, not independently refreshed.
* No source, plan, detail, critique, research, changes, task-state or rubric correction was made by this reviewer.

## Validation Evidence

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| Parent: core PYTHONPATH=tests ../../.venv/bin/python -m unittest test_chat_panel test_chatthreads test_chat_privacy test_chat_memory -q | Four focused core chat modules | Passed, supplied evidence | 85 tests, no skips; recorded in task changes/details. Not rerun in full here. |
| Parent: API PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_chat_panel test_chat_isolation -q | API chat and isolation | Passed with skip, supplied evidence | 70 run, one existing ZF_BROWSER_TESTS opt-in Chromium scenario skipped; existing law-store diagnostics did not fail suite. |
| Parent: core ../../.venv/bin/python -m ruff check .; -m ruff format --check .; -m mypy | Core-wide static checks | Passed, supplied evidence | Format 108 files; mypy 161 files; no claim of independent full rerun. |
| Independent: core PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests ../../.venv/bin/python -B -m unittest test_chat_panel.PureTests test_chat_panel.OutOfScopeTests test_chat_panel.ActionClaimTests test_chat_panel.LabelTests -q | Existing pure chat/policy behavior | Passed | 11 tests, no skips, exit 0. |
| Independent: core PYTHONDONTWRITEBYTECODE=1 ../../.venv/bin/python -B - with inline memory-only Store/isolation doubles and actual ChatPanel.ask, redact and REGISTRY | Four behaviors across all seven modes | Passed | 28 scenarios: exact supplied 977/2297 overflow, 989/1000 inclusive boundary, raw-only overflow despite contraction, and overflow refusal precedence. Asserted dispatch count, stored question/reply, two audit events, fallback fields and not-called provider outcome; complete masked Question suffix on dispatch. No provider or filesystem fixture writes. |
| Independent selector fixture first attempt | Review-only synthetic raw-contraction assertion | Failed, corrected | Initially used repeated short emails, which expand rather than contract. Assertion failed before ChatPanel scenarios. Replaced only the ephemeral in-memory fixture with 1000 a characters plus @example.invalid, which contracts below cap; complete 28-scenario selector then exited 0. No product failure or source change. |
| Independent: core ../../.venv/bin/python -B -m ruff check --no-cache src/zava_forward/core/chat_panel.py tests/test_chat_panel.py | Changed Python files | Passed | All checks passed; no cache writes. |
| Independent: core ../../.venv/bin/python -B -m ruff format --check --no-cache src/zava_forward/core/chat_panel.py tests/test_chat_panel.py | Changed Python files | Passed | Two files already formatted. |
| Independent: git diff --check; git diff --name-only e833fc8c; git status --short | Whitespace and source boundary | Passed | No whitespace errors; only approved tracked source/test/guide changes and task-specific untracked evidence. |
| Browser, complete publication gate, SQL/browser/scanner prerequisite assessment, actual provider, hosted/human approval | Publication/operational acceptance | Not performed | Outside owner-authorized bounded Review; no cloud fallback, az, push, rubric latest.json edit or approval claim. |

The independent memory-only selector supplements rather than replaces supplied real-Store test evidence. Its raw-only fixture independently distinguishes preservation of the raw check from an implementation that checks masked length alone. The overflow-refusal scenario confirms the original earlier refusal wins even when the question exceeds the masked cap.

## Outcome

* Outcome: Conformant
* Outcome rationale: The surgical guard rejects masked overflow using existing LIMIT_REACHED workflow fallback, preserves the raw check and refusal priority, and accepts a complete exact-cap masked question. The two added methods and surrounding unchanged tests cover the requested regression without broadening scope. Supplied focused validation is supported by independent relevant behavioral/static checks.
* This is bounded worktree conformance, not full-task delivery completion, exact-committed-head assessment, hosted acceptance, human approval or publication permission.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | None identified. |
| Decision gap or invalid assumption | None | No significant divergence identified. |
| Material evidence gap | None | Evidence sufficient for bounded verdict. |
| Non-blocking residual work | Parent P02-T02 and existing separate approval gates | Record Review and commit locally; obtain separately authorized approvals before any future publication or activation. |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Supplied core/API focused suite and core-wide static results; independent 11 pure tests, 28 memory-only scenarios, changed-file Ruff lint/format and diff checks passed.
* Blockers: None for bounded Review. Local commit pending; required human/hosted/publication/activation approvals remain unmet.
* Next owner: Active parent; no repeat Review and no additional user command required for this handoff.
