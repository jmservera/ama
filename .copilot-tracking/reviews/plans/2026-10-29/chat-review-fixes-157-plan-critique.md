---
title: Chat review fixes 157 final-candidate plan critique
description: Single independent bounded assessment of the three chat corrections
ms.date: 2026-10-29
---

## Metadata

* Task ID: 157-chat-review-fixes-2026-10-29
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/chat-review-fixes-157-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/chat-review-fixes-157-phase-details.md
* Research: .copilot-tracking/research/2026-10-29/chat-review-fixes-157-research.md
* Critique execution status: Complete
* Candidate baseline: c5d8873a on feat/agent-chat-157
* Assessment: the single independent final-candidate critique requested by the caller.

## Inputs and Criterion Boundary

* The supplied plan, phase details and research were read in full. Repository
  context was read from docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory was treated as context, not evidence.
* The caller requires precisely three corrections: callback-exception
  accounting and fail-closed completion handling; an exact expanded history
  block no larger than 4000 characters for four 990-character repeated
  UNTRUSTED>> questions; and history scoped to the role of each question
  through an A-to-B-to-A role transition.
* The assessment covers requirements, C1-C9, P01-P03 and every task, including
  acceptance criteria, phase dependencies, persistence compatibility,
  regression ownership and validation boundaries.
* The locked test boundary is preserved: the three named owning test files,
  no removals, at most twelve added test methods, and no generated tests or
  snapshots. Relevant existing tests and core/agents Ruff check, format check
  and mypy remain required.
* Full RPI evidence, independent post-implementation Review and a local
  Conventional Commit remain requested. No push, az, other worktrees, rubric
  edits, source edits by this reviewer, nested agents or second critique
  are authorized.
* This is a plan credibility assessment, not an implementation review, test
  execution, SQL Server acceptance or publication authorization.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Admission exception accounting; C1-C2; P01-T01 | Covered | The adapter currently invokes admission before the worker without a typed exception boundary. The panel preassigns one call before invoking the adapter. A zero-call ModelUnavailable envelope reaches the panel's existing typed failure handler and corrects that receipt. The plan requires provider-not-called and panel audit/receipt tests. |
| Completion exception accounting; C1-C2, C7; P01-T01 | Covered | The worker returns its envelope before the second callback. The proposed completion-check-failed outcome retains calculated calls and validated usage while withholding provider text. Existing explicit revocation already establishes this envelope pattern. Disabled completion remains zero calls rather than an invented invocation. |
| Safe failure and authorization behavior; P01-T01 | Covered | Catching ordinary callback exceptions, logging only the exception class and raising safe outcomes from None preserves the existing fallback boundary without exposing callback/provider text. Explicit deny/revoke and current permission/source rechecks remain unchanged. |
| Exact history bound; C3, C6; P02-T01 | Covered | The current raw-row budget precedes delimiter expansion and omits block wrappers. The details instead construct the actual candidate block using the full candidate length, check its final length and append that same expanded value. This addresses expansion and wrapper overhead without double neutralisation. Acceptance includes the four 990-character repeated-token counterexample, nonempty history and ordered newest-first selection. |
| Role-scoped questions; C3-C4; P02-T02 | Covered | Current filtering uses thread creation role for every message. Persisting server-actor role at message creation and matching individual user messages to current role supports both directions of A-to-B-to-A without assigning retrospective provenance. Legacy unknown-role questions are retained in storage but excluded from prompts. |
| Persistence and migration; C4-C5, C8; P02-T02 | Covered | MemoryRepo copies message dictionaries, but SqlRepo serializes MESSAGE_COLS. Appending actor_role preserves the existing positional evidence decoding at index 6. Fresh DDL and additive idempotent migrations are explicitly planned for SQLite and SQL Server, with empty legacy defaults. |
| Dependencies and compatibility; P01-P02 | Covered | Callback and history changes have separate implementation boundaries. Integrated panel regressions depend on the history budget and role filter. SQL serialization/schema work accompanies the new message field; dependency direction, optimistic concurrency and restart behavior are preserved. |
| Focused regressions and existing behavior; P03-T01 | Covered | The locked owners cover adapter/panel receipts, exact emitted history, role roundtrip and migrations. Red-before-fix/green-after-fix evidence, full core/agents suites, focused API integration when available and package static checks are specified without test removal or cross-package API imports. |
| Documentation and local delivery; P03-T01-P03-T02 | Covered | Owning READMEs, exact check outcomes, one fresh independent Review and authenticated local noreply commit identity are specified. The plan requires preserving adverse evidence rather than silently correcting its recorded outcome. |
| Publication and unavailable integrations; C9; P03-T02 | Covered | The plan explicitly refuses proxy success for SQL Server, hosted/human approval and the complete gate. Owner restrictions are retained as publication blockers where incompatible with gate execution; no publication is planned. |

## Verdict

* Verdict: Pass
* Rationale: The proposed corrections follow the actual adapter, receipt,
  prompt-building and persistence paths. Acceptance criteria address the
  supplied failure examples rather than replacing them with raw-history,
  total-prompt or JSON-only proxies. The bounded regression scope is credible
  without adding a feature, weakening authorization or changing locked gates.

## Findings

No actionable PC-xxx findings were identified within the supplied boundary.

* Critical: 0
* High: 0
* Medium: 0
* Low: 0
* Action owner/resolution: none required for this critique.
* Direct disposition: possible. The planning parent can record this Pass and
  finalize the plan without correction, a user decision or another critique.

## Strengths and Residual Risk

* Completion-check-failed distinguishes an unknown authorization result from
  explicit revocation and preserves physical consumption without authorizing
  release of the unchecked answer.
* The history regression measures the dispatched expanded block, including
  delimiters and newlines, and requires useful retained history. Dropping all
  history is not an acceptable way to pass the bound.
* Per-message provenance is written in the shared storage path, not only in
  panel memory. Legacy exclusion avoids fabricating historical roles.
* The SQL Server shared suite in src/api/tests/test_mssqlstore.py inherits
  ChatBehaviour from src/core/tests/test_chatthreads.py. Shared role tests can
  therefore cover that backend when its disposable-service prerequisite is
  met. Inheritance does not establish an executed migration or SQL result.
* The plan explicitly accepts unavailable SQL Server and incompatible complete
  gate execution as unverified/blocked evidence, not successful validation.
  Human, hosted and activation gates remain open.

## Questions or Blocking Evidence Gaps

None prevents assessing or implementing this bounded plan. No user response is
required. Unavailable integration/publication evidence remains governed by the
plan's existing blockers.

## Limitations

* Relevant source inspected: src/agents/src/zava_forward/agents/chat.py,
  src/agents/src/zava_forward/agents/dispatch.py,
  src/core/src/zava_forward/core/chat_panel.py,
  src/core/src/zava_forward/core/chat_isolation.py,
  src/core/src/zava_forward/core/chatthreads.py,
  src/core/src/zava_forward/core/sqlstore.py and
  src/core/src/zava_forward/core/mssqlstore.py.
* Existing owning tests, API panel tests, SQL Server shared-test wiring,
  package pyproject.toml files and component validation guidance were read.
  No open-ended external research was performed.
* No tests, dependency installation, cloud commands, gate execution, commit or
  push were performed during this critique. Implementation is still pending;
  passing this plan does not assert passing software.
* Initial untracked parent planning/state files were left untouched. This
  report is the only file written by this reviewer.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record the Pass disposition, finalize the plan and
  proceed to P01 under the existing locked test and gate boundaries.
* User response required: no.
* Stop: return to the active parent; do not perform another critique or start
  implementation from this reviewer.

## Next Steps

The active planning parent may directly disposition this critique and continue
the requested RPI loop. No user action is required.
