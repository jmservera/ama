---
title: Issue 432 resident host wiring and output link plan
ms.date: 2026-11-13
---

## Phases

* [ ] P1 `LedgerTopicMeter`: keep root in the thread-local; only for outcome `returned`, after `complete`, call `publish_output(root, reference(new_id()), eligible=False)` (never for timeout/credential/held failures) and expose the opaque `last_output` reference so a later review path can link the same id (writes are idempotent per root/output). Never raise or log content.
* [ ] P2 Close the reservation on unexpected exceptions: `aoai._request` credential acquisition (`except Exception`), the whole admitted pre-transport interval (token guard, validation, clock) and `assistant.select` token/transport failures; the meter close is idempotent so each reservation closes at most once, each closed once as `provider-unavailable` then re-raised or mapped as before.
* [ ] P3 `configured_advisor(..., ledger=AdvisorLedger(...))` builds `advisor_meters`; supplying both `meters` and `ledger` is a `ValueError`. `__main__` is unchanged (no owner-approved ledger/authority).
* [ ] P4 Tests in `test_resident_ledger_meter.py`: ineligible output linked, content-free; `RuntimeError` credential closes; `configured_advisor` with `ledger`. Run inventory, consumption, resident tests, ruff, mypy.

## Details

* Output ref is a fresh random `reference()`; no resident data. `eligible=False`, since no human accepted it, so cost per accepted proposal is not inflated.
* Output link failure (`publish_output` hold, or any Exception) must not change the outcome.
* Tier Focused: targeted tests plus hosted CI read.
