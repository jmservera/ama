# Issue 1258 API wiring-test lint diagnostic research (2026-11-09)

Refs #1258. DIAGNOSTIC ONLY. Task `1258-ranking-archive-blob-lint-diagnostic`, parent `1258-ranking-archive-blob-sql-main`. Cycles c1 to c5 are spent, zero remain. No source correction, formatter write, policy-name fix, extra cycle, push, PR, board or deployment is authorized. Earlier records and their outcomes are history and are not edited.

## Research disposition

Executed (read-only). Planning Readiness: Ready. Branch `fix/ranking-archive-ancestor-durability`, target `main`, frozen `9b1e2567c2d0a2173b562103cd27508f75181526` (tree `b88cc90f4a4dd48a51b15e526b734e975fa036c5`), tested head `59d8ad8acc872be604f30dcbee1a44418aae74c8` (tree `f3c6ccc450e156461e6c1d76da1f8631870879c6`), source C5 `52f9b61bb`, main `8d6f029ca`.

## Question

The sql-main integration changes record reports 10 Ruff errors in `src/api/tests/test_ranking_publication_wiring.py`, inherited from C5. Do they apply to the maintained CI, and does the pinned Ruff reproduce them?

## Evidence (read from the repository)

* Workflow `.github/workflows/src-ci.yml`, job `project`, matrix project `api`: working directory `src/api`; Python 3.12; install `pip install -e ../core -e ../agents -e ".[dev]"`; step `Lint` runs `ruff check . && ruff format --check .`. The job triggers on `src/**` paths, so the wiring test file is in scope.
* `src/api/pyproject.toml`: `dev = ["ruff==0.17.1", ...]`; `[tool.ruff]` line-length 100, target py312, `select = ["E","F","I","B","UP"]`. The per-file-ignores and format-exclude lists name `server.py`, `auth.py`, `timecapture.py`, `checks/*.py` and a list of tests. They do not name `test_ranking_publication_wiring.py` or `test_case_journey.py`, so `server.py` is exempt from format only through the exclude list and the wiring test is fully linted and format-checked.
* Package origin: `src/api` is the `zava-forward-api` distribution (setuptools, `requires-python >=3.12`). The wiring test was added by C5 commit `52f9b61bb` lineage (blob `c1b7fa96`); main `8d6f029ca` has blob `a109ef26`, so main's version differs from the branch's.
* Host tool: global `ruff` is 0.17.3 at `~/.local/bin/ruff`, not the pinned 0.17.1. `python3` is 3.12.3. The demonstrator's `demo-rpi-common.md` is referenced by earlier state files but no such file exists in this working tree; this is recorded as unavailable.
* Blob identity: wiring test blob `c1b7fa96` is identical at `HEAD`, `9b1e2567` and `52f9b61bb` (C5). `pyproject.toml` blob `9b261f29` is identical at all four refs.

## Preliminary probes (before the plan commit)

Ruff 0.17.1 was installed into an isolated venv at `/tmp/lint1258/venv` (no global change) and run read-only from `src/api` on the three files: `server.py`, `test_ranking_publication_wiring.py`, `test_case_journey.py`. The probe logs are retained outside the repository in `/tmp/lint1258/research/` and are not the diagnostic producer: `ruff check` exit 1, 10 errors (9 E501, 1 I001), all in the wiring test; `ruff format --check` on the explicit files also reports `server.py` because explicit paths bypass the format exclude unless `--force-exclude` is used. The corroborating `ruff check .` exit 1 (10 errors) and `ruff format --check .` exit 1 (one file, the wiring test) match the CI step.

## Gaps and risks

* The producer in Implement must be re-run after the plan commit so the evidence follows the committed plan.
* `--force-exclude` is needed so the explicit-file run honours the CI format exclude. This is the configured behaviour of the CI `.` invocation, not a lighter rule set.
