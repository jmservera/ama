---
title: Plan - constructed paired observations in the regulatory gate report (Refs #216, #208)
description: One initial integration of the existing paired-trial scorer into the maintained gate report command
ms.date: 2026-11-10
---

## Goal

Let an operator pass one bounded, versioned, caller-declared constructed paired-observation JSON file to `src/agents/evals/run_regulatory_gates.py` and read the existing `evaluate_paired_trial` result as a distinct, qualified report section. Default invocation and output stay byte-identical.

## Scope

* In: the report script, one command-level test module addition, a short README addition, RPI evidence.
* Out: `paired_trial.py`, `regulatory_gates.py`, fixtures, golden and held-out data, committed results, `src/api`, `src/core`, `infra`, workflows, any new scorer, checker, service or framework.
* Non-goals: thresholds, prices, budget, authority, approval inputs, model or network calls, ZF_DATA reads, source auto-discovery, human-trial claims.

## Contract

* Option `--constructed-paired-observations PATH`. Envelope `{"schema": "constructed-paired-observations-v1", "observations": [..]}`, exactly those two keys.
* Limits: regular file of at most 262144 bytes, at most 1000 observations, participant and task matching `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$` (critique amendments 1 and 2).
* Each observation has exactly the nine existing fields. Field constraints come from the existing `paired_trial.valid_observation` plus the exact key set and text bound. Duplicate JSON keys, `NaN`, `Infinity`, trailing data, non-UTF-8, wrong shapes and any invalid row are refused before the report is generated, with `SystemExit("message")` (stderr, exit 1). Argparse misuse keeps exit 2.
* Unpaired, partial-role, empty and critical-hazard inputs are valid constructed data and are reported by the existing scorer.
* New section `constructed_paired_observations` (only when opted in): `schema`, `input` (`sha256`, `bytes`, `observations`), `qualification` (caller-declared constructed data; independent human participation, synthetic origin and `accepted` flags all unverified, not a staff trial, not human acceptance, not owner-agreed, not merged with other datasets), `result` (scorer output, `thresholds=None`, `cost_inputs=None`, `now` = report `as_of`).
* No other report key changes. `--record` semantics unchanged.

## Phases

* [x] Phase 1 Research and baseline (done before this plan).
* [x] Phase 2 Red tests: add command-level cases to `src/agents/tests/test_paired_report_command.py`, run, record the expected failures.
* [x] Phase 3 Implement the option, bounded loader and section in the report script only.
* [x] Phase 4 Green: new and existing paired and regulatory gate tests, committed-report equality, ruff check, ruff format --check, configured mypy.
* [x] Phase 5 README addition and change record.
* [ ] Phase 6 Single Review of the final candidate.

## Validation (owner DEMO targeted tier)

Targeted tests and actual command runs only; no blanket `rpi-checks.py` or `--changed` run. Hosted CI for the exact head is read by the coordinator after publication and is not claimed here.

## Risks

* Constructed `accepted: true` read as human acceptance: mitigated by qualification text and a test.
* `--record` over the canonical file: documented, tests use temporary destinations.
* Command subprocess tests are slow (about 7 s per report): share two report runs through `setUpClass`; rejection cases fail before generation.
