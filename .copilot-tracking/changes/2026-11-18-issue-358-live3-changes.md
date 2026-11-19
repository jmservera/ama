# Issue 358 live pass 3 changes

Tier: FOCUSED. No `src/` or `infra/` file changed; no Azure write.

Files added: research note `docs/reference/research/issue-358-live3-evidence-2026-11-18.md`, raw evidence under
`docs/reference/research/issue-358-live3-2026-11-18/`; index row in `docs/reference/README.md`; log entry.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| 1. Expired stored credential guard test | Proven | `baseline-tests.txt` (126 OK); `mutation-expiry-filter-always-true.txt` (9 failures on temp copy) |
| 2. Rebuild preserves Key Vault-referenced secrets (non-production) | Proven for the rebuild component (first-pass live round trip); not repeated here | `azure-list-and-throwaway-absent.txt`, `demo-api-kv-reference-readonly.json` |
| 2b. Full `setup-entra.py` run on deployed demo app | Unproven: needs Graph addPassword, tenant admin and Key Vault write; rotation excluded | n/a |
| 3. #352 conflict, delegating `main()` | Proven | `delegating-main-source.txt`, `delegation-test.txt` |

## Validation

* `python3 -m unittest infra.tests.test_setup_entra`: 126 tests OK.
* mypy, ruff and rpi-checks not applicable (no code change); `rpi-checks.py --all` not run by instruction.
* Needed src/infra change: none. Any future change is a full-tier follow-up.
