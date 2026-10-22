<!-- markdownlint-disable-file -->

# Changes: climate-paired-alt-source-178-corr1

| Field | Value |
|---|---|
| Date | 2026-10-22 |
| Plan | .copilot-tracking/plans/2026-10-22/climate-paired-alt-source-178-corr1-plan.md |
| Corrected head parent | d314d7c6945a51909517394725577ccd19d5d1ac (base 9e55a392b95c90730c6410b9a4db4ad3a5ae70ce) |

* tools/climate_paired_bounds.py: monthly minimum and maximum now carry value, every tied UTC timestamp (chronological) and the paired value of the other variable.
* tools/test_climate_paired_bounds.py: replaced the bare-value monthly assertion; added split-month tie test and monthly versus annual reconciliation test (24 tests pass).
* docs/reference/research/climate-paired-bounds-178.json: regenerated from the same retained raw fixtures; only the monthly blocks changed shape; all other fields identical.
* Synthesis paragraph and log entry added. Earlier history, the first receipt (/tmp/ama-alt-source-1430-178, sha256 a19ee1a7...) and the original review record are preserved and now historical for head d314d7c6.
* P03 outstanding at time of writing

## Correction 2 (RV-001), scope persisted before source edits

* Input: independent functional-review RV-001 (malformed nested containers raised AttributeError). Scope and validation intent are in the plan and phase details (P04, P05). Results follow below.

* tools/climate_paired_bounds.py: added _object(); hourly_units, header, parameters, parameters.T2M, parameters.RH2M, properties, properties.parameter and geometry must be JSON objects, and geometry.coordinates a list of at least three values, else ValueError (previously AttributeError or similar).
* tools/test_climate_paired_bounds.py: three new tests (Open-Meteo hourly_units; POWER containers x array, list, string, number and null; malformed coordinates).
* Validation: test_climate_paired_bounds and test_climate_paired_blocker pass (30 tests); the committed-fixture golden test passes unchanged, so the report and fixtures are not touched. Mutation check: disabling the _object raise made 40 subtests error; helper restored and tests re-run green.
* P04 complete. P05 (full gate on current base, receipt verification, independent review, publication) is coordinator-owned and not run; no push, no GitHub change. The earlier receipt (head 1c4f374a) does not cover this commit. No issue acceptance claimed; licence/reuse, production precision and AC066-068 remain unmet.: gate result and receipt are recorded in the PR description and final report, kept external.
