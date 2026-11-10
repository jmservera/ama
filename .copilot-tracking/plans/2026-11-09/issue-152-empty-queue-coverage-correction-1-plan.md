<!-- markdownlint-disable-file -->

# Implementation Plan: issue-152-empty-queue-coverage-correction-1

| Field | Value |
|---|---|
| Task ID | issue-152-empty-queue-coverage-correction-1 |
| Date | 2026-11-09 (prospective, written before source edits) |
| Parent task | issue-152-empty-queue-coverage (preserved unchanged) |
| Research | .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-1-research.md |
| Details | .copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-correction-1-phase-details.md |
| Critique | .copilot-tracking/challenges/2026-11-09/issue-152-empty-queue-coverage-correction-1-critique.md |
| Changes (implement phase) | .copilot-tracking/changes/2026-11-09/issue-152-empty-queue-coverage-correction-1-changes.md |
| Tier | focused |

## Executive Summary

The My cases empty-state helper can currently say "declared gap, fixture X declared by Y" on the strength of two non-empty strings in the same `/api/me` payload. No authoritative current fixture or provenance exists to check them against, and no server produces the declaration. The correction defers and removes the declared branch: an empty unfiltered own queue always says coverage is unknown, whatever `work_queues.coverage` contains. A regression reproduces the stale/unrelated/unverified provenance case. No-match, populated and all-cases behaviour is unchanged. README and test docs state what is active. This is a first correction of a partial C5 slice (`Refs #152`); it does not deliver AC-034/043, device, accessibility, user or deployment claims. Browser, `--changed`, independent review and hosted checks remain with the coordinator.

## User Decisions and Requirements

* Work only in this worktree and branch; do not rebase, push, open a PR or change the target. Preserve original artifacts and original Residual work review.
* Without an independently authoritative current fixture and provenance binding, keep coverage unknown. Do not invent a trusted source, add a producer, schema, SQL, data, identity or permission change, or infer authority from role, source text, timestamps, static manifests or queue emptiness.
* The simplest safe result may remove the declared branch.
* Add a focused regression for stale/unrelated/unverified provenance; keep no-match, unknown, populated-queue and all-cases behaviour; README and tests must describe what is active.
* Focused tier. Stop for coordinator reassessment on auth, SQL, deployment, security-sensitive or other full-tier needs.
* Activate and apply web-design-guidelines before web edits and again before review; report `file:line`.
* Run only lightweight targeted unit and static checks; no changed/full gates, browser, SQL or Docker.
* Commit with repository-local privacy-safe identity, Conventional Commit, `Refs #152`, Copilot co-author trailer.

## Goals

* Restore the fail-closed requirement: no declared-unrepresented claim without trustworthy provenance, which does not exist.

## Scope and Non-Goals

* In scope: `src/api/src/zava_forward/api/web/app.js` empty-queue helper and its call site; `src/api/tests/test_queue_empty_state.py`; the empty-queue paragraph of `src/api/README.md`; correction RPI artifacts; one knowledge-base log entry only if a knowledge-base file changes (none planned).
* Non-goals: producer, schema, server, SQL, data, identity, permissions, deployment, manifest status semantics (original F2), browser checks, AC-034/043 completion.

## Functional Requirements

* FR1: an empty unfiltered own queue always yields state `coverage-unknown` with the existing unknown copy, regardless of any `work_queues.coverage` value.
* FR2: no-match, `empty-all` and populated (`null`) outputs are unchanged.
* FR3: the `declared-unrepresented` state and text no longer exist in the client.

## Non-Functional Requirements

* Plain-language copy unchanged; polite live-region and keyboard paths untouched; no new dependency; Fluent 2 and WCAG baseline untouched because only the removed branch changes.

## Acceptance Criteria

* AC1: a regression with matching contract, as-of, policy and role but `fixture_version` `stale-or-unrelated-fixture` and `source` `unverified declaration` yields `coverage-unknown`, and a well-formed declaration also yields `coverage-unknown`; the regression fails on the original source.
* AC2: no-match, unknown, populated, all-cases and call-site wiring tests pass.
* AC3: grep across `src`, `tools` and `docs` finds no `declared-unrepresented`, `trustedCoverage`, declared-gap copy, `work_queues.coverage` consumer or `fixture_version` consumer outside this correction's tests and preserved tracking; hits in unrun browser checks go to the coordinator.
* AC4: README says the declared state is deferred and any `coverage` field is ignored; claims no completion of AC-034/043.
* AC5: targeted unit test, `node --check`, `git diff --check` and markdown link review exit 0; unperformed checks are disclosed.

## Phase Checklist

<!-- P01 -->
### [x] P01: Remove the declared branch and correct tests

* [x] P01-T01 Remove `trustedCoverage`; reduce `queueEmptyExplanation` to filter/scope/unknown and drop `coverage`, `ctx` parameters and call-site arguments.
* [x] P01-T02 Rewrite `test_queue_empty_state.py`: add the stale/unrelated/unverified regression plus a well-formed-declaration-still-unknown case; remove declared-state tests; keep the others; update wiring test.

<!-- P02 -->
### [x] P02: Documentation and validation

* [x] P02-T01 Update the `src/api/README.md` empty-queue paragraph.
* [x] P02-T02 Fetch web-design-guidelines, run targeted checks, confirm the regression fails on the original source (original `trustedCoverage` plus `queueEmptyExplanation` with original arguments, actual failing state `declared-unrepresented`), record changes noting this correction supersedes the preserved parent artifacts' declared-state claims.
* [x] P02-T03 Commit with repository-local privacy-safe identity, Conventional Commit, `Refs #152`, Copilot trailer; record head and tree. Refresh web-design-guidelines in Review.

## Dependencies and Risks

* P02 depends on P01. Risk: removal changes the helper signature; wiring test updated. Browser expectations in unrun Playwright checks are not asserted here.

## Critique Disposition

Critique executed once, verdict Revise, no Critical/High findings; all four applied directly, no user decision needed, no second critique.

| ID | Severity | Disposition |
|---|---|---|
| PC-001 | Medium | Applied: P02-T02 and details run the regression against original `trustedCoverage` plus original function and arguments; expected failing state `declared-unrepresented`. |
| PC-002 | Medium | Applied: AC3 widened to `src`, `tools`, `docs`; unknown copy re-read for accuracy in P01-T01. |
| PC-003 | Low | Applied: P02-T03 owns commit and review-time refresh. |
| PC-004 | Low | Applied: changes record states supersession of parent declared-state claims. |

## Follow-Up Items

* F1 Owner decision on a dataset-owned runtime coverage producer with authority binding (original F1; out of scope).
* F2 Manifest status semantics (original F2).
* F3 Exact-head `--changed`, Playwright, independent review and hosted checks (coordinator).
