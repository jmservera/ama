---
title: Details - constructed paired observations in the regulatory gate report (Refs #216, #208)
description: Phase details for the constructed paired report integration
ms.date: 2026-11-10
---

## Phase 2 Red tests

File `src/agents/tests/test_paired_report_command.py`, strictly typed, `unittest`. A helper runs the real script with `subprocess.run([sys.executable, script, ...])`, `PYTHONPATH` built from the core and agents test directories, `ZF_DATA` pointing at a non-existent temporary path, and returns exit code, stdout, stderr.

* Shared runs (`setUpClass`, `--homes 100`): default run; opt-in run with a prepared three-role favourable input written to a temporary directory, with `--record` to a temporary file.
* Opt-in section: schema, input sha256 equals `hashlib.sha256` of the file bytes, counts, qualification wording; scorer result equals `evaluate_paired_trial(rows, thresholds=None, cost_inputs=None, now=...)` called directly; `pairs` 3, `status` `measured`, `ship_recommendation` `cards_only`, economics `Unknown` with the five named inputs and `price_source.*`, `usage.*`; `threshold.status` `unset_pending_owner_agreement`; supplied `accepted: true` appears only as scorer counts under the constructed qualification.
* No-opt-in equality: default stdout has no new key; opt-in output minus `constructed_paired_observations` equals default output; recorded file equals stdout.
* Rejections before report generation (nonzero, stdout empty, message on stderr): missing file, oversize, malformed JSON, `NaN`, duplicate keys, unknown schema, extra or missing envelope key, non-list observations, too many observations, extra, missing and wrongly typed observation keys, bad role or arm, boolean seconds, negative and infinite seconds (`1e999`), identifier with a space or `@` or over 64 characters, deeply nested array, a directory path (not a regular file).
* Valid edge inputs through the real command: empty list gives `not_evaluated`; partial roles give `not_evaluated` per absent role; unpaired rows are listed under `unpaired`; a chat hazard miss gives `hazard_misses.status` `failed`, critical severity and a reason.
* Isolation: the command run with `socket` connect and `subprocess.Popen` patched to raise (via `runpy`) still succeeds; the temporary `ZF_DATA` path does not exist afterwards.

Expected red: before implementation the option is unrecognised (exit 2), so every opt-in test fails.

## Phase 3 Implementation

In `run_regulatory_gates.py` only:

* Constants `SCHEMA`, `MAX_BYTES`, `MAX_OBSERVATIONS`, `ID_PATTERN`, `OBSERVATION_KEYS` (from `paired_trial` `BOOLS`, `SECONDS`).
* `ID_PATTERN = ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$` replaces the 128-character text bound; the path must be a regular file.
* `load_constructed_observations(path) -> tuple[list[dict[str, Any]], dict[str, Any]]`: bounded read of `MAX_BYTES + 1`, UTF-8 decode, `json.loads` with a `parse_constant` that refuses non-finite constants and an `object_pairs_hook` that refuses duplicate keys, narrow `except` of `OSError`, `ValueError`, `RecursionError`, each re-raised as `SystemExit` with a specific message; then shape, exact-key, count, text-bound and `valid_observation` checks naming the observation index.
* `constructed_section(rows, input_info, now)` calls `evaluate_paired_trial(rows, thresholds=None, cost_inputs=None, now=now)`.
* `main()` loads and validates before `run`, then adds the section only when opted in. `now` is `regulatory_gate_fixture.NOW`.

## Phase 4 Validation commands

From the repository root with the owned venv and `PYTHONPATH="$PWD/src/core/tests:$PWD/src/agents/tests"`:

* `python3 -m unittest test_paired_report_command test_paired_trial test_regulatory_gates test_regulatory_answers test_eval_registry -q` (from `src/agents/tests` paths as in the README)
* default command diff against `src/agents/evals/regulatory_gates_results.json`
* from `src/agents`: `ruff check . && ruff format --check . && mypy`; supplementary file-only mypy of the script, labelled as not configured coverage
* `git diff --stat` and `sha256sum` of `paired_trial.py`, `regulatory_gates.py`, committed results to prove unchanged.

## Phase 5 README

Add a short subsection after "Paired staff trial scoring (2026-11-03)" in `src/agents/README.md` giving the command, envelope, limits, qualifications and the `--record` warning. State that criteria 1, 4 and tokenomics criteria remain unmet.
