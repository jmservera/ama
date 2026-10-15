# Changes: Bicep quality gates (issue #139)

* Added `infra/bicepconfig.json` (linter rules as errors).
* Added `infra/modules/guard.bicep` and the `guard` module in `infra/main.bicep`.
* Added `infra/tests/test_bicep_policy.py` (11 tests).
* Updated `infra/README.md` (quality gates; production profile no longer accepts per-control relaxations).

Validation: `az bicep lint` clean; `python3 -m unittest discover -s infra/tests` 46 tests OK; MVP suite run (see PR).
Divergence: none. Open: live validate of guard message; Azure Policy compliance evidence.

## Review fix pass

* `infra/main.bicep`: all modules and the budget depend on `guard`.
* `infra/tests/test_bicep_policy.py`: `test_every_deployed_resource_waits_for_the_guard` (fails without the fix, verified); `REQUIRE_AZ_BICEP`.
* `.github/workflows/mvp-validation.yml`: `az bicep version` step; infra tests with `REQUIRE_AZ_BICEP=1`.
* Validation: `az bicep lint` clean; infra tests 48 OK.
