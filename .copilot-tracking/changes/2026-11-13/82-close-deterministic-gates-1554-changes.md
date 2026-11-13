---
title: Issue 82 changes
ms.date: 2026-11-13
---

## Changes

* `gates.py`: eligibility, authority and finance rules and gates; `AuthorityGateError`, `FinanceGateError`; `CONTROLLED_RULES` registry of every rule; `unreviewed_rules()`.
* `finance.py`: commitment raise classifies no/unapproved budget and over-budget as fail, unreadable budget or amounts as unknown, evaluates the gate on success; messages and ValueError type unchanged.
* `grants.py`: `require_authority` raises `AuthorityGateError` (PermissionError subclass, same text) with unknown for unreadable designation and fail for readable but out-of-scope or expired.
* `tests/test_gates.py`: registry, new gates never pass without evidence, finance/authority wiring.

## Validation

* Core suite: 3177 run, 403 skipped, 50 failures/errors all in `test_device_registry_azure` (Azure SDK client tests, unrelated to gates; this venv has no Azure SDK).
* `test_gates.py` 28 OK; ruff check and format clean; `src/core` mypy clean.
* Targeted api (finance exposure/match/grants screens/grant lifecycle) and core finance/grant suites pass; the full src/api suite exceeded a 900 s limit and was not completed.

## Open (not claimed)

* Eligibility gate exists but no call site is wired (no recorded eligibility evidence field).
* All rules carry the explicit unreviewed marker; no named human reviewer. #82 is not closed (Refs only).
* New rules take effect 2026-11-13; an earlier clock yields unknown/refusal for finance commitments and authority.
