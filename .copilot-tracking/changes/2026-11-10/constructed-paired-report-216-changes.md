---
title: Changes - constructed paired observations in the regulatory gate report (Refs #216, #208)
description: Running change record for the constructed paired report integration
ms.date: 2026-11-10
---

## Status

Implementation complete and validated (see below); `implement-done` recorded by the witness after this record.

## Planned changes

* `src/agents/evals/run_regulatory_gates.py`: option, bounded loader, distinct section.
* `src/agents/tests/test_paired_report_command.py`: new command-level tests.
* `src/agents/README.md`: short subsection.

## Changes made

| File | Change |
| --- | --- |
| `src/agents/evals/run_regulatory_gates.py` | Optional `--constructed-paired-observations PATH`, bounded strict loader (`load_constructed_observations`), distinct `constructed_paired_observations` section calling `evaluate_paired_trial(rows, thresholds=None, cost_inputs=None, now=NOW)`. Validation happens before `run` and before `--record`. |
| `src/agents/tests/test_paired_report_command.py` | New, 18 command-level tests through the real script (subprocess), strict typing. |
| `src/agents/README.md` | New subsection "Constructed paired observations in the report (2026-11-10)". |

Unchanged by hash: `paired_trial.py` `85450ae64373dcfb60fb1cdca22ab9e7083d1b72daaa140758687c2e9ddd7736`, `regulatory_gates.py` `722b26f3a99afa2dab272e2129d928d8d66019972afbd1733446ed4e8ebbb35a`, `regulatory_gates_results.json` `8f97a758c61fbc82a149c4644d5ae0072ab1c0fd598ff6c59b2677a0ea973f7c`.

## Red and green

* Red (before any implementation): all 18 new tests fail; the option is rejected with `unrecognized arguments`, exit 2 (23 failures and 5 errors counting subtests).
* Green: `test_paired_report_command` 18 tests OK; with `test_paired_trial test_regulatory_gates test_regulatory_answers test_eval_registry test_gate_agreement test_alert_triage test_dependency_rule`: 77 tests OK.
* Default command output (60000 homes) is byte-identical to the committed report (sha256 `8f97a758...ea973f7c`), before and after.
* Opt-in real run at 60000 homes with the baseline six-row input: exit 0, the report minus the new section equals the committed report; `status` measured, 3 pairs, `cards_only`, cost `Unknown` with 13 named missing inputs. A bad envelope exits 1 with a stderr reason.
* Ruff check, ruff format --check and configured mypy (`src` and `tests`, 48 files) pass from `src/agents`. Supplementary `mypy --strict evals/run_regulatory_gates.py` (file-only, not configured coverage) passes after fixing an implicit re-export of `NOW`.

## Amendments and divergences

* Critique findings 1 to 3 applied (pseudonymous id pattern, regular-file check, qualification wording).
* Additional bound added during implementation, not in the plan: seconds above one year are refused (`MAX_SECONDS`) so huge ints, `1e999` and sum overflow cannot reach the scorer or emit non-finite output. `valid_observation` alone raises `OverflowError` on huge ints.
* `NOW` is imported from `regulatory_fixture` (its defining module) rather than through `regulatory_gate_fixture`, after the supplementary strict check flagged implicit re-export.
* `ruff check --fix` applied to the script for import ordering only.
* A scratch draft briefly created under `/tmp` was removed and never entered the repository.
* Tests were written after `implement-start` and before the implementation.

## Not done

* No mutation-testing run; the test suite was not checked against deliberately broken implementations.
* No blanket or `--changed` RPI gate (owner DEMO targeted tier). No hosted CI observed (nothing pushed).
* No web, browser, SQL, model, human or live validation.
