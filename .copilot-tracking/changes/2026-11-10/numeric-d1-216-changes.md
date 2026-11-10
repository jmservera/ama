---
title: Changes - numeric boundary D1
description: Implementation record for the two numeric corrections
ms.date: 2026-11-10
---

## Status

Implementation complete. Process note: my first attempt to write this full record failed because the file already existed, so the `implement-done` witness observed this stub; the record below was completed afterwards (the witness will note the changes artifact evolved).

## Files changed

* `src/agents/evals/run_regulatory_gates.py`: seconds values below zero are refused (integer-safe comparison before `valid_observation`), and the scorer result is serialized with `allow_nan=False` inside a narrow `ValueError` handler that refuses with `--constructed-paired-observations: derived values are not finite ...`. The section is now built before `run()`, so refusal precedes report generation and `--record`.
* `src/agents/tests/test_paired_report_command.py`: three command tests (negative `elapsed_seconds` and `review_seconds` including a 401-digit integer; subnormal cards with maximum chat for a paired participant; exact bound 31536000 accepted for both fields and 31536001 refused). Each refusal asserts exit 1, empty stdout, option prefix, no `Traceback` and an untouched sentinel `--record` temporary file.
* `src/agents/README.md`: one refusal clause for the derived-finite case.

## Evidence

* Baseline on `ab365e53`: subnormal input exit 0 with `"elapsed_ratio": Infinity`; huge negative integer exit 1 with an `OverflowError` traceback.
* Red: against the pre-fix script the new tests gave 7 failures (6 negative-seconds subtests, 1 derived-ratio; the exact-bound test passes as a regression guard). Adverse note: a first red run of the derived-ratio test used unpaired participants, so it failed for the wrong reason (the scorer produced no ratio); the test was corrected to a paired participant and the red was re-run against the pre-fix script. Both outputs are kept in the evidence directory.
* Green: command tests 21 OK; `test_paired_trial` 10, `test_regulatory_gates` 18, `test_regulatory_answers` 7, `test_eval_registry` 8, `test_gate_agreement` 7, `test_alert_triage` 7, `test_dependency_rule` 4, all OK. An initial combined `python -m unittest` invocation could not import `regulatory_gate_fixture` (path set-up, not a defect) and one run then failed on the corrected-away unpaired test; files were rerun with `discover -s tests -p`.
* Configured `ruff check`, `ruff format --check` and `mypy` (48 files, `src` and `tests` only) pass. Supplementary `mypy --strict evals/run_regulatory_gates.py` passes and is not configured coverage.
* Default 60000-home output sha256 `8f97a758c61fbc82a149c4644d5ae0072ab1c0fd598ff6c59b2677a0ea973f7c`, equal to the committed results; `paired_trial.py` has no diff; no tracked result written. Re-running both reproductions now exits 1 with empty stdout and the option-prefixed reasons.

## Not run

Full agents suite, hosted CI, browser, SQL, model, human and live checks.
