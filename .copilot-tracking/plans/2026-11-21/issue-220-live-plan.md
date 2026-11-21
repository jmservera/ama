# Issue 220 live plan (2026-11-21)

1. Change `_same_signed_in_person` in `src/core/src/zava_forward/core/resident_decisions.py`: code and email must match; oid must match only when the roster row records one. Use it in `_owner_rights`.
2. Add a focused test in `src/core/tests/test_challenge_signed_in_principal_220.py` for an oid-less roster row (write succeeds, nothing adverse inferred; a different person is refused).
3. Run core tests for resident decisions and issue 220, mypy and ruff in `src/core`; read hosted CI later. Tier FULL for src, but no `rpi-checks.py --all` (coordinator runs gates).
4. Write research note under docs/reference/research/ with the per-criterion table, add index and log entries, changes record, review.
