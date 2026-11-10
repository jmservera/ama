<!-- markdownlint-disable-file -->
# Changes: pinned-tool validation of recovered #123, 2026-11-09

Plan: [plan](../../plans/2026-11-09/pinned-validation-123-plan.md). No source, manifest or pin change. Phases 1 to 3 done.

## Evidence (frozen HEAD `6023741cb42d62f71d47e1780b6ccb765d596fd6`, origin/main `b46a9ad9a9619db535368d1b2cbbddec8110e122`)

* Pins confirmed in `src/core/pyproject.toml` dev extra: `ruff==0.17.1`, `mypy==2.4.0` (CI also `ruff==0.17.1`).
* Isolated venv `~/.venvs/zf123-pinned` (outside repo), Python 3.12.3. `pip install ruff==0.17.1 mypy==2.4.0` only (tools were missing). Frozen: ruff 0.17.1, mypy 2.4.0 (compiled), ast_serialize 0.13.1, librt 0.16.0, mypy_extensions 1.2.0, pathspec 1.1.1, typing_extensions 4.16.0.
* From `src/core`: `ruff check .` exit 0 (all checks passed); `ruff format --check .` exit 0 (216 files already formatted; handoff's 215 differed in count, no format finding); `mypy` exit 0 (no issues, 269 source files).
* `PYTHONPATH=src:tests python -m unittest test_paired_equity test_cohort_eval test_household_conditions test_retrofit_effects test_monitoring_coverage test_rule_engine test_chat_privacy -q`: Ran 146 tests in 31.382s, OK, 0 skips, exit 0. `zava_forward.core.paired_equity` imported from `src/core/src/zava_forward/core/paired_equity.py` in this worktree (current source).
* `git diff --check` exit 0. No core diagnostic change was needed; `fairness_evidence=False` and `activation_allowed=False` untouched.
* Not run: SQL, API, browser, hosted CI, `rpi-checks --all`.

## Preserved mismatch outcome

The earlier ruff 0.17.3 / mypy 2.4.1 results in the recovery changes and review records stay as recorded: they were produced under non-pinned versions. This pinned rerun is the version-conformant evidence and agrees with them.
