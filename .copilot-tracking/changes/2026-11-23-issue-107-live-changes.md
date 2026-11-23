# Changes (2026-11-23, Refs #107)

Tier: FOCUSED. No src change; docs and tracking only.

Files: docs/reference/research/issue-107-live-r4-assistants-evidence-2026-11-23.md (new), docs/reference/README.md (index), docs/reference/log.md (entry), .copilot-tracking/evidence/107-live/mssql-release-tests.txt.

## Per-criterion table (unticked criteria)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images/restarts cannot restore revoked approval or replenish finite allowances | Proven for the demo on actual local SQL Server 2022 (95 tests OK, 0 skipped); old image simulated, real older image not pullable (private ACR) | research note r4; mssql-release-tests.txt |
| Matching approved exercise record permits bounded proposals only; delivered-build real AI, SQL and Azure evidence | Unproven: no approved release on deployed build (needs named approver, OQ-017); live API revision 0000055 observed read-only | research note r4 |

Not run: rpi-checks.py --all, hosted CI, independent exact-head review.
