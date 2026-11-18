# Changes: issue #107 live proof (2026-11-18)

Tier: FOCUSED. No src, infra, workflow or dependency change; docs and evidence only. rpi-checks.py not run (--all forbidden). Mypy/ruff not applicable (no Python source changed; live_probe.py is evidence under .copilot-tracking).

## Files
* Added docs/reference/research/issue-107-live-assistants-evidence-2026-11-18.md
* Edited docs/reference/README.md (index row), docs/reference/log.md (new entry)
* Added .copilot-tracking/evidence/2026-11-18/issue-107-live/ (probe script, JSON outputs, test outputs, screenshot)
* RPI artifacts: research, plan, details, critique, this file, review, state

## Validation run
* `ZF_TEST_MSSQL=1 python3 -m unittest -v test_assistant_release.MssqlUnleasedRevocation` (src/api, local disposable SQL Server 2022): 7 tests OK.
* `python3 -m unittest -v test_assistant_restart_non_replenishment test_assistant_release test_assistant_reserve_guard`: 80 tests OK, 7 skipped (the MSSQL classes).
* Live: Playwright probe against ca-cutover-test-demo-api (GET assistants, forecast, rai-metrics, proposals; invoke x5): all five denied, envelope null, tokens 0.
* Azure CLI read-only: container app image digest, env names, `standard` deployment model version.

## Per-criterion table

| Unticked criterion | Result | Basis |
| --- | --- | --- |
| Independent SQL connection/worker and race tests; old images/restarts cannot restore revoked approval or replenish allowances | Proven (actual local SQL Server 2022 for revocation, mismatch, restart and allowance races; SQLite proxy for old-image path) | mssql_unleased_revocation.txt, sqlite_restart_non_replenishment.txt. Not run on Azure SQL (no drills; fixture refuses it) |
| Matching approved exercise record permits bounded proposals only; delivered-build version-linked real AI, SQL and Azure evidence | Unproven | Live denial and default-off proven; no approved release can be created without an appointed OQ-017 approver; #432 real-AI calls were not under a release record |

## Residue
Throwaway container ama107-mssql removed; password shredded; no Azure resource created. Live demo store holds five retained denial proposals.
