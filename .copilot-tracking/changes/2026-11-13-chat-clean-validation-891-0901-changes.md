# Changes: chat-clean-validation-891-0901 (2026-11-13)

No source, test, helper, fixture, policy or workflow file changed. Only tracking evidence was added.

## Commands actually run (from the worktree; `src/api` for the test)

* `git show 8c735ae...` research/review/plan (read-only), `git diff --name-only 8c735ae HEAD -- <src and tests>`.
* `python3 -m venv /tmp/v891-0901` then `/tmp/v891-0901/bin/pip install -q --no-deps ./src/core ./src/agents ./src/api`: exit 0 (three 0.1.0 distributions listed).
* `env -u ZF_DATA PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests timeout 400 /tmp/v891-0901/bin/python -m unittest test_ai_consumption_api -v` from `src/api`: real exit status 1.
* Origin probe from `/tmp` with the venv interpreter: `zava_forward.core.ai`, `agents.chat`, `api.server`, `agents.ai_eval` all resolve to `/tmp/v891-0901/lib/python3.12/site-packages/zava_forward/...` (a separate probe; it proves those modules' origin in that probe, not every import in the run).

## Result (full output: [run891.out](../validation/chat-clean-validation-891-0901/run891.out), status: [run891.exit](../validation/chat-clean-validation-891-0901/run891.exit), sha256 `fafc2035fe9272b38c98bb0e3934e786f2ab3a301fe9dd6d49a44b9da7d5d0a6`)

* `Ran 37 tests in 71.309s`, `FAILED (errors=1)`: 36 `ok`, 1 ERROR.
* Failing test: `ConsumptionApi.test_manager_report_local_http_and_bad_period` (test file L1673): `GET /api/ai/report` returned 500, `FileNotFoundError` at `agents/ai_eval.py:615 run_eval`.
* Likely cause (from reading source only, not verified by a second run): `ai_eval.GOLDEN` defaults to `Path(__file__).resolve().parents[3] / "evals" / "ai_priority_golden.json"`. In a non-editable install `__file__` is under site-packages, so the repo fixture under `src/agents/evals/` is absent. The README installs editable (`pip install --no-deps -e`), which keeps `parents[3]` at `src/agents`. The install form is a plausible but UNCONFIRMED cause: the missing path and `ZF_AI_GOLDEN` state were not inspected in the run. Not proven to be an environment fault or a source defect.
* Evidence boundary: the 36 passes are local installed-code unit results only (not proof that every import in the run came from the owned venv, and not model, privacy, live or per-call acceptance). The errored report test failed before its assertions. Criterion 2 remains unmet.
* Not exit 0, so this is not a passing exact-source witness. The 36 passing tests are recorded as 36 passing in this run, nothing more.

## Deviations

* Order: the plan critique ran after the single run was already executed (time bound), so it is retrospective, not prospective. Recorded honestly in the critique file.
* One attempt only, per the bound; no rerun with `-e`.

## Resume point

From `src/api`: `python -m venv <owned>; <owned>/bin/pip install --no-deps -e ../core -e ../agents -e .` (README editable form), then the same unittest command with the same helper-only `PYTHONPATH`; compare against this record. Alternatively set `ZF_AI_GOLDEN` to the repo's `src/agents/evals/ai_priority_golden.json` (a data pointer, not a source path), with the owner's approval of that variant.
