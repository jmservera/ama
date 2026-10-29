---
title: Regulatory assistant PR 506 rebase plan
ms.date: 2026-10-29
---

Task: pr-506-rebase-2026-10-29; slug: regulatory-assistant-208-rebase.

## Executive summary

Rebase the two existing topic commits onto current main, preserve current-main
contracts and both documentation histories, then validate the integration and
commit only local corrections/evidence. Hosted CI and publication are not
proven by local checks. Original feature Review/human blockers remain unchanged.

## Sources

Research: .copilot-tracking/research/2026-10-29/regulatory-assistant-208-rebase-research.md.
Details: .copilot-tracking/details/2026-10-29/regulatory-assistant-208-rebase-phase-details.md.

## User Decisions and Requirements

* Rebase feat/regulatory-assistant-208 for draft PR #506 onto fetched main.
* Keep both sides' intent and append-only entries; prefer main for rubric
  and scenario manifest conflicts, rerun manifest checks after pinned changes.
* Source only under src; tests outside package directories; no retired code.
* Use /tmp/mv, project source/tests and sibling paths for focused checks.
* Do not run full API discovery unless the nonblocking heavy-lock probe passes.
* No Azure operations, pushing, issue-closing keywords or acceptance inflation.
* Local Conventional Commit with required Copilot coauthor trailer.

## Goals

Restore conflict-free main ancestry and passing relevant local CI checks.

## Scope and Non-Goals

Integration corrections and dated RPI artifacts only. No new regulatory
capability, redesign, cloud operations, approval changes or historical cleanup.

## Functional Requirements

Preserve regulatory routing, bounded offline usage, current main API behavior,
both README/log additions and original RPI evidence.

## Non-Functional Requirements

Use explicit paths to this worktree before shared installed packages. Keep
command/results evidence including failures. Do not equate scoped tests with
full CI or operational acceptance.

## Acceptance Criteria

* origin/main is an ancestor after rebase; no conflict markers or whitespace errors.
* Core/API/agents Ruff and format pass; core/API mypy pass.
* Focused regulatory, privacy, rule, dependency and manifest tests pass.
* Any CI-specific changed-file lint is exercised explicitly.
* One independent critique and one independent integration Review are retained.
* Clean locally committed topic; no push or Azure action.

## Test ownership and budget

Existing component tests are canonical. Exact removals: none. Maximum new test
methods: 2, only if a genuine conflict-induced regression requires them.
No new generated targets except a proven scenario hash refresh; retain main
manifest scenarios and main rubric byte-for-byte. Existing tests provide
semantic feature coverage; this task supplies integration regression evidence.

## Phase Checklist

* [x] P01: Integrate main
* [x] P02: Validate and reconcile
* [x] P03: Independent Review and local commit

## P01: Integrate main

* [x] P01-T01: Rebase, inspect each conflict, preserve documentation and runtime intent.

## P02: Validate and reconcile

* [x] P02-T01: Run project quality and scoped unittests, including pinned manifest.
* [x] P02-T02: Correct only integration defects; record failures and reruns.

## P03: Independent Review and local commit

* [x] P03-T01: Reconcile evidence; obtain one read-only independent Review.
* [x] P03-T02: Configure privacy-safe identity and commit without pushing.

## Critique Disposition

One final-candidate critique executed: Revise, PC-001 (Medium). Applied
directly: P03-T02 now derives commit identity only from successful gh api user,
with no literal fallback. No user decision needed, no second critique.
Planning readiness: Ready after direct disposition.

## Follow-Up Items

Coordinator must publish rebased history with appropriate lease policy and run
hosted CI and any mandatory final exact-head publication gates. Original human
and feature acceptance findings remain in the 2026-10-27 Review.
The single integration Review is Complete / Residual work, no confirmed new
integration defects; RV-001 retains publication, RV-002 original acceptance.
Local implementation/evidence commit be64c291 completed P03. The final
evidence-only commit records completion without changing the assessed source.
All active plan tasks are complete; publication and original acceptance remain
distinct follow-ups, not waived gates.
