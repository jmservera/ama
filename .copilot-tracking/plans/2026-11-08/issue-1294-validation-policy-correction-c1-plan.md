<!-- markdownlint-disable-file -->
# RPI Plan: issue-1294-validation-policy-correction-c1

## Task Metadata

| Field | Value |
|---|---|
| Task ID | issue-1294-c1 |
| Task slug | issue-1294-validation-policy-correction-c1 |
| Date | 2026-11-08 |
| Branch / base | docs/validation-policy-1294 on origin/main fa7ae0c9770e890f82482456bfcb8e97f1e05429; starts at HEAD 397ce435ae4dddfcf9279179656049b8b670b720 (tree 3a1faa5dc109c8deecf546cec6c3e4077cca2bc6) |
| Research | .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c1-research.md |
| Details | .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c1-phase-details.md |
| Changes | .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-correction-c1-changes.md |
| Local tier | Focused (guide and instruction wording only). HVE classification Major (separate axis). |

## Executive Summary

Correct four independent-review findings on the issue #1294 candidate by wording only: restore the complete employee-chat acceptance contract for direct local checks, fix the false Hosted-only coverage label, replace the categorical full-tier rule for workflow, tool, dependency and Dockerfile edits with impact-based classification, and repeat the behavior test with independent design, honest profile, independent grading and a retained sandbox.

### What You May Not Know

* The direct harness writes `axe-results.json` and prints the marker, so every runner check can be done directly without a wrapper; the runner only copies the JSON first.
* Local `--changed` selecting the full matrix for workflow paths is a conservative selection aid, not a tier rule.
* Host model selection may prevent an intended-profile run; that is recorded as proxy or Deferred, never Pass at the intended profile.

### Unresolved Decisions or Blockers

* None blocking.

## User Decisions and Requirements

* Owner policy: targeted tests in development; small and documentation-only changes use relevant local checks plus applicable hosted checks without a blanket `--changed`; major features, SQL, infrastructure, deployment, security-sensitive changes and releases keep the full gate and verified external receipt.
* Direct employee-chat check preserves pinned axe digest, ordered states, positive integer passes, `PASS employee chat:` marker, no skips, no violations; selector exactly one test, zero skips.
* Fix the Hosted-only label; remove the unconditional full tier for file classes; do not imply those changes are categorically safe.
* Repeat behavior testing independently; retain the sandbox; never delete anything; preserve earlier report and log verbatim.
* No workflow, source, branch-protection, Docker, SQL, Azure, install or push actions.

## Goals

* Guides match the runner and CI facts and the owner's tier categories.

## Scope and Non-Goals

* In scope: .github/copilot-instructions.md, src/README.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, docs/reference/log.md (append), tracking evidence. Non-goals: tools, workflows, source, the earlier review and behavior report, the #470 timing criterion.

## Functional Requirements

* FR1 direct-check text; FR2 Shared / Local-only / Hosted-only structure; FR3 impact-based classification in instructions, README lead, coordinator and examples table; FR4 repeated behavior test with retained evidence.

## Non-Functional Requirements

* ASCII punctuation, no em dashes, `*` lists, relative links resolve, earlier log entries untouched.

## Acceptance Criteria

* AC1 README names the digest, ordered states, positive `passes`, marker, no skips or violations and how each is checked, plus exactly one test and zero skips for the selector.
* AC2 No Hosted-only item with a local counterpart; hosted data-guard job described as its own job.
* AC3 No categorical full-tier wording remains for the four file classes; full tier retained for the owner categories, mixed and unresolved risk; not-categorically-safe statement present.
* AC4 New behavior report with independently designed scenarios, resolved profile label, independent grading or Deferred with blocker; sandbox retained.
* AC5 Link, diff, coverage reproduction and example checks recorded with exits.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct the guide and instruction wording

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Direct employee-chat contract and Shared/Local-only/Hosted-only sections (src/README.md)

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Impact-based classification in copilot-instructions.md, README lead and table, coordinator

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Append correction log entry

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and repeat behavior testing

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Link, diff, coverage reproduction and example checks

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: hve-builder-tester run with independent design and grading, retained sandbox

<!-- rpi:phase id=P03 -->
### [x] P03: Changes record, correction Review, commit

## Dependencies

* P02 depends on P01; P03 depends on both.

## Critique Disposition

Critique: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c1-plan-critique.md (verdict Revise; 2 High, 3 Medium, 1 Low; none needs a user decision). No second critique runs. All applied directly:

| Finding | Disposition |
|---|---|
| PC-001 | Applied. AC1 and P01-T01 require exactly three ordered entries, non-bool integer passes above zero, exit 0, marker in stdout and JSON present, fresh external `--out`. |
| PC-002 | Applied. Selector execution is Shared; exact-count, zero-skip and named-test verification is Local-only; every Shared item cites both locations and flags one-sided verification; full direct selector command given (src/api, runner PYTHONPATH, `ZF_BROWSER_TESTS=1`, `-v`). |
| PC-003 | Applied. Classifier records impact and basis in the changes or review record; focused for these file classes needs a stated reason that permissions, pinned actions or images, packages, secrets, deployment or security controls and gate semantics are unchanged; doubt or mixed takes full; `--changed` full selection is not a tier. |
| PC-004 | Applied. New sandbox path, no reconstruction of the removed one; grader receives the examples table and full contract; designer gets no lead-drafted scenarios; proxy executor or unresolved profile caps the result at proxy or Deferred, never intended-profile Pass; Deferred states the exact rerun condition; scenarios cover zero-pass, wrong-state, selector with a skip, categorical-tier phrasing. |
| PC-005 | Applied. Stale phrases listed in details; file-scope diff check; bytecode disabled; exits recorded; no `--changed` run claimed. |
| PC-006 | Applied. P03 states repository-local noreply email, preserved earlier review and behavior report, no push, hosted CI not run; independent exact-head review, human and hosted approvals remain required and not yet obtained. |

## Follow-Up Items

* Host the employee-chat harness in CI, add zero-skip verification to the hosted selector, #470 timing (carried from the original plan; workflow changes unauthorized here).
