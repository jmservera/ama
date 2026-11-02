# Issue 521 live SQL window renewal: research (2026-11-01)

Task: `issue-521-live-sql-window`. Branch `chore/resident-live-sql-window`, target `main`. Refs #521.
Research disposition: executed. Planning Readiness: Ready.
Validation tier: focused. Rationale: live operations plus documentation evidence only; no source changes.

## Authority

Owner authorisation 2026-11-01T15:55Z (explicit): extend the resident demo SQL allowlist window to
2027-02-01T00:00:00 (exclusive end). Scope: resource group `ama`, SQL server `sql-cutover-test-rzsrg`,
database `retrofit`. No RG deletion, private endpoints, public access, firewall rules or broad RBAC.
ACA min replicas 0 and all jobs Manual preserved. AI tariff expiry out of scope. The README cost
precondition is treated as covered by the owner's explicit authorisation; no billing query was made.

## Evidence

| # | Finding | Source |
|---|---------|--------|
| E1 | PR 690 (merged) set the authority end to 2027-02-01T00:00:00Z and documented the coordinator steps | `gh pr view 690`, `infra/README.md` section "Coordinator steps after the 2026-11-01 expiry" |
| E2 | Before: ca-resident-demo latest revision `res2-5fb2e32` was ActivationFailed; min 0, max 1; env expiry 2026-12-31T23:59:00Z | `az containerapp show/revision list` |
| E3 | Before (counts only): `ck_allowed_case_window` was `valid_to <= '2026-11-01T00:00:00'`; 522 `allowed_case` rows, all revoked=0, all valid_to 2026-10-31T23:59:00; resident database user `id-resident-demo` present (external) | read-only run `job-cutover-test-init-nr6bgyb` |
| E4 | All 522 rows carry one provenance: owner-approved synthetic demo allowlist 2026-10-26 | run `job-cutover-test-init-mu36xsj` |
| E5 | SQL is private; the existing Manual job `job-cutover-test-init` is the only in-VNet path (Entra admin identity), so the VM and public access were not used | `infra/README.md`, prior 563b research |
| E6 | Revision suffix 5fb2e32 descends from the #590 merge (f168d07), so the image `zava-resident-demo@sha256:9ce989d9...` is inferred to carry the January 2027 policy; ACR was not readable from this host | `git merge-base`; confirmed by the later acceptance of the 2027-01-31 expiry at deploy |
| E7 | Job config backed up (full JSON, outside the repository, mode 600); `az containerapp job start` overrides are per execution, so the template was never changed | session files |
