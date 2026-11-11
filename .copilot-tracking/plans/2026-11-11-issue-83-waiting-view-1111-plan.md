---
title: Issue 83 read-only handoff waiting-time screen plan
ms.date: 2026-11-11
task_id: issue-83-waiting-view-1111
---

## Executive Summary

Add one read-only staff screen, `#/handoff-waiting`, that renders the existing scoped `GET /api/handoffs/unaccepted` projection (elapsed hours, recorded as-of, chase owner, status, supplied reasons, escalation state) with an explicit scope statement, reached by a permanent link in the list-view header row. No API, core, persistence, permission, threshold, scheduling, escalation or CSV change. Failure or malformed payloads show a fixed alert and no table. Tier: focused. Whole #83 stays unaccepted: OD-09 approved times and operational acceptance are not supplied, so C3 is not ticked. Readiness: Ready after one critique (see Critique Disposition).

* Research: `.copilot-tracking/research/2026-11-11-issue-83-waiting-view-1111-research.md`
* Details: `.copilot-tracking/details/2026-11-11-issue-83-waiting-view-1111-phase-details.md`
* Critique: `.copilot-tracking/plans/2026-11-11-issue-83-waiting-view-1111-plan-critique.md`
* Changes record (created by Implement): `.copilot-tracking/changes/2026-11-11-issue-83-waiting-view-1111-changes.md`

## User Decisions and Requirements

* Owner directs demo delivery of existing issues; no new tickets or duplicate implementations (brief).
* Expose the existing scoped read-only waiting-time projection in an accessible staff UI with existing Fluent 2 components; explicit scope; not confused with "waiting for you" (brief).
* Reachable even when the personal pending list is empty; smallest coherent entry point chosen by investigation (brief; research C5, C6).
* Show elapsed time, recorded as-of, existing chase owner, supplied reason and status; keep Unknown or no approved global response time and manual case navigation (brief).
* Preserve the pending list and the delivered CSV download; no new fields, route, persistence, permissions, thresholds, scheduling, automated escalation, provider or cloud call (brief).
* Failure or malformed load is visible, never empty or success; no raw API exception text (brief).
* Focused validation only; no installs unless a command fails for a missing prerequisite; no full gate, SQL, image build, deploy, push, PR, board or issue edits (brief).
* One initial increment; no post-review correction batch; historical correction balance recorded honestly (brief; research).

## Goals

* Staff can see how long each unaccepted handoff has waited and who chases it, from one screen, without it being mistaken for a lateness or escalation decision.

## Scope and Non-Goals

* In scope: `src/api/src/zava_forward/api/web/app.js` (view, header link, route, route status label), one new test file under `src/api/tests/`, a short `src/api/README.md` section.
* Non-goals: API or core change, new navigation item, thresholds (`max_age_hours` is never sent), actions or escalation buttons, scheduling, CSV change, resident names, OD-09, role matrix changes, acceptance edits.

## Functional Requirements

* FR1: link "Handoff waiting times" in the list header row of both list views to `#/handoff-waiting`.
* FR2: the view makes one `GET /api/handoffs/unaccepted` (no query) and no mutation.
* FR3: scope text states this is every not-yet-accepted handoff the role can see, is not the "Handoffs waiting for you" list, and has no approved global waiting-time limit so age alone is not lateness or escalation.
* FR4: table columns Case (manual link to `#/case/{id}`), Status, Waiting (hours), Due, Chase owner, Proposed receiver, Escalation (text: already escalated, needs escalation with supplied reasons, or no escalation reason recorded); single recorded as-of line.
* FR5: empty array shows a plain "No unaccepted handoffs are visible to your role" status, without as-of.
* FR6: non-array, non-object row, missing or non-finite fields, non-null `approved_limit_hours`, unparseable as-of, or any request failure show a fixed alert (owner, next action) with a re-check button, no table and no server message text.
* FR7: route status label "Handoff waiting times" instead of "Case workspace", set where `destination?.scope` is computed in `route()`; dispatch after the contractor and no-case-service guards, before the list fallback.
* FR8: two fixed failure messages: 403 (this account cannot view handoff waiting times) and any other failure or malformed payload (could not load; owner application support; refresh).

## Non-Functional Requirements

* Native semantics: h1, link, button, table with caption and `th scope`, `table-scroll` region, `role="status"` loading, `role="alert"` failure; non-colour status; no new animation; no new CSS unless needed; ASCII text; plain-language content standard.
* Existing `pendingHandoffs` behaviour and Node slice markers unchanged.

## Acceptance Criteria

* AC1: Node cases: success, due-reason, merely-old no-reason, already escalated, empty, transport error, HTTP error, malformed, non-null limit, abort; no mutation call; one GET path only.
* AC2: Chromium (`ZF_BROWSER_TESTS=1`) loopback: link reachable by keyboard from My cases with no card; table shows elapsed hours and as-of; card load failure does not block it; failure and malformed show alert without table; no non-login POST.
* AC3: existing handoff guidance, download, API, role endpoint inventory tests and `node --check app.js` pass; Ruff and mypy configured checks pass for the new test file.
* AC4: commit is local only, frozen, identity privacy-safe, Conventional Commit with trailer.

## Phase Checklist

* [x] P01 View, route and entry link in `app.js`
* [x] P02 Focused tests
* [x] P03 README note and focused validation
* [ ] P04 Original Review

## Critique Disposition

One independent critique ran (fresh general-purpose worker activating `rpi-plan-critique`, verdict Revise, 1 High, 3 Medium, 2 Low). No second critique runs. Compatible planner-direct findings were all applied; none conflicts with a user decision; no user decision was needed.

| Finding | Disposition |
| --- | --- |
| PC-001 High | Accepted. P02 adds a Chromium case where `/api/handoffs` returns `[]` and `/api/handoffs/unaccepted` returns rows, labelled as a constructed response because real data cannot produce it (same scope, research C5). Node stub case retained. |
| PC-002 Medium | Accepted. Test budget raised to match AC1/AC2 (about 12 Node scenarios, 6 Chromium methods); due versus merely old comes only from server `escalated`, `needs_escalation`, `reasons` (no client clock); a Node case proves an old row with no reasons is not labelled late. |
| PC-003 Medium | Accepted. Keyboard cases cover entry link, case link and re-check button, plus failure-state button. |
| PC-004 Medium | Accepted. Two fixed messages: 403 (this account cannot view handoff waiting times; ask a programme owner) and other failure or malformed (could not load; owner application support; refresh). HTTP-error test splits into 403 and 500; a 200 non-JSON body (arrives as `{}`) is a malformed case. |
| PC-005 Medium-Low | Accepted. FR7: in `route()` the scope label is chosen where `destination?.scope` is computed (before dispatch); the dispatch line sits after the contractor and `services.cases === false` guards and before the list fallback. |
| PC-006 Low | Accepted. P01 precondition: web guidelines fetched 2026-11-11 (W1) and read before editing; Node slice markers are `const WAITING_READ_ERROR` through the end of `handoffWaitingView`; this section replaces the placeholder. |

## Follow-Up Items

* OD-09 approved times, escalation routes, scheduling and operational acceptance (human decision; outside this task).
* Optional later: navigation entry for administrators; resident name column would need an API change (not authorised here).
