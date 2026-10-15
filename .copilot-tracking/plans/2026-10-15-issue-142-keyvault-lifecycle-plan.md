# Plan: #142
1. Add scheduled query alerts to keyvault.bicep, wire actionGroupId.
2. Add secret-inventory.json and secret_lifecycle.py (check, review, rotation-plan) with offline tests.
3. Document in infra/README.md, index and log. Validate with unit tests and az bicep build.
Critique (single pass): ordering rule for credential deletion added to test; owners left as open items.
