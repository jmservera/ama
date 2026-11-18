# Changes: issue #107 live proof, second pass (2026-11-18)

Tier: FOCUSED (docs and evidence only; no src, infra, workflow or dependency change). rpi-checks.py not run. Mypy and ruff not applicable (no Python source changed; live_probe.py is a copied evidence script). Prior worktree ../issue-107-20261117T2352 reused for its measured gap; first-pass artifacts left untouched; the existing state file was not overwritten.

## Files
* Added docs/reference/research/issue-107-live-r2-assistants-evidence-2026-11-18.md; edited docs/reference/README.md and docs/reference/log.md.
* Added .copilot-tracking/evidence/2026-11-18/issue-107-live-r2/ (raw test output, probe JSON with ids redacted, Azure read output, screenshot).
* RPI artifacts with the -r2 suffix: research, plan, details, critique, changes, review.

## Validation run
* `ZF_TEST_MSSQL=1 ... python3 -m unittest -v test_assistant_release.MssqlUnleasedRevocation` (src/api, local SQL Server 2022 RTM-CU28 container): 7 tests OK, 34.5 s.
* `python3 -m unittest -v test_assistant_restart_non_replenishment test_assistant_release test_assistant_reserve_guard`: 80 tests OK, 7 skipped.
* Live read-only Playwright probe on ca-cutover-test-demo-api: assistants, forecast, rai-metrics, proposals all 200; five assistants have no approved release; proactive false; allowance 0; tokens 0.
* Azure CLI read-only: image digest, revision 0000031 running, `standard` deployment gpt-4.1-nano 2025-04-14.

## Per-criterion table

| Unticked criterion | Result | Basis |
| --- | --- | --- |
| Independent SQL connection/worker and race tests; old images/restarts cannot restore revoked approval or replenish allowances | Proven on local actual SQL Server 2022 for revocation, restart and allowance races; old-image path SQLite proxy only; not Azure SQL | mssql_unleased_revocation.txt, sqlite_three_modules.txt; no drills authorised |
| Matching approved exercise record permits bounded proposals only; delivered-build version-linked real AI, SQL and Azure evidence | Unproven | Default-off and no-release denial live; no OQ-017 approver, so no approved record can be created without fabricating authority |

## Residue
Container ama107r2-mssql removed; password shredded; no Azure resource created; no write to the live demo this pass.

Witness note: implement-start reported "source was already dirty" because the note, index and evidence were written before the changes file; no src file exists in the diff.
