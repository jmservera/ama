# Issue 2186 live research (2026-11-22)

Goal: full gate receipt stays valid across docs-only main moves in `tools/rpi-checks.py`, with tests. Focused tier.

## Evidence

* `base_relaxation(..., inert_only=True)` and `validate_receipt` already relax a full receipt for inert-only moves (commit 8c27b4940c, #2221).
* `test_full_receipt_survives_only_inert_main_moves` passes locally (1 test OK); the 7 relaxation/verify tests pass.
* `verify()` prints `BASE RELAXED (kind)` from `receipt["base_relaxation"]`, which validate_receipt sets for any scope. The only existing verify-output test uses a partial scope receipt.
* Prior note: docs/reference/research/issue-2186-live-full-receipt-docs-move-2026-11-21.md.

## Gap

No test drives `verify()` with a real full-scope receipt after a docs move. Planning Readiness: Ready. Disposition: executed (reuse plus one gap test).
