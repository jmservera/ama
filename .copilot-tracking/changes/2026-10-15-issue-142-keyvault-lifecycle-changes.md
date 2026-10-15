# Changes: #142
* infra/modules/keyvault.bicep, infra/main.bicep: expiry and denied-access alerts.
* infra/secret-inventory.json, infra/scripts/secret_lifecycle.py, infra/tests/test_secret_lifecycle.py.
* infra/README.md, docs/reference/README.md, docs/reference/log.md.
Validation: infra tests 35 OK; az bicep build OK. mvp suite not affected (no mvp change).
