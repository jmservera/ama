<!-- markdownlint-disable-file -->

# Phase Details: climate-paired-alt-source-178

Task context: retrieved modelled paired sample, validating adapter, labelled report. Evidence: research W1-W7, C1-C2.

## P01 Adapter, tests, report

* Test ownership: one new test file tools/test_climate_paired_bounds.py, no removals, one semantic test class plus one golden class. Targets: canonical report JSON only.
* T01: functions `parse_open_meteo`, `parse_power`, `validate_pair`, `derive`, `compare`, CLI. Magnus: es = exp(17.625 T / (243.04 + T)); RH = 100 es(Td)/es(T); tolerance 1.0 RH point (fixture maximum residual 0.852; stated in the report).
* T02 tests: constructed inputs for hash mismatch, null temperature, null RH, short RH series, duplicate or skipped hour, wrong unit, RH 101, dew point above temperature, RH inconsistent with T and dew point, POWER fill -999, non-HTTPS. Derivation test on a small hand-computed series (known min, max, percentile, paired RH). Golden test on committed fixtures.
* T03: command recorded in the synthesis so the report is reproducible.

## P02 Synthesis, index, log

* New section "Alternative modelled paired climate source (2026-10-22, Refs #178)" in docs/reference/research/iot-sensor-analytics-research-plan.md after the 2026-10-21 section; index row in docs/reference/README.md next to the existing #178 rows; append log entry; do not edit earlier entries.

## P03 Gate and publication

* Install src packages if the gate needs them; run tools tests, `python3 tools/rpi-checks.py --all --base <origin/main sha> --out <external dir>`, then `--verify-receipt`; push with `--force-with-lease` after the rebase. Receipts and logs stay external and are reported.
