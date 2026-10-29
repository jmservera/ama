---
title: Capacity page 523 research
description: Focused SQL demo failure investigation
ms.date: 2026-10-28
---

## Research brief

Investigate issue #523 for maintainers: reproduce the manager capacity page
against local SQL and generated demo data, identify the failing endpoint and
root cause, check adjacent manager pages, and prepare a bounded repair.
Output mode: convergence. Posture: focused, selected from the named code path
and acceptance criteria. No Azure, secrets, environment files or private data.
Heavy checks must hold `/tmp/ama-rpi-heavy.lock` nonblocking.

## Questions and candidate areas

1. Which API or rendering operation fails on SQL demo data?
2. Is the defect shared by manager pages?
3. Which existing error/retry and test patterns should the repair preserve?

Start with `src/api` frontend, routes, core SQL store and synthetic seed helpers.
External evidence is limited to the GitHub issue; no cloud inspection is authorized.

## Extensions and participation

Repository instructions and RPI phase skills selected. Web guidelines will be
loaded before web edits. Independent critique and final review will be bounded
delegations; tightly coupled research remains inline. No interaction required:
the caller explicitly requests the full ordered loop and publication.

## Direction controls

Use `fix/capacity-page-523` in the supplied clean worktree. Source only in `src/`.
Preserve original evidence; no live deployment. Live verification remains owner-owned.

## Cycle 1

### Wider

Traced `capacityView` through its two reads and SQL document hydration.
`list_packages` returns one package; `list_work_orders` fails on freshly generated
980-case demo data seeded into SQLite. Generator used the existing test-only
fictional geography register, seed 20260901 and as-of 2026-10-13; no dataset read.

Reflection: the failure is in work-order projection, not the package request,
manager role, or AI setup.

### Deeper

`list_work_orders -> _wo_view -> appointment_summary -> _appointment_binding`
raises `KeyError: 'contract_version'`. Legacy generated packages omit that field.
The package read already represents it as null. The appointment binding indexes
it directly, so every evidence-visible manager order list fails before JSON.
The handler does not catch that exception; browser network errors or unstructured
HTTP failures therefore have no useful capacity-specific message.

Reflection: fix the read compatibility boundary, never invent a version or
repair stored authority implicitly. Existing `_contract_authority` rejects a
missing version, so unknown contract metadata must remain non-authorizing.

### Contrarian

The same generated data loads packages successfully, ruling out wholesale SQL
seed failure. Both SQL implementations inherit the same appointment projection;
SQLite establishes a concrete source failure but is not real SQL Server evidence.
Current procurement fixtures supply contract versions and therefore miss it.
Other pages need actual browser coverage; no live root-cause claim is made.

## Validation blocker

At intake `/tmp/ama-rpi-heavy.lock` was held by PID 4053825 (`python3.12`).
Confirmed with `lslocks` and `ps`; no foreign output or credentials inspected.
Per shared-host policy, SQL Server/browser/full-gate work is blocked without
queued admission or polling. Resume only after an explicit coordination event
and nonblocking lock acquisition. Independent lightweight work continues.

## Evidence and decisions

W1: https://github.com/jmservera/ama/issues/523, retrieved 2026-10-28.
Reports capacity failure and requires SQL, retry, regression, adjacent-page and
live-verification evidence.

C1: `src/api/src/zava_forward/api/web/ops.js:159`: both reads use Promise.all.
C2: `src/core/src/zava_forward/core/procurement.py:506`: projection calls appointment summary.
C3: `src/core/src/zava_forward/core/appointments.py:110`: direct missing-key lookup.
C4: `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_mvp_coverage.py:37`:
legacy package schema omits contract_version.
C5: `src/core/src/zava_forward/core/procurement.py:112`: contract authority requires a version.
C6: `src/api/src/zava_forward/api/web/app.js:205`: route already supplies Try again.
C7: isolated installed-source SQLite reproduction printed `list_packages OK 1`
then the exact C2/C3 traceback. 980 cases, 443 open, 10 generated staff.

## Alternatives and current decisions

Select null-preserving optional contract-version projection with regressions
for legacy seeded packages and unchanged write rejection. Reject fabricating
versions or rewriting seed authority. Improve capacity load errors locally,
preserving route cancellation, session expiry, existing retry and manual drafts.
Do not redesign the app or alter global API behavior.

No separate research lane needed: this is one continuous trace. One focused
three-wave cycle completed; further source search is redundant. Real SQL,
browser and adjacent-page runtime evidence remain blocked, not replaced by SQLite.

## Readiness

Research disposition: executed. Planning Readiness: Ready for bounded source
repair; SQL/browser/publication acceptance remains blocked by shared-host admission.
