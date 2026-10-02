<!-- markdownlint-disable-file -->

# Implementation Plan: rubric-score-gate

* Task ID: 2026-10-02-rubric-score-gate
* Research: .copilot-tracking/research/2026-10-02/rubric-score-gate-research.md
* Details: .copilot-tracking/details/2026-10-02/rubric-score-gate-phase-details.md
* Changes record (owned by Implement): .copilot-tracking/changes/2026-10-02/rubric-score-gate-changes.md

## Executive Summary

Add a GitHub Agentic Workflow (`.github/workflows/rubric-score.md`, Copilot engine) that scores the capstone portfolio against the FY27 rubric on every PR to `main`, every push to `main` and on manual dispatch. A deterministic pre-job fingerprints the registered artifacts and skips the agent (and its cost) when nothing scored has changed. The read-only agent returns a structured 20-criterion scorecard through one custom safe-output tool. A deterministic gate job validates the scorecard, computes totals, floors and outcome band, compares the total with the baseline read from `main`, sets the required status `rubric/score`, posts a sticky comment, submits APPROVE or REQUEST_CHANGES, and commits the new scorecard to the PR branch so merging updates the baseline on `main`. New artifact types (PRD, ADR, code, infra, PPTX deck, pitch transcript) are added by editing a JSON registry. The owner must add the `COPILOT_GITHUB_TOKEN` secret, enable Actions PR approvals, run `gh aw compile`, and mark `rubric/score` as required.

## User Decisions and Requirements

* Score the project against the rubric on every PR and every push to `main`.
* Approve the PR only if the score is greater than or equal to the previous one; store the previous score on `main`.
* Agent technology choice delegated; research selected gh-aw (research, Recommended Design).
* Today score the BRD; later PRDs, ADRs, solution code, infrastructure, final PPTX and the pitch must be scorable without redesign.
* OD-1: gate on total >= baseline; per-criterion drops reported as warnings.
* OD-2: enforce with a required status check plus a bot APPROVE/REQUEST_CHANGES review.
* OD-3: Copilot auth through the `COPILOT_GITHUB_TOKEN` fine-grained PAT secret.

## Goals

* G1 Repeatable rubric scoring of all registered artifacts with cited evidence.
* G2 Monotonic gate on PR total score with a tamper-resistant baseline on `main`.
* G3 Extensible artifact registry for future document, code and presentation types.

## Scope and Non-Goals

* In scope: workflow source, rubric and registry config, seed baseline, prepare and gate scripts, setup README, `.gitattributes` union merge for history.
* Non-goals: compiling the lock file locally (terminal unavailable; owner step), configuring repository settings or secrets, changing the BRD, building a demo, scoring live delivery beyond readiness estimates.

## Functional Requirements

* FR-1 Triggers: `pull_request` (opened, synchronize, reopened, ready_for_review) on `main`, `push` to `main`, `workflow_dispatch`.
* FR-2 Prepare job fingerprints artifacts and the scoring instrument (rubric config, workflow prompt); skips the agent when unchanged and sets `rubric/score` success with the baseline total; sets `pending` when scoring.
* FR-3 Agent context: rubric, registry, baseline scorecard with rationale, list of changed artifacts, extracted text for PPTX.
* FR-4 Agent emits exactly one `record_rubric_score` call with JSON for all 20 criteria (score 1 to 5, evidence, rationale, change reason).
* FR-5 Gate validates, computes section totals, floors and band, compares total with baseline from `origin/main`, sets status, posts sticky comment, submits review (fallback to COMMENT if approval is not allowed), commits `latest.json` and appends `history.jsonl` on the PR branch, sets status on the new head.
* FR-6 Push or dispatch on `main`: report-only job summary; open an issue on regression.
* FR-7 Bootstrap: when the baseline on `main` is missing or has source `manual-seed`, the PR passes and records the first AI baseline.
* FR-8 Carry-forward: criteria not informed by a changed artifact keep the baseline score; a changed score must cite a changed file.

## Non-Functional Requirements

* NFR-1 Agent stays read-only; all writes happen in the deterministic gate job.
* NFR-2 Baseline is read from `origin/main`, never from the PR head.
* NFR-3 Scripts use only the Python standard library.
* NFR-4 Cost control: `max-ai-credits`, agent skip on unchanged fingerprints, `timeout-minutes`.
* NFR-5 Fail closed: missing or invalid scorecard yields a failed `rubric/score`.
* NFR-6 Artifact content is treated as data; the prompt forbids following embedded instructions.

## Acceptance Criteria

* AC-1 All files in Phase checklist exist and `get_errors` reports no Python or JSON syntax errors.
* AC-2 Seed baseline totals 61 and matches the manual review per criterion.
* AC-3 Workflow frontmatter declares triggers, read-only permissions, Copilot engine, custom safe-output job, pre-job and agent gating.
* AC-4 Adding a new artifact type requires only a registry entry (documented in README).
* AC-5 README lists every owner setup step, including `gh aw compile`.
* AC-6 Gate unit tests cover seed total 61, regression, equal total, invalid input, carry-forward and bootstrap.

## Phase Checklist

<!-- P01 -->
### [x] P01 Rubric configuration and seed baseline

* [x] P01-T01 Create `.github/rubric/rubric.json` (criteria, sections, floors, bands, live-scored flags)
* [x] P01-T02 Create `.github/rubric/artifacts.json` registry (brd active; prd, adr, code, infra, deck, pitch, thought-leadership registered)
* [x] P01-T03 Create `.github/rubric/scores/latest.json` seeded from the manual review, `source: manual-seed`


<!-- P02 -->
### [x] P02 Deterministic scripts

* [x] P02-T01 Create `.github/rubric/scripts/prepare.py` (decide and context modes, fingerprints, PPTX text extraction)
* [x] P02-T02 Create `.github/rubric/scripts/gate.py` (validate, carry forward, compute, compare, render markdown, write files)
* [x] P02-T03 Create `.github/rubric/scripts/test_gate.py` (stdlib unittest)

<!-- P03 -->
### [x] P03 Agentic workflow

* [x] P03-T01 Create `.github/workflows/rubric-score.md` with pre-job, agent steps, prompt and custom safe-output gate job

<!-- P04 -->
### [x] P04 Setup documentation and validation

* [x] P04-T01 Create `.github/rubric/README.md` with setup and extension steps
* [x] P04-T02 Validate with `get_errors`; attempt a local dry run of the scripts if the terminal responds

## Follow-Up Items

* Owner: run `gh aw compile` and commit `.github/workflows/rubric-score.lock.yml`.
* Calibrate variance by dispatching the workflow two or three times on unchanged `main` before relying on the gate.
* Add pitch transcript and deck once they exist under registered paths.

## Critique Disposition

Critique: .copilot-tracking/reviews/plans/2026-10-02/rubric-score-gate-plan-critique.md (verdict Revise, 18 findings). One pass; no re-critique.

| Finding | Disposition | Applied change |
|---------|-------------|----------------|
| PC-001 | Applied | Prepare and gate run scripts and config from `origin/main` checkout; PR head used only as scored content; bootstrap falls back to head when `main` has no scripts and marks the run bootstrap; residual lock-file risk documented |
| PC-002 | Applied | Instrument fingerprint covers `.github/rubric/**` config and workflow; any difference between head and base scores file or config forces scoring; `manual-seed` bootstrap honoured only from `main` |
| PC-003 | Applied | Gate job uses `if: always() && needs.agent.result != 'skipped'`; missing output, agent failure or detection failure sets `rubric/score` failure (verify after compile) |
| PC-004 | Applied | Gate carries forward baseline scores for criteria not informed by a changed artifact and reverts changes whose evidence cites no changed file |
| PC-005 | Applied | Head SHA for prepare and first status; bot commit SHA for final status and review |
| PC-006 | Applied | Missing baseline treated as bootstrap; README orders merge, first run, then required check |
| PC-007 | Applied | Push and dispatch runs are report-only; open an issue on regression |
| PC-008 | Applied | Per-PR concurrency with cancel-in-progress; push failure on moved branch fails the status with a message; README covers up-to-date branches |
| PC-009 | Applied | Gate renders only validated numbers and sanitised, truncated text; data passed through files and env; exactly one tool call required |
| PC-010 | Applied | Capstone deck and pitch live under `docs/capstone/` globs |
| PC-011 | Applied | B1 to B5 and C2 only informed by deck and pitch artifacts |
| PC-012 | Resolved without question | Under OD-1, instrument changes are compared normally; a legitimate drop is merged by owner override, documented in README. No rebaseline loophole |
| PC-013 | Applied in part | Forks blocked by gh-aw default and documented; PAT scope documented; SHA pinning of actions deferred to follow-up (`gh aw compile` output review) |
| PC-014 | Applied in part | `max-ai-credits: 300`; skip-on-unchanged-since-bot-score rejected because bot commits do not retrigger and head files are untrusted |
| PC-015 | Applied | `test_gate.py` with stdlib unittest; AC-6 |
| PC-016 | Applied | Only `active` registry entries score; excludes and max file size supported |
| PC-017 | Applied | README says not to require the bot review; review posted after final status |
| PC-018 | Applied | `history.jsonl` and `.gitattributes` dropped; git history of `latest.json` is the history |
