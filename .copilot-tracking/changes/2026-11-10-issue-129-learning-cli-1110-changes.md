<!-- markdownlint-disable-file -->
# Changes: issue 129 constructed learning-report CLI

* Related plan: `.copilot-tracking/plans/2026-11-10-issue-129-learning-cli-1110-plan.md`; details and critique alongside.
* Status: implementation complete (witness `implement-done`); Review follows once.

## Baseline (before any source edit)

* `python -m zava_forward.core.learning_test_bundles in.json`, the same via stdin, and `--help`: each exit 0 with no output (external copy `phase129-learning-cli-evidence-1110/baseline.txt`, input `in.json`). Existing module tests: 12 pass.
* Source blobs before: module `2c5483ccd20961ceb98264a3d86ec0409e3fa2f1`, tests `316834519216dd0da86195419918eb3516299b9a`, README `1cc9a1c7a09fbca16b58650ab6ce23d10aa23a14`.
* Environment: own venv `~/.venvs/issue129-learning-cli-1110` (Python 3.12.3, editable `src/core[dev]`, ruff 0.17.1, mypy 2.4.0 per `src/core/pyproject.toml` pins); no global install.

## Changes

* `src/core/src/zava_forward/core/learning_test_bundles.py` (blob `d1915d8dfb53ae287a51f3c2bf44c72188bc46ed`): additive only. Docstring command paragraph; imports `argparse`, `json`, `sys`; constants `SCHEMA_VERSION`, `MAX_INPUT_BYTES`, `MAX_CASES`, `MAX_ID`, `MAX_MINUTES`, `MAX_COUNT`, `QUALIFICATIONS`, `O16_QUALIFICATION`; `_unique_pairs`, `_reject_constant`, `_exact`, `_identifier`, `_validate_input`, `main` and the `__main__` guard. `BUNDLES`, `compare_bundle`, `run_report`, `reconcile_o16`, `render_report` and all existing lines are unchanged (diff has no removed lines). Bundle, retention-false and O16 rules are still enforced by `run_report`.
* `src/core/tests/test_learning_test_bundles.py` (blob `a6f73890b533cf7cb03caddf38c7cc5bf5607355`): 8 new tests in `ConstructedReportCommand` that run the real module as a subprocess in an empty temp directory with `ZF_DATA` pointed at a non-existent path and assert no files appear. They cover all five bundles through the real scorer/renderer, stop-before-effort, comparator-lower, O16 and constructed/unverified labels, 40 refusal shapes (empty, malformed, UTF-8, NaN, overflow float, duplicate key, deep nesting, oversize, schema, unknown keys, booleans, strings, negative, over-limit, float or foreign counts, free-text case, retention true/missing/zero, O16 missing/bad/misplaced), bounded refusal echo, boundary maxima and `-h` without side effects.
* `src/core/README.md` (blob `7b7396091a48696a617c80deda9bbc376abb41fe`): new "Constructed learning-test report command (#129, Refs #123)" section with command, limits and qualifications. No knowledge-base index, log or protocol edit.

## Validation (owner demo targeted tier; external logs in `phase129-learning-cli-evidence-1110/`)

* Red: with the tests added before the CLI, the new class failed (`FAILED (failures=9, errors=3)` on the first run, which included two test-authoring faults later fixed: wrong expected medians and an overflow-float fixture that did not replace anything; those were corrected before implementation was judged green). Green after: 20 tests OK (12 existing unchanged plus 8 new), exit 0.
* Core configured `ruff check .`: all checks passed (exit 0); `ruff format --check .`: 235 files formatted (exit 0); configured `mypy` (strict, 288 files): no issues (exit 0). A first mypy run reported 12 `no-untyped-call` errors from an untyped lambda in the new test; fixed with typed helpers and re-run clean. Versions: ruff 0.17.1, mypy 2.4.0, Python 3.12.3 (project pins), own venv.
* Skipped, deliberately, per the owner tier: blanket full gate, `--changed`, SQL, browser, hosted CI and live trial. Hosted CI for the exact head has not been observed.
* Adverse/process notes preserved: the first test-file insert was applied with a Python rewrite instead of the edit tool (content identical to an edit); the red first run had authoring faults listed above; no unrelated Core test was run, so the known random-signature oracle in 1373 was not encountered.
* After (external `after.txt`): the same envelope now prints the constructed/unverified report, exit 0; invalid input exits 1 with one stderr line.

## Divergences and amendments

* Output is two `print` blocks (report then qualifications) rather than one; no semantic change. `-h` prints the module docstring (command, schema, limits).
