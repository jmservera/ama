# Plan: scheduled ranking publication job (#79 criterion 4)

Date: 2026-11-13. Research: `.copilot-tracking/research/2026-11-13/79-ranking-snapshot-retention-2122-research.md`. Refs #79.

## Phases

* [ ] Phase 1: failing-first tests
  * `src/orchestrator/tests/test_ranking_publish.py`: with a fake Blob container, a signed test registry, a Store with cases, `main` publishes one record to Blob, a second run the same day reports already published (one PUT only, no overwrite), exit 0; the shipped draft policy exits non-zero with marker `RANKING_PUBLISH_BLOCKED` and writes nothing; unset Blob configuration exits 2 and never falls back to a folder; an unreadable store prints only the exception type; an invalid or missing run date is refused.
  * `infra/tests/test_bicep_policy.py`: compiled template has a `Microsoft.App/jobs` Schedule job running `zava_forward.orchestrator.ranking_publish`, conditional on the ranking archive container, with the ranking Blob and store env, no `--exercise`.
* [ ] Phase 2: implement
  * `src/orchestrator/src/zava_forward/orchestrator/ranking_publish.py` (store-sourced cases; Blob archive only; injectable env, store, archive, registry, today).
  * `infra/modules/containerapps.bicep`: `rankingPublish` job, daily `30 2 * * *`, same identity, store and Blob env as the API, only when `rankingArchiveContainer` is set.
* [ ] Phase 3: docs
  * infra README ranking archive section, orchestrator README, core README pointer, ADR 0002 status row. State criterion 3 open and retention approval open.
* [ ] Phase 4: validate in `/tmp/venv-79ret-2122`: core, orchestrator, agents, api, infra unit tests, `test_ai_call_site_inventory`, ruff check and format, mypy, `az bicep build`.
* [ ] Phase 5: changes record, review, commit (`Refs #79`), cleanup, no push.

## Decisions

* Reuse the runner `run()` so one code path handles verification, signoff refusal and idempotency.
* No new dependency.
* Job exits non-zero while the policy is unsigned so a missing sign-off is visible, not silently green.
* Run date is read from the UTC clock only in `main`; `run_publish` takes it as an argument.
