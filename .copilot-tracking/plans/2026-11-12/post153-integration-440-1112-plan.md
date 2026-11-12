<!-- markdownlint-disable-file -->
# Plan: post-153 integration checkpoint for #440 (2026-11-12)

* Task ID: `post153-integration-440-1112`; session `d351ddc0-f4e6-4e5f-ae56-db0937d3ad2b`; branch `docs/post153-integration-checkpoint-440-1112` at `4074b44f3704b860dd4b890473cca620115d3dca`.
* Research: .copilot-tracking/research/2026-11-12/post153-integration-440-1112-research.md (disposition `executed`, Planning Readiness `Ready`).
* Details: .copilot-tracking/details/2026-11-12/post153-integration-440-1112-phase-details.md. Critique: .copilot-tracking/plans/2026-11-12/post153-integration-440-1112-critique.md. Changes record (created by implement): .copilot-tracking/changes/2026-11-12/post153-integration-440-1112-changes.md.

## Executive summary

Planning is for one documentation-and-evidence candidate: a new dated section in the cutover evidence pack, a concise index entry and an append-only log entry, recording bounded integrated evidence for merged PRs #1470 (proposal-card plain-language source) and #1475 (five-home runbook), which the previous checkpoint (PR #1478) explicitly excluded. Observations are already taken and retained outside the repository (19 + 31 + 187 tests with 92 SQL skips, a static runbook link check, `node --check`). No product defect is confirmed; one static accessibility concern (role-less `pre` elements with `aria-label`) and two omissions are routed to existing owners without new issues. Readiness: ready for one critique, then implementation. Nothing here implies live availability, a model call, consent, approval or an issue-criterion tick.

## User Decisions and Requirements

* Existing issue #440, newly due recurring checkpoint; not a new issue or reopened correction campaign; no new correction allowance; no closing keyword or tick.
* Work only in this worktree and branch; primary checkout and other worktrees untouched.
* Documentation plus focused affected observations only; no full gate, Docker, SQL, browser installation, global lint sweep, blanket suite, Azure, credentials, cloud or model calls.
* Record in `docs/architecture/cutover-evidence-pack.md` (new dated section), `docs/reference/README.md` (concise index entry) and `docs/reference/log.md` (append-only entry).
* Separate local observed, implemented-unverified, blocked and unknown; requirement-qualified traceability; actual commands, exits and paths; omissions stated.
* Concrete new findings only, deduplicated against existing owners; no new issues, no product fixes, no scope expansion.
* Do not edit application code, agent instructions, workflows, approvals, requirements, issue criteria or existing adverse artifacts.
* Commit locally with the resolved privacy-safe identity and Copilot trailer; no push, PR, rebase, amend, merge.

## Goals

* G1 Pin identities of merged #1470 and #1475 on current main and their exclusions.
* G2 Record focused current observations for the proposal-card source and the five-home link contract.
* G3 Keep the record honest about scope, omissions and adverse results, and route findings.

## Scope and Non-Goals

* In scope: three documentation files plus original RPI artifacts under `.copilot-tracking/`.
* Non-goals: source or test edits, rerun of the 281-test campaign, browser, live or Azure evidence, new issues, approvals.

## Functional Requirements

* FR-1 The pack section states pins, trees, blobs, document statuses, exclusions and issue states.
* FR-2 It lists each command, exit status, test count and raw path; failed or corrected attempts are retained.
* FR-3 It traces each boundary to a requirement-qualified class (local observed, implemented-unverified, blocked, unknown).
* FR-4 It records findings F1 to F3 with owners and no issue creation.
* FR-5 The index entry and log entry link the section; the log is append-only.

## Non-Functional Requirements

* NFR-1 Markdown style: ASCII, `*` lists, no em dashes, no bolded prefixes; relative links resolve.
* NFR-2 No secrets, private data or `.copilot-tracking/` references in production code or commit message.
* NFR-3 Statements stay within observed evidence; draft, in-review and Proposed are not approvals.

## Acceptance Criteria

* AC-1 Section appended after the 2026-11-12 demo wave section; earlier text unchanged (`git diff` shows additions only in the three files).
* AC-2 Every number in the section matches the raw outputs.
* AC-3 Link and anchor check of changed Markdown passes locally.
* AC-4 Only the three documentation files and new tracking files change; no source path appears in the diff.
* AC-5 One review artifact records execution and outcome; commit is clean and local.

## Phase Checklist

<!-- P01 context: evidence pack section -->
### [x] P01 Pack section

* [x] P01-T01 Append the dated section to `docs/architecture/cutover-evidence-pack.md`.

<!-- P02 context: index and log -->
### [x] P02 Index and log

* [x] P02-T01 Add the index entry in `docs/reference/README.md`.
* [x] P02-T02 Append the log entry in `docs/reference/log.md`.

<!-- P03 context: validation -->
### [ ] P03 Validation and commit

* [x] P03-T01 Check links, anchors, numbers against raw outputs and the diff boundary.
* [x] P03-T02 Complete the changes record, state file and Review artifact before staging; stage exactly the three docs and the new `post153-integration-440-1112` tracking files.
* [ ] P03-T03 Commit locally with the resolved identity and trailer.

## Critique Disposition

One independent critique ran (fresh general-purpose worker, `rpi-plan-critique`), verdict Revise, nine findings, no user decision needed; no second critique runs. All dispositions below are planner-applied directly; none conflicts with a user decision.

| Finding | Disposition |
| --- | --- |
| PC-001 `node --check` unrecorded | Applied: reran on `assistants.js` and `app.js` with retained `.out`/`.exit` and node version; added `command-manifest.txt` and `sha256-manifest.txt` in the raw directory |
| PC-002 skip count wording | Applied: report 187 ran, 95 executed and 92 skipped; the reason is the `MSSQL` gate at `test_quality_sensors.py:1802` ("needs disposable SQL Server (ZF_TEST_MSSQL=1)"); per-test reasons were not captured with `-q`, so the attribution of all 92 is inferred |
| PC-003 false WCAG/design-system statement | Applied: research corrected (`design-system.md:94-95,109`, tables only) |
| PC-004 dedupe unrecorded | Applied: three open-issue searches retained in `dedupe-search.out` returned no match; owners remain proposed by inspection (#153, #132/#134), not confirmed |
| PC-005 origin proof incomplete, `core.sensors` | Applied: `origin-trace.out` hashes 3 test modules and 4 package modules (7 of 7 equal to `HEAD` blobs); `zava_forward.core.sensors` was a guessed module name in the first preflight (real modules are `sensor_*.py`), recorded as an author error, not a product finding; a failed first trace (tests path missing) retained |
| PC-006 string-level five-home check | Applied: stated as string-level and self-referential for id shape; no existence, open-state or browser evidence |
| PC-007 historical 281, omitted tests, `6819456` | Applied: the 281-test campaign is historical and not rerun; `test_workspace_scripts.py` omitted (route allowlist only, not the card); `loading_briefing_browser_check.py` omitted (browser); local commit `6819456` (not an ancestor of HEAD, on a sibling branch) is excluded |
| PC-008 requirement IDs and class table | Applied in P01-T01: name PRD and BRD labels only as nearest by inspection, per-boundary class table |
| PC-009 changes and review records | Applied: P03-T03 added |

## Follow-Up Items

* FU-1 F1 role-less `pre` accessible name: route to #153 or #132 owners (static, unverified).
* FU-2 F2 browser check `assistants_browser_check.py` not run: needs admitted browser harness.
* FU-3 F3 no repository test covers the runbook five-home contract.
* FU-4 Live preflight of the five ids and endpoint: blocked pending owner admission.

## Test ownership lock

Owned: existing tests only (`test_content_standard`, `test_case_journey`, `test_quality_sensors`). Exact removals: none. Maximum additions: zero tests added to the repository; the static runbook check script stays outside the repository. Coverage is regression and static, not semantic acceptance.
