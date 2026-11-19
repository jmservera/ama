---
title: Issue 130 identity 403 fix and per-criterion evidence (2026-11-18)
description: Root cause and fix for the 403 on every Entra staff write through resident_decisions._operation, with regression tests and the status of the one unticked criterion
ms.date: 2026-11-18
---

Refs #130. Synthetic demo, desktop only. Code candidate, local commit only; not pushed, not deployed.

## Root cause

`resident_decisions._operation` compared the whole resolved actor dict with the roster row for the signed-in e-mail. An Entra principal carries extra keys (`tid`, `bound`, `identity_source`, `display_email`, app roles, a display name), so the dicts never matched and every staff write was refused with 403 "Reload your current staff identity before recording this step." Earlier live runs (issue 130 audits 1 to 5, issue 220) saw this on the demo app `ca-cutover-test-demo-api`. The comparison had no test: replacing it with a bare lookup left all 449 tests in `test_resident_decisions.py` passing.

## Fix

The check now compares the immutable keys email, code and oid, case-folded, all of which must match (`_same_signed_in_person`). Display name and tenant metadata no longer decide authorisation. A principal whose key differs from the roster person is still refused with the same 403.

## Evidence

* Reproduction before the fix: a bound Entra principal for a roster row carrying `oid` and `tid` was refused with the 403 message on JSON and SQLite stores.
* Three new tests in `src/core/tests/test_resident_decisions.py` (JSON and SQLite): matching bound principal accepted and audited under the roster e-mail; forged code, forged oid and unbound principals refused with no case or audit change; a signed-in identity that differs from the roster person is refused with no mutation.
* Mutation probe: with the comparison disabled the refusal test fails on both stores; with it restored all pass.
* Validation: 458 resident tests pass (162 skipped, SQL Server-only); `python3 -m mypy` clean in `src/core` (396 files) and `src/api` (347 files); `ruff check` and `ruff format --isolated --line-length 100 --check` clean on the touched files; 14 `src/api` nomination tests pass. The resident test run was re-observed in independent review (458 tests, OK, 162 skipped); the mypy, ruff and api results are observed; raw output not retained.
* Live: the fix is not deployed (production changes are out of scope), so the live 403 stays observable until a redeploy. Live verification of the fix is therefore unproven; the earlier live evidence is in the [fifth audit](./issue-130-live-r5-nomination-route-audit-2026-11-18.md).

## Acceptance criteria

All items ticked in the issue keep their ticks; this change adds no new claim for them beyond the identity regression coverage. Tier: FULL (src security control). The complete local gate was not run by instruction; independent exact-head review and hosted CI remain required.

| Unticked criterion | Status | Reason |
| --- | --- | --- |
| Representative participation and comprehension require authorized human evidence; constructed UI checks alone cannot pass that gate | Unproven for the demo | Data are synthetic, no representative authority is recorded, and the owner excluded person-run testing and DPO/Legal approval for the demo. Constructed checks cannot satisfy this gate by definition. |
