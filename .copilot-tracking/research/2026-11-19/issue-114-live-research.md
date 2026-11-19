# Issue 114 live research (2026-11-19)

Refs #114. Research disposition: executed. Planning Readiness: Ready.

* Issue #114 has one unticked criterion: per-year audit and ledger digest verification proven by test before reliance. The other two are ticked.
* Existing code: `ledger.py` (`verify_entries`, `make_year_digest`, `year_digests`, `verify_years`) and `store.py` `verify_ledger_before_reliance`. Existing tests: `test_recovery`, `test_sqlstore`, `test_ledger_digest_blob`.
* Prior note: `docs/reference/research/issue-114-live-reverify-2026-11-18.md`. The deployed image lacks `MssqlStore.verify_ledger_before_reliance`; closing that needs an image roll (deployment), outside the owner's authorisation.
* Question: is any source or test gap left for the criterion in code? Method: rerun tests at base 910adb0a1 and map coverage.
