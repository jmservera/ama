# Changes: issue349 preflight correction 1

* `infra/scripts/tenant-readiness-preflight.py`: added strict `issuer_tenant_id()`; moved `urlsplit` import to module level.
* `infra/tests/test_tenant_readiness_preflight.py`: new issuer negative/positive test (29 tests now pass).
* Ruff (gate options) and format clean. No tenant, Azure or other file changes.
