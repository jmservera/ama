<!-- markdownlint-disable-file -->
# Plan: live-acceptance-1030c

Task ID: live-acceptance-1030c-2026-10-30. Date: 2026-10-30.

## Executive Summary

Run a capture-free live browser acceptance rerun on both authorized sites,
not a product repair. Warm first, allow slow callback, require authoritative
employee admission, and retain a complete 24-row evidence matrix. Unobserved
criteria remain unproven. Commit locally; no push or issue mutation.

## User Decisions and Requirements

* Full ordered Research, Plan, Implement, Review; dated artifacts; local commit.
* Refs #550, Refs #551, Refs #552, Refs #563 only, no closing keywords.
* Two sign-in attempts maximum per site using only the supplied files.
* Warm both /healthz with >=120s timeout/retries; cold starts are not feature failures.
* Resident AI disabled: rat reply explains unavailable AI and human route, no AI label.
* Employee Aadi password login, slow callback, /api/me, chat, map and case.
* Never emit credentials, screenshots, traces, HAR, cookies, tokens or private payload.
* No Azure resource changes and no assistive-technology/conformance claim.

## Sources

Research: .copilot-tracking/research/2026-10-30/live-acceptance-1030c-research.md.
Current source checks C3-C7 and issue bodies W1-W4 define bounded predicates.

## Goals

Determine fresh live behavior and separate accepted sub-observations from
whole compound acceptance. Preserve earlier adverse records unchanged.

## Scope and Non-Goals

Tracking-only runner, safety tests, aggregate JSON and dated RPI records.
No application changes, remote writes, enabled-model execution or AT testing.
No baseline density comparison without a trusted deployed-before baseline.

## Functional Requirements

Warm both origins; count fresh login launches durably before browser activity.
One credential submission per attempt; no resubmission after uncertain delivery.
Read literal trimmed lines only inside runner. No provider text capture.
Employee must pass strict /api/me schema, expected account identity,
trusted-proxy provider, programme-manager role and non-view-only projection.
Resident must reach authenticated own-case page after actual form login.
Inspect rendered native controls, chat persistence/scroll/input/selection,
consent ordering, actual rat fallback, actual map API/marker agreement,
case icons, blocker disclosure and tab/panel geometry at desktop/narrow widths.
Do not intercept or fabricate backend responses.

## Non-Functional Requirements

120s navigation/request timeouts; up to 180s callback settling after submit.
Use boolean/numeric/allowlisted-status evidence only. No raw DOM, response,
exception, URL/query, identity, network headers or request bodies.
Disable all captures; close contexts in finally; output source hash and UTC.
Exclusive manifest prevents accidental re-execution beyond this task's cap.

## Acceptance Criteria

Every step records command/action, timestamp and result, including blocked
branches. A 24-entry issue matrix distinguishes Proven, Partial and Unproven.
Disabled-AI behavior may prove fallback but cannot prove enabled-AI criteria.
No whole compound pass when any required subpart is missing.

## Test Ownership and Output Budget

Owner: parent implementation. Removals: none. Maximum additions: one runner,
one offline test module, one manifest and one aggregate evidence JSON, plus
the five phase records, critique, review and session state. Canonical code:
tracking runner/tests only. Generated targets: manifest/evidence only.
Offline semantic coverage: literal parser, exclusive guard, attempt cap,
strict boolean projection and output secret exclusion. Live regression
coverage: actual browser/API predicates, never fixture substitutions.
Validate syntax/tests, targeted Ruff if available, JSON/hash consistency,
diff whitespace and complete external local gate after commit.

## Phase Checklist

<!-- P01 -->
### P01: Guarded live execution

* [x] P01-T01: Implement/test guarded runner and warm both sites.
* [x] P01-T02: Execute resident and employee bounded authentication and checks.

<!-- P02 -->
### P02: Evidence reconciliation and persistence

* [x] P02-T01: Record all 24 decisions, limitations and commands.
* [ ] P02-T02: One independent Review; local Refs-only commit and complete gate attempt.

## Critique Disposition

One critique executed, original verdict Revise preserved at
.copilot-tracking/plans/2026-10-30/live-acceptance-1030c-critique.md.

* PC-001 rejected: its asserted prohibition on /tmp is not present in the
  caller, current environment or repository instructions. Existing runtime
  import succeeded without installation; documented gate explicitly owns
  its /tmp lock. No bypass or altered gate is authorized.
* PC-002 applied: reject diagnostic environment, disable core dumps and all
  captures, exact-origin checks before secrets, fixed-code errors only,
  finally cleanup and synthetic-canary output tests.
* PC-003 applied: atomic observation map in details; compound missing evidence
  always prevents whole-row Proven.
* PC-004 applied: exact paths, commands, stage allowlist and durable guard tests
  below. No second critique. Implementation readiness: Ready.

Runner/test/generated targets under
.copilot-tracking/changes/2026-10-30/live-acceptance-1030c/:
acceptance.py, test_acceptance.py, manifest.json, evidence.json.
Command: `/tmp/mv/bin/python -B -m unittest discover -s
.copilot-tracking/changes/2026-10-30/live-acceptance-1030c -p 'test_*.py' -v`.
Stage allowlist: these four files and exactly this task's research, plan,
details, critique, changes, review and state records. General gate discovery
does not substitute for the explicit offline test command.

## Follow-Up Items

Enabled-model and human/AT acceptance remain outside this rerun.

## Implementation-Time Amendment

First run proved resident observations but employee admission remained unknown
after KMSI and 180s. Use the second/final authorized employee launch only after
the first completed context/browser cleanup and KMSI delivery evidence is
verified. Original runner/manifest/evidence remain immutable. Add exactly
second/attempt2.py, second/manifest.json and second/evidence.json under the
owned evidence directory; explicit test module remains the same. Preserve
failed binding booleans and final origin predicates. No second critique.

## Handoff

Details: .copilot-tracking/details/2026-10-30/live-acceptance-1030c-phase-details.md.
Changes target: .copilot-tracking/changes/2026-10-30/live-acceptance-1030c-changes.md.
