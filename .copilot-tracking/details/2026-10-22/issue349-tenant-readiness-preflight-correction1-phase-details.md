# Phase details: correction 1

* P01: add `issuer_tenant_id()`; replace the regex in the api-issuer-tenant check; unreadable issuer stays `unknown`, foreign or malformed issuer is `mismatch`.
* P02: `test_issuer_must_be_exact_authority_and_tenant_path` with nine negative subtests and one positive.
* P03: unique external receipt directory; verify with `--verify-receipt` against current origin/main before push.
