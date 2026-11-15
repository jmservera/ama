# Changes (Refs #142)

* Modified `infra/modules/keyvault.bicep`: `secretRotationDays` (1-365, default 90) merged into vault tags as `secret-rotation-days`.
* Added `infra/tests/test_keyvault_secret_governance.py` (9 tests).
* Validation: unittest for the new, secret lifecycle and bicep policy tests passed; ruff check/format passed on the new file. Hosted CI, full gate and a bicep build were not run.
* Not delivered: owner/rotation documentation and access review criteria of #142 remain open.
