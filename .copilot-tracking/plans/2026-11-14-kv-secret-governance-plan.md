# Key Vault secret governance plan (Refs #142)

* [x] Add bounded `secretRotationDays` parameter recorded as vault tag.
* [x] Add `infra/tests/test_keyvault_secret_governance.py` covering hardening, rotation metadata, RBAC role limits and zero secret outputs.
* [x] Focused validation: new test, test_secret_lifecycle, test_bicep_policy; ruff isolated check and format.
* Critique: single pass, no conflicting findings. Tier: focused (module parameter default is non-breaking; no deployment change).
