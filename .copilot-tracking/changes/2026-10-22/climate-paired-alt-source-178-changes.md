<!-- markdownlint-disable-file -->

# Changes: climate-paired-alt-source-178

| Field | Value |
|---|---|
| Date | 2026-10-22 |
| Plan | .copilot-tracking/plans/2026-10-22/climate-paired-alt-source-178-plan.md |
| Scope | Full plan except P03 publication (gate and push owned by the final stage) |

## Preflight and branch reconciliation

* Fresh fetch: origin/main 9e55a392b95c90730c6410b9a4db4ad3a5ae70ce. Local f58b98b8 was an ancestor of remote head 99c782ea (single commit by github-actions[bot], "chore(rubric): record score 48/100").
* Fast-forwarded to 99c782ea, then rebased the run-owned branch onto origin/main with history intact (all local climate commits and their append-only log, index and synthesis entries kept).
* One conflict, only in the generated .github/rubric/scores/latest.json. The bot score (scored 2026-10-21T06:14Z for the old head f58b98b8) is older than the score already on main (2026-10-21T09:25Z, commit f521b7ba), so main's file was kept and the bot commit became empty and was dropped by the rebase. The bot's old-head score remains in remote history and PR checks regenerate scores for the new head. This is the only reconciliation decision.
* Local identity: jmservera, 8036360+jmservera@users.noreply.github.com (from gh api user).

## P01 Adapter, tests, report

* Added tools/climate_paired_bounds.py: parsing and validation of Open-Meteo and NASA POWER hourly responses, Magnus humidity consistency (1.0 point), UTC-timestamp-keyed cross-source comparison, percentile rule, report builder, CLI.
* Added tools/test_climate_paired_bounds.py (22 new tests; 33 with the existing climate tests; mutation checks on tolerance, dew-point, hour-step, cross-source and fill-value guards each fail the suite). Covers every rejection path, tolerance boundary, hand-computed derivation and ties, shifted-source and unequal-length rejection, golden regeneration of the report from the committed raw fixtures, and separation of the Durham evidence.
* A test run found a real defect: an invalid retrieved-on value raised an unclear isoformat error. Fixed to the intended message.
* Added raw fixtures docs/reference/research/climate-paired-sample-178/ (SHA-256 96e707ea... and cba9cf30...) and docs/reference/research/climate-paired-bounds-178.json.

## P02 Synthesis, index, log

* New synthesis section, pending-production table, index row and log entry; ms.date of the synthesis set to 2026-10-22. The documented reproduction command regenerates the report byte-identically.

## Divergences and amendments

* None to scope. Critique PC-001..PC-005 applied before implementation. Plan arithmetic in one test was corrected (expected mean difference 1.1).

## Validation so far

* python3 -m unittest discover -s tools -p 'test_climate_*.py': 33 tests OK.
* P03 (full gate, receipt, push) outstanding; recorded in the final stage.

## Follow-up items

* Production source precision, licence and commercial-use confirmation, multi-year window, representativeness.
