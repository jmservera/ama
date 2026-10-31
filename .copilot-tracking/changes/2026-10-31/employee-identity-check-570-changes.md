---
title: Employee identity caller changes and validation
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Scope and State

Task 570, employee-identity-check-570, implementation scope P01.
Plan and details dated 2026-10-31. One original critique retained (Revise);
compatible direct dispositions recorded before implementation.
Implement an authenticated-session adapter only; no new sign-in/credential
handling. Independent expected-ID provenance remains a live prerequisite.

## P01-T01: Maintained caller

Completed: src/api/checks/employee_acceptance_check.py invokes unchanged
BINDING with independently supplied expectations, validates exact boolean
shape and refuses incorrect identity, provider/role/schema or transport state.
Exact origin before/after evaluation and every observation; rechecks identity
around each stage. Fixed statuses and boolean outputs only, no sign-in or
credential entry point. src/api/tests/test_employee_acceptance_check.py adds
six contracts through fixture composition, not inherited duplicate discovery.
API README documents integration, caller responsibilities and live limitations.

The positive real Chromium regression admits a rosterless principal without
display email, then exercises actual local chat (workflow-only), keyboard map
filter with actual map HTTP response and actual case view. Negative Chromium
has equal display email but a different immutable principal and executes zero
observers. No remote network, live identity or authorized credential access.
Original helper and all historical artifacts remain unchanged.

### Coupled Local Corrections

Original synthetic observer probe failed: chat storage correctly refused
missing privacy references. Corrected the fixture, not application admission,
with existing explicitly synthetic privacy references. Chat refusal disposes
the panel, so its wait now stops on panel disposal as well as reply/error.
Map aria-busy is removed rather than set false; wait reflects actual code.
An aria-pressed=false locator is unstable after selection; use stable index
among all filter buttons. Case links in overview can be hidden; explicitly
navigate all-case list and follow an actually offered visible link.
Initial full-observer browser test failed case stage; corrected local navigation
then the exact regression passed. These are ordinary coupled test/caller
corrections, no policy/authorization change and no repeated critique.

## P01-T02: Validation and Live Boundary

Missing namespace import first observed; system pip refused externally managed
environment. Restored distributions using pip in an external session venv.
Authorized healthz returned HTTP 200. Read-only Graph user lookup returned
insufficient privileges. No credential file read; zero sign-in attempts.
Live identity/chat/map/case currently Blocked, not passed.

The distinct direct `az rest` Graph user lookup also returned
Authorization_RequestDenied on 2026-10-31. No safe independent object-ID
source available. Stop that live lane without modifying Azure/directory access.

## Validation Record

All commands from src/api use the external pip venv and
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests.

| Check | Status | Evidence |
| --- | --- | --- |
| python3 -m unittest discover -s tests -q | Passed | 1436 tests in 603.964s; 320 opt-in integration skips remain recorded, not executed acceptance. |
| python3 -m unittest test_employee_acceptance_check -q | Passed final source | Six contracts; two actual Chromium methods, including actual synthetic local observers. |
| python3 -m checks.employee_acceptance_check | Passed final source | Two executed Chromium methods, zero skips, installed Chromium, real loopback /me and actual local chat/map/case. |
| ruff check . | Passed final source | No errors. Initial new import-order error fixed using Ruff. |
| ruff format --check . | Passed final source | 66 files formatted; existing checks exclusion unchanged. |
| ruff format --check --isolated --line-length 100 checks/employee_acceptance_check.py | Passed final source | Explicitly checks otherwise excluded runner. |
| mypy | Passed final source | 125 files. Fixture principal call follows existing Any adapter pattern at the untyped fixture boundary. |
| git diff --check | Passed | No whitespace errors. |
| Live healthz | Observed | HTTP 200. Not authentication/feature acceptance. |
| Live expected identity, employee chat, map filters and case | Blocked | Independent expected object ID unavailable; zero sign-ins, no credential read. |

## Pre-Review Reconciliation

P01-T01 source and regression completed. P01-T02 local validation and live
eligibility evaluation completed; original live issue criterion remains unmet.
P01 phase is partial against that live outcome. P02 publication remains pending.
Plan/detail markers, README and this changes record agree. One Review may
assess this bounded repair and route live evidence separately. No conformance
or whole-issue completion claimed.

## Remaining Work

Candidate commit and complete publication gate.
Missing independent object ID cannot be replaced
with observed /me, HTTP success, email equality or role-only admission.

## Follow-Up Items

Identity administrator provides independent expected tenant/object provenance;
then execute a fresh owner-authorized bounded live campaign. This remains
the original issue's unproven acceptance criterion, not evidence of delivery.

## Original Review and Routing

Exactly one independent Review executed; execution Complete, outcome Not accepted.
Record: .copilot-tracking/reviews/logs/2026-10-31/employee-identity-check-570-review.md.
Reviewer independently ran existing/new identity contracts, local Chromium,
Ruff and mypy and reproduced two substantive caller defects:
RV-001 map false acceptance on malformed rendered data (Medium);
RV-002 missing fresh admission after navigation inside observers (High).
Both remain open, routed to later implementation. No correction/second Review
in this task; no publication approval or whole-issue completion claimed.

RV-004 preserves unavailable independent identity/live acceptance.
RV-003 claims a prohibited shared-lock path. Parent does not adopt that
unsubstantiated compatibility assertion: the prescribed repository gate
explicitly owns that named local lock; no prohibited destructive action or
actual lock failure has been observed. Preserve original finding unchanged,
run the documented complete gate and report its actual result separately.
Even a passing gate cannot approve this Not accepted candidate for publication.

Loop execution is finished, delivery is partial. P02-T01 Review portion ran;
commit/gate remain next, push/PR blocked by material original Review findings.
