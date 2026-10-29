---
title: Progress dashboard correction round 2 research
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

# Task Research: progress-dashboard-533-correction2

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher | RPI parent, inline |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/progress-dashboard-533-correction2-research.md |

## Research Brief

* Target: malformed closure/return evidence and quadratic dashboard overdue evaluation.
* Purpose/audience: implement the two supplied review corrections for PR #540, Refs #533.
* Scope: API lifecycle replay, core queue clocks, inherited JSON/SQLite tests and browser check.
* Non-goals: UI changes, private data, Azure, publication, historical evidence replacement.
* Criteria: unknown-date coverage without aborting reads; exact overdue parity without building scans; strict static checks and regressions.
* Requested outputs: dated full RPI evidence and local Conventional Commits.
* Output mode: convergence.

## Research Parameters

* Questions: Q1 how to validate both collections without changing valid replay; Q2 which clocks determine overdue independently of blockers; Q3 how to validate within lock/environment constraints.
* Initial internal areas: progress.py, taskqueues.py, Store work_context, building records, progress tests/checks and package guides.
* External scope: none.
* Posture: focused, selected for bounded caller-supplied findings.
* Completion basis: material questions answered with source evidence and contrarian checks.
* Evidence root: .copilot-tracking/.
* Research edits: evidence/state only.
* Explicit limits: no push, az or force-push; full suites require nonblocking heavy admission; current-worktree source imports; /tmp/mv tools if usable.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | Repository guidance and selected RPI Agent | Selected: branch safety, original evidence retention, local-only caller boundary |
| Skill | rpi-research | Selected: three-wave evidence and readiness |
| Specialist | RPI researcher | Skipped: one tightly coupled source trace, handled inline |
| Web skills | UI design/review | Skipped: backend-only correction, no web edits |

## User Participation and Research Decisions

Explicit full-loop request authorizes this correction's automatic progression.
No ordinary confirmation needed; stop after local commits as explicitly requested.
Previous correction session is completed/stopped and remains historical.

## Scope and Success Criteria

Validate malformed evidence, backend parity, exact clock semantics, no per-case building
scan, API/core strict typing and lint/format, unit and progress browser checks.
Missing required prerequisites are reported, never converted into success.

## Task Research Requests and Direction Controls

Both named findings are required. Pulled --rebase first: fast-forward 802efa04
to 7bda02a8 (bot score only). Clean active branch matches open PR #540/main.
Do not use closing keywords, rewrite old evidence or publish.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How should malformed auxiliary lifecycle collections be handled? | straightforward | Answered |
| Q2 | Can overdue evaluation share existing clock logic without full context? | depth | Answered |
| Q3 | What validation is available under the caller's constraints? | straightforward | Answered |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index/memory, package guides and the prior
correction state/Review. Previous null-history fix is present; these two findings
are distinct. Recent branch session search returned no additional history.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Source inspection confirms lifecycle replays the two unvalidated collections and
dashboard counts overdue by materializing work_context for every current case.
Reflection: investigate taskqueues' exact deadline logic before extraction.

#### Wave 2: Deeper

Taskqueues computes deadlines only from hazard response/update, resident update
and projected pending handoff. Deadline is strictly before snapshot; completion
at/before snapshot satisfies it. A released hazard can still have outstanding
deadlines. Handoff projection supplies chase_owner from from_name.
Reflection: a helper can return identical structured overdue rows and be reused
by context and dashboard; it must not evaluate return narratives or blockers.

#### Wave 3: Contrarian

Missing collections default to empty lists, unlike explicit null. Empty lists
and dictionary rows that do not denote transitions remain valid. Dropping bad
rows could invent a complete lifecycle, so reject either entire malformed
collection. Checking only the last row is insufficient. Broad catches mask bugs.
Direct raw handoff use loses chase-owner projection; retain handoff_view.
Existing context accesses the last return narrative, so malformed returns on an
open case must also be covered after the dashboard bypasses full context.
Reflection: strict collection guards plus clock-only extraction address both
failure routes without broadening domain validation or changing work queues.

#### Parent Synthesis and Disposition

Accept C1-C6: strict validation and single shared deadline implementation.
Reject broad catches, skipping rows, null-to-empty coercion and duplicate
dashboard clock logic. No further cycle: all scoped questions answered.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Replay assumes iterable dictionaries for both collections | src/api/src/zava_forward/api/progress.py:101 | High |
| C2 | Dashboard invokes full context per open case | src/api/src/zava_forward/api/progress.py:238 | High |
| C3 | Work context computes building blockers, record scans case membership | src/core/src/zava_forward/core/store.py:317; src/core/src/zava_forward/core/buildings.py:51 | High |
| C4 | Existing progress class is inherited for SQLite | src/api/tests/test_progress_dashboard.py:99; src/api/tests/test_progress_dashboard.py:464 | High |
| C5 | Four ordered deadline kinds and strict snapshot/completion rules | src/core/src/zava_forward/core/taskqueues.py:153; src/core/src/zava_forward/core/taskqueues.py:196; src/core/src/zava_forward/core/taskqueues.py:289 | High |
| C6 | Handoff projection owns chase-owner normalization | src/core/src/zava_forward/core/workflows.py:44 | High |
| C7 | Strict API/core static commands and browser harness exist | src/api/pyproject.toml:61; src/core/pyproject.toml:35; src/api/checks/progress_browser_check.py:29 | High |

No external sources used.

## Findings Mapped to Questions and Evidence

Q1: C1/C4 support list-of-dictionaries guards and inherited persistence regressions.
Q2: C2/C3/C5/C6 support clock-only helper with projected handoff and unchanged rows.
Q3: C7 supports required checks; /tmp/mv has mypy 2.4.1 and Ruff 0.17.3 but no
Playwright and core editable points to issue-531. Use current source PYTHONPATH
for every check and restore needed packages only after the observed missing
package failure. Existing /tmp/ama-533-venv is a browser candidate, not yet verified.

## Alternatives and Decision State

Selected: strict list/dictionary validation and shared clock-only overdue helper.
Reject broad catches or falsy coercion because they hide unknown evidence.

## Open Questions, Risks, and Residual Uncertainty

Clock extraction must preserve provenance, ordering, completion and snapshot semantics.
Heavy lock availability is not yet known. /tmp/mv tool versions differ from
manifest pins; report actual versions, do not claim pinned CI equivalence.

## Current Decisions

Preserve original RPI evidence; use a distinct correction2 identity.

## Potential Next Research

Only re-enter if clock dependencies invalidate extraction.

## Planning Readiness

Ready (C1-C7). Research disposition: executed. All three waves completed inline.
Self-check: sources resolve, no external/legal claim, scope retained, alternatives
and environment limits explicit. Parent proceeds to Plan.
