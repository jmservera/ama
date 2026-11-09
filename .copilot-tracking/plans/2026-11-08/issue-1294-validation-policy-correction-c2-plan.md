<!-- markdownlint-disable-file -->
# Plan: issue-1294-validation-policy-correction-c2

* Task ID: issue-1294-validation-policy-correction-c2
* Date: 2026-11-08
* Parent: issue-1294-validation-policy-correction-c1 (HEAD 7260826bcc4ba8688baccf75b651780ccd0b0d11, tree 3d990a5a48aba65b8c07f9d3b71095d5b5ee780c, base fa7ae0c9770e890f82482456bfcb8e97f1e05429)
* Research: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c2-research.md (Ready)
* Details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c2-phase-details.md
* Changes (created by implementation): .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-correction-c2-changes.md

## Executive Summary

Three independent-review findings remain. Two are wording defects in src/README.md: a sentence that makes every mixed change full tier, and a runner-only 58-byte `--out` limit attributed to the direct employee-chat harness (whose `--out` only receives the results file; the 58-byte rule derives from the runner's TMPDIR wrapper). The third is process: the earlier behavior verdict was Revise with after-grade edits, so a fresh full independently designed, executed and graded behavior cycle is required on the corrected files. Focused tier; no workflow, tool or source edits. The host cannot bind a model for subagents, so the run is a proxy with no intended-profile or native claim.

## User Decisions and Requirements

* Focused tier; owner policy: targeted checks for small changes, full exact-head validation for major, SQL, infrastructure, deployment, security-sensitive and release changes.
* Mixed changes take the strictest applicable tier: two focused components stay focused; any full-tier component makes the candidate full; doubt takes the full tier (owner wording kept verbatim, no qualifier).
* Direct harness `--out` must be described only with evidence-supported constraints.
* Fresh full behavior cycle (design, simulation, independent grading), no reuse of prior grades; retain sandbox; preserve reports 1 and 2, sandbox 2 and all adverse evidence; Deferred with exact blocker if a stage cannot run; proxy labelling when the profile cannot be bound.
* No push, PR, board, rebase, cleanup, deletion, workflow or source change, install, Docker, SQL, Azure.

## Goals

* Correct F2 and F3 wording; satisfy F1 with a fresh run; commit a frozen local candidate with a correction Review.

## Scope and Non-Goals

* In scope: src/README.md, docs/reference/log.md (append), new C2 RPI and HVE evidence. Coordinator and copilot-instructions wording already say strictest applicable; change only if the behavior run finds a defect.
* Non-goals: workflow, tool, source edits; measuring Chromium socket behavior; hosted CI.

## Functional Requirements

* FR1 Every README mention of mixed changes (line 68 lead, classification paragraph, examples table) says strictest applicable tier, with focused plus focused staying focused; "doubt takes the full tier" kept verbatim.
* FR2 Examples table has two labelled mixed rows: documentation plus infra/main.bicep (full, a component is infrastructure) and documentation plus a small employee-chat change (focused).
* FR3 README direct-check list (both the line ~205 sentence and the ~198 list) states: direct `--out` only receives `axe-results.json` and has no evidenced length limit; the 58-byte limit is runner-specific; the direct run's temporary and state directory is under `ZF_BROWSER_SCRATCH` (absolute, outside the checkout, else the harness raises ValueError) or `<checkout>/.venv` when unset; Chromium inherits the caller TMPDIR, so a short TMPDIR is an unmeasured precaution only.
* FR4 New behavior run 3 with new sandbox 2026-11-08-issue-1294-policy-3, report 3.

## Non-Functional Requirements

* ASCII punctuation, no em dashes, no deletion of evidence, read-only Python with PYTHONDONTWRITEBYTECODE=1, appended log only.

## Acceptance Criteria

* AC1 Every "mixed" occurrence in src/README.md inspected and reads strictest applicable; no "any mixed change"; no "genuine risk" text.
* AC2 No claim that the direct harness `--out` is subject to the 58-byte limit.
* AC3 Report 3 is a full run with independent design, grading, retained sandbox, per-stage agent identity, actual model if observable (else not observable), context separation, an explicit proxy no-intended-profile-no-native label, and its actual verdict. Terminal-state rule: if grading requires any edit, the status is recorded as Revise with the edit as an unsimulated post-grade change flagged for the exact-head reviewer and owner; no Pass is claimed and no self-reuse.
* AC4 diff check, link scan, ASCII, stale-phrase, selection reproduction recorded with exits, outputs stored in the sandbox-3 folder or the changes record (workspace only).
* AC6 Classification line with basis (guide wording only; no workflow, tool, manifest, Dockerfile, SQL, infra, deployment or security-control change), allowed path list, and before/after `git status --short --ignored` showing prior sandboxes, reports and tools/__pycache__ intact.
* AC5 Prior reports, sandbox 2, pycache untouched; clean committed candidate.

## Phase Checklist

### [x] P01: Correct README wording
#### [x] P01-T01: Mixed-change rule and examples (F2)
#### [x] P01-T02: Direct harness out and scratch statement (F3)
#### [x] P01-T03: Append C2 correction log entry

### [x] P02: Validate and fresh behavior cycle
#### [x] P02-T01: Link, diff, ASCII, stale-phrase, selection checks
#### [x] P02-T02: Full independent behavior run 3 (F1), retained sandbox; apply any findings once

### [x] P03: Changes record, correction Review, commit

## Critique Disposition

Critique: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c2-plan-critique.md (verdict Revise, one run, none needs a user decision, no second critique).

| ID | Severity | Disposition |
|---|---|---|
| PC-001 | High | Applied: doubt rule kept verbatim, qualifier removed (Goals, FR1, details). |
| PC-002 | Medium | Applied: line 68 and the Mixed rows aligned; AC1 inspects every mixed hit. |
| PC-003 | High | Applied: designer gets a required-topics checklist, not scenarios; terminal-state rule in AC3. |
| PC-004 | Medium | Applied: FR3 rewritten with source-backed facts. |
| PC-005 | Medium | Applied: runner-versus-direct out scenario and per-stage identity and proxy fields. |
| PC-006 | Medium | Applied: outputs under the workspace (sandbox-3 or changes record). Earlier C1 /tmp outputs remain as recorded. |
| PC-007 | Low | Applied: AC6 added; allowed paths and status comparison. |

## Follow-Up Items

* Intended-profile rerun when host allows a model selection; hosted CI observation; owner policy gaps listed in the C1 review (RV-003); #470 timing.
