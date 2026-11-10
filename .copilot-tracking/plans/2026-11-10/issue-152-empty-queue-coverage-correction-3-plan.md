<!-- markdownlint-disable-file -->

# Implementation Plan: issue-152-empty-queue-coverage-correction-3

| Field | Value |
|---|---|
| Task ID | issue-152-empty-queue-coverage-correction-3 |
| Date | 2026-11-10 (prospective, written before the merge) |
| Parent | correction 2, correction 1 and original task (preserved unchanged) |
| Research | .copilot-tracking/research/2026-11-10/issue-152-empty-queue-coverage-correction-3-research.md |
| Details | .copilot-tracking/details/2026-11-10/issue-152-empty-queue-coverage-correction-3-phase-details.md |
| Critique | .copilot-tracking/challenges/2026-11-10/issue-152-empty-queue-coverage-correction-3-critique.md |
| Changes | .copilot-tracking/changes/2026-11-10/issue-152-empty-queue-coverage-correction-3-changes.md |
| Tier | targeted DEMO validation (focused); no `--changed` or complete gate run here |

## Executive Summary

Correction 3 of 5 total (two remain). The retained branch holds an honest empty-queue explanation: no-match is a search result, and an empty unfiltered own queue says coverage is unknown. It has never been integrated with current main or exercised in the served browser harness. This correction records the fetched `origin/main`, performs one ordinary merge into the branch preserving history and both intents, binds the changed browser-harness recipe hash through the existing scenario-manifest mechanism, and runs targeted validation plus the existing served workbench browser harness. It makes no coverage-producer, server, navigation, intake, persistence, finance, resident_decisions, SQL or acceptance claim. `Refs #152` only.

## User Decisions and Requirements

* Recover the existing task; no reset, rebase, cherry-pick, drop, stash, amend, force, push, PR or issue write. Ordinary merge only.
* Keep all current-main behaviour (account label, simulator navigation, priority history controls and the rest).
* Allow only the directly coupled recipe-hash correction in `scenario-manifest.json` and minimal index/log maintenance if repository rules require; preserve Proposed/unapproved status and fixture coverage limits.
* Fresh web-design-guidelines rules before implementation and before review; Fluent 2, plain-language and WCAG baselines retained; no visual overhaul.
* Report RUN/PASS/SKIP accurately; actual `date -u` timestamps only.

## Goals

* G1: `origin/main` merged into the branch with no loss of either intent.
* G2: scenario-manifest recipe hash matches the changed harness through the existing mechanism; Core manifest/needs-inventory tests pass.
* G3: targeted tests, Node syntax, strict API mypy, Ruff and the served browser harness are actually run on the integrated head, with exact outcomes.

## Non-Goals

* Runtime coverage producer or trusted declaration; server.py, navigation, routes, intake, persistence, finance, resident_decisions; SQL, image, model, Azure, release; human, AT or usability acceptance; AC-034/043 or whole 152 closure.

## Acceptance Criteria

* AC1: merge commit with parents e4f77fa75 and the recorded origin/main SHA; no conflict resolution beyond the slice, or a stop with evidence.
* AC2: `queueEmptyExplanation`, the `listView` empty render and main's other app.js features all present after the merge.
* AC3: the recipe SHA-256 in `scenario-manifest.json` equals the harness file; Core manifest and needs-inventory tests pass; no source set, hash, expected data, audit or permission is weakened.
* AC4: served harness exit status, PASS lines (own-queue nonempty/empty role cases, no-match copy, supported 320/390/1280 widths and keyboard contracts if provided) recorded; a failure or missing browser is reported as such.
* AC5: original records and the adverse receipt unchanged; clean local candidate.

## Phase Checklist

<!-- P01 -->
### [x] P01: Integrate, bind and validate

* [x] P01-T01 Persist state, fetch and record origin/main, web guidelines pre-implementation; ordinary merge.
* [x] P01-T02 Verify both intents survive (grep/diff against main and branch); stop on overlap.
* [x] P01-T03 Read the scenario-manifest integrity code and correct the recipe hash by the existing mechanism; minimal index/log only if required.
* [x] P01-T04 Prepare owned venv; run targeted tests, Node, mypy, Ruff, Core integrity, served browser harness.
* [x] P01-T05 Commit with local noreply identity and Copilot trailer; review once; final handoff.

## Dependencies and Risks

* Risk: stale recipe hash; mitigated by P01-T03. Risk: harness or browser unavailable; report blocked, no fallback. Risk: main's app.js changes interact with the empty-state surface; mitigated by AC2 checks and the browser harness.
* Risk: the earlier API-suite failure may recur; it is outside targeted scope and stays adverse evidence.

## Critique Disposition

Critique executed once; see the critique artifact. Dispositions are recorded below after it.

| ID | Severity | Disposition |
|---|---|---|
| PC-001 | Medium | Applied: P01-T01 commits the pre-merge C3 records and state before `git merge`. |
| PC-002 | Low | Applied: P01-T02 diffs app.js against origin/main (slice hunks only), greps main's features and runs the whole workbench module. |
| PC-003 | Low | Applied: P01-T04 reads the API project mypy configuration and runs it over the whole project, not a file. |

Verdict Revise; all applied directly; no second critique.

## Follow-Up Items

* Two further corrections remain of the five-total allowance; none is inferred here.
* Coordinator: independent exact-head assessment, hosted checks, publication decision.
* Owner decision on a trusted coverage producer (original F1).
