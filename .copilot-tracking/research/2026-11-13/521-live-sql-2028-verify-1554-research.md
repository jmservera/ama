# Research: Live SQL 2028-01-01 cutoff verification (Refs #521 criterion 4)

Date: 2026-11-13. Disposition: reused (preflight [521-azure-sync-preflight-1416-research.md](521-azure-sync-preflight-1416-research.md) plus source read). Planning Readiness: Ready. Tier: Focused.

## Evidence

* Preflight (a) and (b): live app `ca-resident-demo` already carries `ZF_DEMO_EXPIRES_AT` 2028-01-01T00:00:00Z; the live SQL `ck_allowed_case_window` constraint is unverified.
* `infra/sql/resident-showcase.sql` batch 3 drops and re-adds `ck_allowed_case_window` in one transaction with `valid_to <= '{{AUTHORITY_END}}'`; it is idempotent and never touches row windows. Later batches re-run the view and principal grants.
* `infra/scripts/resident_showcase_sql.py` renders `AUTHORITY_END` from `zava_forward.core.resident_showcase`, authenticates with an Entra token held in memory (`az account get-access-token`, never printed), and needs `--client-id` for principal verification.
* Owner decision `live_azure_demo_sync = redeploy_demo_and_sql_2028_after_merge` authorises this apply.

## Approach

1. Confirm `AUTHORITY_END` renders as 2028-01-01T00:00:00.
2. Probe the server (DNS, TCP 1433, token-authenticated connect) with the token in memory only. Do not change firewall or RBAC when blocked; record the exact result.
3. If reachable, apply only the constraint batch (not the view or grants, which need the resident client id and separate approval), then read back `sys.check_constraints.definition`.
4. Record redacted evidence, run `test_cutover_audit` and a secret scrub, review, commit locally. No push.
