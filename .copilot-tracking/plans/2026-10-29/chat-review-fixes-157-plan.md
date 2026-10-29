---
title: Chat review fixes 157 plan
description: Bounded correction plan for PR 503
ms.date: 2026-10-29
---

Task: `157-chat-review-fixes-2026-10-29`; slug `chat-review-fixes-157`.

## Executive Summary

Correct callback failure consumption without exposing unverified replies,
budget the expanded history block, and persist the asking role per message
across JSON/SQLite/SQL Server. No frontend or activation change is needed.
Implementation and the single independent Review are complete. Critique:
Complete / Pass, no findings. Review: Complete / Conformant with justified
divergence for bounded implementation, no implementation defects. Requested
checks pass. SQL Server execution and publication gates remain separately unmet.

## User Decisions and Requirements

* Full dated Research, Plan, Implement and Review loop for the three findings.
* Use feat/agent-chat-157 (PR 503, Refs #157); pull/rebase first (completed).
* Add focused regression coverage for every finding and run relevant existing
  tests, Ruff check/format check and mypy for core and agents.
* Commit locally using Conventional Commits and the supplied Copilot trailer.
* Do not push, use az, touch other worktrees or hand-edit rubric scores.

## Goals

Accurate physical-model accounting, bounded dispatched context and role-correct
follow-ups without weakening current authorization or ordinary workflows.

## Scope and Non-Goals

Agents chat adapter; core chat panel and shared message persistence, including
the regulatory service's direct repository writers and copied legacy messages,
additive SQLite/SQL Server migrations; owning tests and component READMEs.
No new dependency, frontend change, deployment, paid model call or publication.

## Functional Requirements

* Admission exceptions return safe typed failure with zero calls.
* Completion-check exceptions retain known calls and valid usage; record a
  distinct failed completion state and do not expose unverified reply text.
* Keep existing explicit deny/revoke and disabled-provider behavior.
* Count exact final expanded history block, wrappers and newlines included,
  at or below MAX_HISTORY_CHARS; never neutralise it twice.
* Derive actor_role from the server actor in chat_add_message; include only
  user questions matching the current role, not the creation role.
* Old questions lacking provenance remain stored but are excluded from prompts.

## Non-Functional Requirements

No secrets in failures/logs; preserve package dependency boundaries, SQL
portability, restart behavior, optimistic concurrency and current permission
rechecks. Additive migrations are idempotent and do not relabel old questions.

## Acceptance Criteria

* Regression tests demonstrate zero provider calls on admission exceptions
  and retained one-call usage on completion exceptions through panel receipts.
* Four repeated-token 990-character questions cannot dispatch an oversized
  history block; history is nonempty and newest-first selection stays ordered.
* A-to-B-to-A questions follow their actual role, including after reload;
  JSON/SQLite behavior agrees and SQL Server DDL/migration is wired.
* Requested checks run with exact outcomes recorded; no proxy success claims
  for unperformed SQL Server, hosted, human or complete local gates.
* One critique and one independent post-implementation Review are preserved.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct callbacks and consumption
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Safe admission and completion failures

Typed failure envelopes preserve usage/calls and safe outcome codes.

<!-- rpi:phase id=P02 -->
### [x] P02: Correct bounded role-scoped history
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Budget dispatched block
<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Persist per-message actor role

P02-T01 and P02-T02 are conceptually independent; panel regression coverage
depends on both. Persistence migrations depend on the new message column.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and review
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Regressions and component checks
<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Independent Review and local commit

## Test Ownership and Locked Boundary

Canonical targets: src/agents/tests/test_chat_model.py (callback tests),
src/core/tests/test_chat_panel.py (history tests),
src/core/tests/test_chatthreads.py (storage/migration parity).
Exact removals: none. Maximum additions: twelve test methods across those files.
No generated tests or snapshots. Callback tests may inject ChatPanel through
duck-typed storage to verify receipts without a forbidden agents-to-API import.
Run focused tests red before fixes, then green; run full core/agents suites and
focused API chat integration if installed; component Ruff/mypy.
Full publication gate is not bypassed: owner forbids az/other worktrees,
so any incompatible complete gate remains a documented publication blocker.

## Critique Disposition

The single independent final-candidate critique is Complete / Pass, with no
PC-xxx findings. Direct disposition: accept; no user decision or rerun needed.
Report: .copilot-tracking/reviews/plans/2026-10-29/chat-review-fixes-157-plan-critique.md.

## Follow-Up Items

Inherited publication/human/activation gates remain outside these fixes.
Actual SQL Server migration and shared role tests require an owned disposable
server. Complete gate requires checkout/tool actions incompatible with the
owner's no-other-worktrees/no-az boundary; no publication is requested.
No newly invented feature work.

## Handoff

Research: .copilot-tracking/research/2026-10-29/chat-review-fixes-157-research.md.
Details: .copilot-tracking/details/2026-10-29/chat-review-fixes-157-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-29/chat-review-fixes-157-changes.md.
P01/P02 and P03-T01 complete. P03-T02 is complete at the local commit persistence boundary. The original
independent Review is preserved, not repeated. No source or test correction
was made after it. No push or operational acceptance is implied.
