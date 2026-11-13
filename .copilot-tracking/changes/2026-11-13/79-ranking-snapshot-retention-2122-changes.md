# Changes: #79 criterion 4, scheduled ranking publication

Date: 2026-11-13. Refs #79. Plan: `.copilot-tracking/plans/2026-11-13/79-ranking-snapshot-retention-2122-plan.md`. Critique: `.copilot-tracking/critiques/2026-11-13/79-ranking-snapshot-retention-2122-critique.md`.

## Added

* `src/orchestrator/src/zava_forward/orchestrator/ranking_publish.py`: scheduled entry point. Reads open cases and `as_of` from the configured store under its lock, calls `ranking_publication_runner.run("publish", ...)` against the Blob archive only, prints `RANKING_PUBLISH_OK`, `RANKING_PUBLISH_BLOCKED` or `RANKING_PUBLISH_ALERT`. Exit 0 ok, 1 blocked or failed or stale data, 2 Blob not configured.
* `src/orchestrator/tests/test_ranking_publish.py` (10 tests, written first and failing on import): publish once and keep the retained bytes on repeat, next day with unchanged data keeps the record and alerts, shipped unsigned draft refused and still unsigned, no folder fallback, missing or partial Blob configuration refused, bad date, secret-free failure with retry confirming, non-boolean `closed`, registry verification, no bypass or delete in source.
* `infra/modules/containerapps.bicep`: `rankingPublish` Schedule job (`30 2 * * *`), conditional on workloads, background workloads and a non-empty `rankingArchiveContainer`.
* `infra/main.bicep`: the job joins the job-failure alert list when `enableRankingArchiveBlob` is true.
* `infra/tests/test_bicep_policy.py`: new job test (schedule, command, env, conditions, monitoring); existing counts and name sets updated for the new job.

## Docs

* `infra/README.md` and `src/orchestrator/README.md`: job and runner contract, exit codes, evidence boundary.
* `docs/adrs/0002-pilot-readiness-architecture.md` is a dated historical snapshot and is intentionally unchanged.

## Not changed

* Policy status stays `draft`, owner unsigned (criterion 3 open). No signature, `--exercise` or sign-off bypass.
* No new dependency (REST adapter reused). No UI copy. No Azure call.
* Retention duration is not approved or locked; the container immutability policy remains owner-set and default off.

## Divergences from plan

* Critique PC-005: a log-query missing-run alert was not added; job-failure alert coverage was added instead. Recorded as follow-up.

## Validation

See the review record.
