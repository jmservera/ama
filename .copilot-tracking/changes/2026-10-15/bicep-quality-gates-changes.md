# Changes: Bicep quality gates (issue #139)

* Added `infra/bicepconfig.json` (linter rules as errors).
* Added `infra/modules/guard.bicep` and the `guard` module in `infra/main.bicep`.
* Added `infra/tests/test_bicep_policy.py` (11 tests).
* Updated `infra/README.md` (quality gates; production profile no longer accepts per-control relaxations).

Validation: `az bicep lint` clean; `python3 -m unittest discover -s infra/tests` 46 tests OK; MVP suite run (see PR).
Divergence: none. Open: live validate of guard message; Azure Policy compliance evidence.
