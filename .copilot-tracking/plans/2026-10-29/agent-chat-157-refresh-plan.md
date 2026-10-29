<!-- markdownlint-disable-file -->
# RPI Plan: agent-chat-157-refresh

## Task Metadata

* Task ID: pr-503-refresh-2026-10-29
* Task slug: agent-chat-157-refresh
* Plan date: 2026-10-29
* Planning status: Ready; single critique Complete / Revise, direct corrections applied
* Phase details: .copilot-tracking/details/2026-10-29/agent-chat-157-refresh-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/agent-chat-157-refresh-plan-critique.md

## Executive Summary

Rebase the four local topic commits onto fetched main and reconcile overlaps
without dropping newer employee-chat behavior or the topic's admission,
privacy and browser-disclaimer safeguards. Run scoped local checks and leave
a Conventional Commit plus dated evidence for the coordinator, without push.
Hosted CI and draft feature acceptance remain separate from this local repair.
No implementation decision is unresolved; publication gates may remain blocked.

## User Decisions and Requirements

* Run research, plan, implement and review with dated tracking artifacts.
* Fetch and rebase feat/agent-chat-157 onto origin/main for draft PR #503.
* Preserve both sides' intent and both append-only/index contributions.
* Take origin/main's rubric files and scenario manifest; validate frozen sources.
* Keep source under src and tests outside packages; no legacy implementation.
* Use /tmp/mv with source/test sibling PYTHONPATH; run Ruff, format, mypy and relevant unittests.
* Do not run full API discovery without nonblocking heavy-lock acquisition.
* No Azure resource changes, push or issue-closing keywords.
* Commit with Conventional Commit and required Copilot coauthor trailer.

## Goals

Remove local ancestry conflicts and demonstrate compatibility of the reconciled
runtime through existing focused regression contracts.

## Scope and Non-Goals

Scope: rebase conflicts, directly coupled regressions, original evidence
preservation and a local committed candidate. Exclude feature expansion,
original RV-001 through RV-005 remediation, resources, activation and remote
publication. No unnecessary UI redesign or new test infrastructure.

## Functional Requirements

Retain later employee-chat/runtime changes and earlier topic isolation,
admission, privacy and precise disclaimer assertions. Preserve both index/log
contributions and immutable historical critique/Review verdicts.

## Non-Functional Requirements

Lint, format and types must pass for core/API/agents. Existing relevant tests
must pass with skips explicitly disclosed. Do not edit workflow protections,
rubric scoring semantics or dependency pins to obtain a green result.

## Acceptance Criteria

* Fetched main is an ancestor of final HEAD and no unmerged paths remain.
* Main's rubric and manifest are byte-identical to the captured rebase target.
  Any pin mismatch blocks this criterion; no snapshot exception is authorized.
* Core/API/agents Ruff, format and mypy plus chat/manifest/role tests pass.
* Semantic integration is inspected, not inferred from textual rebase success.
* Changes artifact records exact commands, outcomes and validation limitations.
* Implementation and original RPI evidence are committed, independent Review
  runs once, and no push/Azure change occurs.
* Hosted success is not claimed before coordinator publication.

## Sources

* .copilot-tracking/research/2026-10-29/agent-chat-157-refresh-research.md
* src/README.md and .github/workflows/src-ci.yml
* Existing 2026-10-27 chat evidence and draft PR #503

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reconcile branch

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase and resolve semantic conflicts

Dependencies: critique disposition and fresh expected-branch/worktree preflight.
Fetch main and capture immutable HEAD/base; stop on unexpected pre-existing
changes rather than stash/reset them. Rebase onto the captured main SHA, resolve
each conflict with both code intents retained, and take main's rubric/manifest.
Inspect base-to-head differences and original patch equivalence where possible.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and commit

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute focused checks and persist evidence

Dependencies: P01. Run component-wide lightweight Ruff/format/mypy and selected
chat, isolation, memory, admission, evaluator, manifest, role and browser
regressions. Source/test paths precede existing editable paths in /tmp/mv.
Record failures and fixes, preserve original adverse results. Resolve
authenticated account email locally before commit, use required trailer.
Record complete publication gate separately; missing prerequisites block
publication rather than being represented as a pass.

<!-- rpi:phase id=P03 -->
### [x] P03: Independent Review and local handoff

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Review once and route remaining work

Dependencies: P02. Independent worker reviews the committed candidate and
dated evidence once. Do not silently repeat Review or remediate Review findings
inside this loop. Commit its original evidence and final state locally;
later evidence commits do not imply exact-head approval. No push.

## Test Ownership and Change Budget

Canonical source: existing src/{core,agents,api}/src packages.
Canonical tests: their existing sibling tests and API checks.
Removals: none. Maximum additions: two tightly scoped test methods only if
conflict resolution exposes an uncovered behavior; otherwise zero.
Generated targets: none. Main owns rubric and manifest snapshots.
Semantic coverage: explicit conflict-intent comparison and existing admission/
employee-chat checks. Regression coverage: selected unittests and browser check
if overlap requires it. No full API discovery planned.

## Dependencies

Python /tmp/mv and installed source packages; no install without an observed
missing-dependency failure. No private data, inference or cloud dependency.

## Critique Disposition

Critique execution: Complete; original verdict: Revise. No second critique.

| Finding | Disposition | Evidence / rationale |
| --- | --- | --- |
| PC-001 | Applied | Removed manifest hash exception; main snapshots must remain exact |
| PC-002 | Applied | Fresh branch/worktree preflight and immutable rebase/snapshot target required |
| PC-003 | Applied | Mandatory concrete selector/coverage table and import-origin check before validation; browser applicability explicit in details |
| PC-004 | Partially applied / unsupported premise rejected | Focused-only validation retained. Critique's claimed prohibition on temporary writes is not present in the parent instructions; caller explicitly mandates /tmp/mv and /tmp shared lock, and repository requires external receipts/logs. Do not invent that restriction. No full discovery is planned; a future full run must hold the real shared lock throughout execution |

## Follow-Up Items

* Coordinator must push and observe fresh hosted checks; rubric infrastructure
  failure is not established fixed by local runtime checks.
* Existing RV-001 through RV-005 and human/activation gates remain outside
  refresh acceptance.

## Handoff

Implementation artifact: .copilot-tracking/changes/2026-10-29/agent-chat-157-refresh-changes.md.
All P01-P03 tasks executed. Single independent Review: Complete / Conformant
for bounded refresh at ca5cb010. Automatic parent persists evidence and the
planned publication-gate attempt; no push or whole-feature acceptance implied.
