# Changes: Live SQL 2028 cutoff verification (Refs #521 criterion 4)

Date: 2026-11-13. Status: BLOCKED, constraint not applied and not verified. Criterion 4 stays unmet. Evidence is redacted: no token, subscription or tenant id, or IP address recorded.

## Probe result (read-only, Entra token held in memory only)

| Check | Result |
| --- | --- |
| Merge precondition | `origin/main` (`ca7803e85`) is an ancestor of HEAD and carries `AUTHORITY_END` 2028-01-01T00:00:00Z in `zava_forward.core.resident_showcase` |
| Render | `resident_showcase_sql.render` yields one constraint batch containing `'2028-01-01T00:00:00'` |
| Target database | `az sql db list` on `sql-cutover-test-rzsrg`: one user database (`retrofit`, Online) plus `master`; unambiguous |
| DNS | Resolves to a public address (private endpoint path not used from this host) |
| TCP 1433 | Connects |
| Token-authenticated connect to `retrofit` | Refused by SQL Server: `Deny Public Network Access` is set to Yes ("Connection was denied because Deny Public Network Access is set to Yes") |
| Constraint read-back, row-count preflight, apply | Not performed (no session) |

## Actions not taken

* No firewall, private endpoint, public-network-access or RBAC change (brief forbids it when blocked).
* No SQL statement executed; no row window changed; no source file changed.

## Next action for the owner

Run `python3 infra/scripts/resident_showcase_sql.py <principal> --client-id <resident MI client id> --apply sql-cutover-test-rzsrg retrofit` from a host allowed by the private endpoint (or approve a short, reverted network window), then read back `sys.check_constraints` for `ck_allowed_case_window`. Only then tick criterion 4 and update the `infra/README.md` Pending entry.

## Local checks

See the validation section below.

## Validation

* `python3 -m unittest src/core/tests/test_cutover_audit.py`: 9 tests OK.
* Secret scrub over the task artifacts (token, credential and GUID patterns): 0 hits.
* Probe scripts were temporary files in `/tmp`, deleted after use. Existing `/tmp/venv-*` directories were not created in this task (not verified as owned by other tasks), and were left in place (critique PC-006).
