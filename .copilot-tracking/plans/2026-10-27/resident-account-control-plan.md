---
title: Resident account control implementation plan
ms.date: 2026-10-27
---

Task: #467. Parent: #466. Status: complete; PR #471 open, approvals pending.

## Executive Summary

Reuse the employee site's native account disclosure at the resident header's
right edge. Show only the current authorised account email and existing logout.
Keep authorisation, sign-in/out and focus behavior; add focused regression and
local real-HTTP/browser checks. No cloud, SQL, cap change or UI framework swap.

## Sources

`.copilot-tracking/research/2026-10-27/resident-account-control-research.md`
C1-C5/W1; owner request and issue #467.

## User Decisions and Requirements

* Top-right account identity and sign out matching employee UI.
* Native semantics, keyboard/screen-reader operability and narrow-width support.
* Preserve own-case-only behavior and expose no other account's email.
* Full ordered RPI loop with genuine dated evidence.
* Focused tests, API unit suite, Ruff/mypy changed Python, local Playwright.
* Stack PR on `feat/resident-interactive`, use Refs only, no force push/merge.
* No full gate, Azure, SQL changes, secrets/private datasets or MAX_MAPPINGS edit.

## Goals

Make logout discoverable in a familiar, accessible header account control.

## Scope and Non-Goals

Resident demo assets, its authorised view projection, API tests, one bounded
browser check and directly related API README. No core authorization changes,
account switching, staff UI changes, images, persistence or dependency changes.

## Functional Requirements

Use details/summary with a visible Account label and panel containing own email
and Sign out. Render identity with textContent, only from authorised view.
Collapse on Escape (focus summary), outside click, logout and denied/signed-out
states; clear hidden email. Reload must restore the correct account identity.

## Non-Functional Requirements

Existing Fluent-derived tokens and visible focus; no added animation. Header
wraps without horizontal overflow at 320px, including long emails. Existing
logout success/failure announcements and focus targets remain unchanged.

## Acceptance Criteria

Top-right disclosure accessible by name and native Enter/Space; Tab reaches
logout; Escape returns summary focus. Successful logout clears account and
case, focuses sign-in heading and revokes session. Failed logout hides account/
case and retains honest recovery. Separate sessions and forged/expired/revoked
sessions never disclose another account. Reflow checked at 320/390/1280px.

## Phase Checklist

<!-- P01 -->
### P01: Implement bounded account control

* [x] P01-T01: Add authorised own email and header disclosure/styles/handlers.
* [x] P01-T02: Update API contract coverage and add focused real-app browser check.
* [x] P01-T03: Document behavior; run checks and record exact results.

<!-- P02 -->
### P02: Independent review and publication

* [x] P02-T01: One independent post-implementation Review; route findings.
* [x] P02-T02: Commit and open stacked PR; no merge.

## Locked Test Ownership and Validation

API owns projection and UI regressions. Core remains unchanged; run its resident
showcase tests as an extra focused check. No test removals. Maximum additions:
four API test methods and one browser check file, using existing synthetic
FakeReader/Clock fixture and actual HTTP server, never SQL or private stock.
Update exact-shape and intentional own-email assertions, preserving other-email
exclusions. Browser covers semantic/keyboard/reflow and logout success/failure;
HTTP tests retain authority/isolation regression coverage. No generated targets.
Run full API unittest discovery, focused core resident-showcase tests, changed
Python Ruff/format/mypy and JS syntax, then local Chromium. Hosted CI/rubric/
human review remain pending; no WCAG conformance claim.

## Critique Disposition

One independent critique executed: Revise, PC-001 (Medium). Directly resolved
by the exact validation target map below. No user decision needed, no repeat.

| Target / owner | Locked command or assertion |
| --- | --- |
| API unit suite | From src/api: `PYTHONPATH=../core/tests:../agents/tests /tmp/ama-467-venv/bin/python -m unittest discover -s tests -q` |
| API assertions | Amend SignInTests.test_login_shows_only_own_allowlisted_view; add at most four methods covering own account/session-only anonymity, denied/revoked/expired identity and header semantics |
| Focused core | From src/core: `/tmp/ama-467-venv/bin/python -m unittest discover -s tests -p test_resident_showcase.py -q`; exclude SQL/verifier siblings |
| Browser | New src/api/checks/resident_account_check.py; from src/api: `PYTHONPATH=tests /tmp/ama-467-venv/bin/python -m checks.resident_account_check`; actual loopback app, all browser acceptance scenarios above |
| Static Python | From src/api: Ruff check/format and mypy on src/zava_forward/api/resident_demo/app.py, tests/test_resident_demo_api.py, checks/resident_account_check.py |
| JavaScript | `node --check src/api/src/zava_forward/api/resident_demo/web/demo.js` from root |

Implementation-time current-state update: adapt the four existing SQL browser
harness logout access sites to open the native disclosure first. This maintains
the existing check for hosted/later use; it does not authorize running it or
accessing SQL. Include that changed harness in Ruff/mypy. No new test methods,
infrastructure or generated targets; addition ceilings unchanged.

## Follow-Up Items

None currently established. Formal human accessibility acceptance is outside
this small implementation and is not inferred from automated browser checks.

## Handoff

P01 complete: two added API methods, authorised email, native header account,
browser coverage and compatibility adaptation, documentation, static checks
and full API unit evidence recorded. No implementation blocker or open finding.
One independent Review executed: Complete / Conformant, no substantive findings.
P02-T02 complete: implementation/evidence commit fab2d93d, normal push and
PR #471 opened against feat/resident-interactive with explicit stacking
dependency and Refs #467 / Refs #466 only. No merge or force push.
Hosted CI/rubric/owner review remain pending; no new child work selected.
Changes: `.copilot-tracking/changes/2026-10-27/resident-account-control-changes.md`.
