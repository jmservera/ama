---
title: Resident logout browser-check correction research
ms.date: 2026-10-28
---
<!-- markdownlint-disable-file -->

## Research Brief

Correct PR #525 thread PRRT_kwDOUU8JX86xVDWZ for issue #520. Investigate both
SQL-browser logout assertions, related checks and validation commands. Output
mode: convergence. Audience: implementer and independent reviewer.

## Research Parameters

Focused posture, selected for the caller's named internal defect. Evidence root:
`.copilot-tracking/`. No application behavior changes, Azure, secrets or `.env`
reads. Preserve no-Set-Cookie logout and PR `Refs #520`. Heavy lock acquisition
must use nonblocking attempts for no more than 40 minutes.

## Extension Registry and Participation

Repository instructions and RPI phase skills selected. No UI source changes:
design skills are not applicable. Research stays inline because the continuous
trace is small. Independent critique and final Review will use bounded agents.
No interaction needed: the user expressly requested all four phases and publication.

## Research Questions and Prior Knowledge Gate

* Q1: Which logout checks incorrectly depend on cookie deletion?
* Q2: How can rejection prove revocation rather than a missing request fence?
* Q3: Which SQLite and SQL Server browser commands cover the correction?

Starting evidence: caller thread, current browser check and API unit test.
Branch is clean, open PR head is `feat/resident-chat-520`, and fetched remote
has no ahead commits at intake (`32877254ec92a6aba409a1f43b26a66a52c706e1`).
No pull is needed; no bot commit is pending.

## Direction Controls

Preserve the application fence against delayed logout response cookies. Search
other tests/checks, use Ruff limit 100, validate relevant API units and resident
browsers, commit dated evidence, push normally, reply and resolve only the named
thread. Do not infer issue closure or human acceptance.

## Research Cycle Log

### Cycle 1: Wider

Inspected the named browser check and searched API tests/checks for logout,
cookie clearing/deletion and signed-out state. Two stale success assertions
appear in `check_cross_case_and_logout` and `check_logout_failure`. The unit
test already asserts retained cookie, no Set-Cookie, codec revocation, view 401
and signed-out session. Reflection: this is check drift, not an application bug.

### Cycle 1: Deeper

The session endpoint returns HTTP 200 with `signed_in` and nullable `session_id`.
View requests are fenced by `X-Resident-Session`. Capture the original session ID
before logout and use it for denial checks. Existing unit tests already enforce
the desired contract. The assistant browser uses SQLite callback storage and
has no `--mssql` option. The named demo browser always uses real SQL Server;
there is no SQLite variant or `--mssql` option.

### Cycle 1: Contrarian

A missing fence could make a denial assertion vacuous. Use the original session
ID alongside the retained token, including the independent replay context.
Cookie absence assertions in the unit module apply to failed login, not logout.
Other clear-cookie uses reset fixtures or delete a deliberate response probe,
not the resident logout cookie. No other deletion-on-logout expectation found
in Python tests/checks under `src/` or `tools/`.

Parent synthesis: accept the two-check correction and strengthen replay fencing.
Reject reintroducing cookie deletion because it violates the caller's deliberate
delayed-response fence. No additional research cycle is material to this scope.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Two logout-success checks expect deletion | `src/api/checks/resident_demo_browser_check.py:352`, `:426` | High |
| C2 | Unit contract retains token and forbids Set-Cookie | `src/api/tests/test_resident_demo_api.py:405` | High |
| C3 | Full exact-head publication gate and isolated local SQL/browser contracts | `src/README.md:69` | High |
| C4 | Session status and view fence are distinct | `src/api/src/zava_forward/api/resident_demo/app.py:298` | High |
| C5 | SQLite browser has only axe/out options | `src/api/checks/resident_assistant_browser_check.py:620` | High |
| C6 | Local SQL browser owns and drops a unique database | `src/api/checks/resident_demo_browser_check.py:81` | High |
| C7 | Full gate invokes az, conflicting with caller exclusion | `tools/rpi-checks.py` (`infra` commands) | High |

## Decisions, Risks and Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
No legal or live resident acceptance is evaluated. Existing external API venv
cannot import the removed gate checkout's editable packages; create a task-owned
external venv after this actual missing-dependency failure. Never modify previous
receipt-bound environments. Full gate needs `az`, forbidden by the user; preserve
that publication boundary explicitly rather than executing Azure tooling or
claiming a full receipt.
