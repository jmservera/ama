# Plan: add `verify-federation` to infra/scripts/pipeline.py (C1)
Critique (single pass, direct): scope must stay read-only; require exact issuer/audience/subject on every credential, at least one credential, no secrets or output echo. Accepted.
1. verify_federation(identity, kind, environment): managed identity (az identity federated-credential list, RG ama) or app registration (az ad app federated-credential list + passwordCredentials empty).
2. CLI operation `verify-federation` with --identity, --identity-kind, --github-environment.
3. Unit tests in infra/tests/test_pipeline.py; README line; live read-only run showing current 0 credentials fails closed.
