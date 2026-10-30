---
title: Capacity and work orders issue 523 changes
description: Current implementation and local acceptance evidence
ms.date: 2026-10-30
---

## Scope and State

Full plan execution: capacity-work-orders-page-523, base
5634f9a077d175a931c15e3400114665d8c071ee. Research and Plan completed in
order. Single critique Revise PC-001 applied: sanitize external runner exactly
like main. P01 implementation and P02 local validation complete; original Review
and local commit/gate remain. Preserve merged #528 runtime repair.

## P01: Acceptance coverage

Planned changes: optional pinned axe input and seeded/error/empty capacity
scans, keyboard retry, one helper test module and existing README update.
P01-T01 completed. No production web or core changes. The optional scan verifies
the existing pinned digest before app construction, reports violations and
incomplete checks, and fails on violations. Four new helper tests exercise
accepted/rejected bytes and clean/violating scans. Seeded, both unavailable
reads and empty states now scan #app; initial retry uses focused Enter.
Existing invocations remain supported.

Implementation judgment: repeat the established pinned scalar digest locally
instead of importing regulatory fixture-heavy checks through a package-only
path. This preserves standalone script invocation. No second critique needed.

## Validation and Residuals

Existing legacy procurement regression passed before implementation (one test).
System Python lacked Playwright and shared venv lacked editable core; a fresh
owned external venv was successfully provisioned with pip and declared editable
core[sql,blob], agents and api[dev]. No dependency manifest changed.
Five focused tests passed (four helpers and existing legacy HTTP regression).
First Ruff run found new test import ordering; Ruff fixed it, then formatted the
test. Targeted mypy passed for both changed Python files. All wider results
pending. No Azure, deploy, live sign-in or push.

## P02-T01: Current package quality and heavy admission

Fresh owned venv, API cwd:
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`.
Focused five-test run passed. Full `ruff check .` passed; `ruff format --check .`
passed (61 files); full `mypy` passed (117 source files).

The requested complete unittest discovery was queued using
`flock -w 600 /tmp/ama-rpi-heavy.lock`; admission timed out, exit 1, without
starting Python or producing the redirected unittest log. This is Not run,
not a failing test suite or a pass. The SQL/browser command uses the same
600-second admission and a separate sanitized owned runner; it subsequently
acquired the lock and started its uniquely owned SQL container. No foreign
process was interrupted or output read.

Current SQL/browser milestones: manager capacity renders one generated package
and 601 orders. All twelve current manager navigation destinations passed
successful browser-read/heading/content checks. Seeded capacity and each initial
failed-read state have zero axe violations and zero incomplete checks. Remaining
draft/session/empty scenarios are still running, so no whole-run pass is claimed.

Historical evidence, not a current-candidate rerun:
.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-delayed-401-review.md
records a successful owned SQL/Chromium run with 980 cases, one package,
601 orders, all eleven actual manager destinations and prior retry/expiry tests.
The current runtime is unchanged, but that historical result does not substitute
for this candidate's new scans.

## P02-T02: Completed real SQL/Chromium acceptance

The sanitized external runner completed under the requested outer flock,
exit 0. Owned SQL Server `ama-capacity523-2fad22a58e29`, random loopback port
33314; its uniquely owned container was removed and absence verified afterward.
The real loopback app responded to synthetic manager login and all API reads.
Generated seed: 20260901, as-of 2026-10-13, fictional register, 980 cases.
Capacity displayed one package and 601 work orders, then clear package/order
empty states. Four axe 4.10.3 scans (seeded, packages unavailable, workorders
unavailable, empty) returned zero violations and zero incomplete checks.

Both failed API reads showed named plain-language errors and recovered through
focused Enter on native Try again. Repeated failed refreshes retained editable
drafts; successful recovery retained original context/event and did not repeat
saved mutations. Both delayed-sibling 401 permutations retained sign-in after
successful retry responses. Cancellation, transport, 403, expiry and empty
states passed. Expected cancelled-request BrokenPipe diagnostics remain in the
original log, not hidden; the browser recorded no unexpected API/console/page
failure.

All twelve current manager destinations passed: #/, #/all, #/overview,
#/progress, #/visits, #/funding, #/finance, #/capacity, #/closed, #/assistants,
#/time and #/screens. No same-class failure found.

External evidence root:
/home/azureuser/.copilot/session-state/4e7cc75c-46cf-4e8c-ab7e-e434e13e0fd8/files/.
Raw log: capacity-mssql-browser.log, SHA-256
1c76930771042eea97e3c7294b9aa3ebbb31022eb47da4455418f389832b1085.
Runner: run_capacity523.py. Transcribed lightweight outputs: validation523.txt.
The full API discovery was re-admitted once after this owned gate completed.
It passed, exit 0: 1374 tests in 481.766s, 318 optional skips.
Raw output: api-unittest-attempt2.log in the same external evidence root.
The general-discovery skips are not counted as SQL coverage; the separate owned
SQL/browser run above provides issue-specific real SQL evidence.
No source changes occurred during validation.

## Acceptance Evidence

| Criterion | Current evidence and status |
| --- | --- |
| Root cause identified | Proven: historical missing contract_version on workorders projection, merged null-preserving fix, fresh passing HTTP regression |
| Manager SQL demo capacity loads | Proven: actual SQL Server/Chromium, one package and 601 orders plus both empty messages |
| Plain-language failed call with retry | Proven: both 503 reads, transport/403/session/cancel paths; native keyboard retry succeeds |
| Regression covers failure | Proven: existing legacy regression plus four new scan helper tests pass |
| Other manager pages checked | Proven: all twelve current destinations pass; no same failure class observed |
| Live verification recorded or pending owner | Marked pending owner; no deployment or live observation performed |

These are local synthetic engineering results, not production, full Fluent UI,
WCAG, screen-reader/voice-control or human acceptance.

## Review Handoff

Source is frozen at the three SHA-256 values in external validation523.txt.
The only changed implementation files are the capacity check, its four helper
tests and related README. No production web file changed; current full web
guidelines were retrieved for scoped review, with no changed-web-file findings
to assess. No full-conformance claim follows from axe.

Original independent Review executed once: Complete / Residual work. No source
defects found. RV-001 (Low) routes local commit/publication gates to coordinator
follow-up; RV-002 (Low) routes live verification to the owner after deployment.
Original outcome is preserved, not promoted to full acceptance.
Review artifact:
.copilot-tracking/reviews/logs/2026-10-30/capacity-work-orders-page-523-review.md.
No code change or second Review follows it.

Full publication gate, coordinator push/PR/hosted approval and live owner
verification are not yet completed. Local commit and a post-commit full-gate
attempt are next. The supplied main base still matches fetched origin/main.
