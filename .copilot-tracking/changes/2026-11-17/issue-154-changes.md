# Issue 154 changes (2026-11-17)

* Added `test_representative_expiry_and_revocation_take_effect_on_the_next_request` in `src/api/tests/test_resident_preview_api.py`. No source change: the boundary already denied (test passes without a fix).
* Divergence: first assertion expected an exact error body; the denial also carries the synthetic banner, so the assertion now checks the error text and absence of home/appointments/viewer. A source edit preceded the first `implement-start` witness, which was refused (state lacked the changes path); the retry succeeded with a "source already dirty" qualification.

Validation (FOCUSED): `tests.test_resident_preview_api` 16 OK (src/api, PYTHONPATH=../core/tests:../agents/tests); core `test_resident_journey_design test_resident_access test_resident_preview` 48 OK (baseline); `ruff format --isolated --line-length 100 --check` clean; `mypy tests/test_resident_preview_api.py` clean. Not applicable: rpi-checks --all (heavy lock, tier), browser harness (no web files).
