# Issue 1258 API wiring-test lint diagnostic changes (2026-11-09)

Refs #1258. Diagnostic only. Implement phase executed validation only, after the prospective commit `a7ae689a08a9643f43d9285afc73a6dfcaa47924`. No source, formatter write, `--fix`, suppression, push, PR, board or deployment. `git status --short` was empty before and after the producer.

## Producer

Pinned `ruff 0.17.1` (isolated venv `/tmp/lint1258/venv`; the host global is 0.17.3 and was not used for the result), working directory `src/api`, maintained `pyproject.toml`, files `src/zava_forward/api/server.py`, `tests/test_ranking_publication_wiring.py`, `tests/test_case_journey.py`. Raw logs are retained outside the repository in `/tmp/lint1258/run/` (`SHA256SUMS` there); earlier research probes in `/tmp/lint1258/research/` are unchanged.

| Command | Genuine exit | Log SHA-256 |
| --- | --- | --- |
| `ruff check --output-format=concise <3 files>` | 1 (10 errors) | `5d668e643d75c74e57a404960146260cf07c9917103e7f9e02cee96755e68c61` |
| `ruff format --check --force-exclude <3 files>` | 1 (wiring test would be reformatted) | `4c6c8c5a5c5a40640bcf06e65cc4e6c69292351e1ed7d296ece5456003fb422b` |
| CI form `ruff check .` | 1 (10 errors) | `d06e545a3f0336f9e1abdb16a99b415f9366bd41bfb20b58c063aee5c4b64ad9` |
| CI form `ruff format --check .` | 1 (1 file would be reformatted, 124 already formatted) | `5edf3142a37b628a2da693cf2b19b609338cd44c832264242233a77768b55f2d` |

Every exit file has SHA-256 `4355a46b...dd865` (value `1`).

## Errors (all in `tests/test_ranking_publication_wiring.py`)

| Line | Rule | Detail |
| --- | --- | --- |
| 361 | E501 | 101 > 100 |
| 365 | I001 | import block unsorted or unformatted (auto-fixable, not applied) |
| 369 | E501 | 104 > 100 |
| 375 | E501 | 108 > 100 |
| 383 | E501 | 104 > 100 |
| 398 | E501 | 142 > 100 |
| 419 | E501 | 110 > 100 |
| 448 | E501 | 110 > 100 |
| 468 | E501 | 108 > 100 |
| 482 | E501 | 116 > 100 |

`server.py` and `test_case_journey.py` report no lint error. The formatter also flags the wiring test only. `server.py` appears in an explicit-path format check without `--force-exclude` because explicit paths bypass the configured exclude; CI `.` excludes it.

## CI applicability

Applicable. `.github/workflows/src-ci.yml` job `project`, matrix `api`, runs `ruff check . && ruff format --check .` in `src/api` with Python 3.12 after `pip install -e ../core -e ../agents -e ".[dev]"`, which installs `ruff==0.17.1` per `src/api/pyproject.toml`. The wiring test is not in `per-file-ignores` or `[tool.ruff.format] exclude`, so both CI commands cover it and fail on the identical 10 errors. The workflow triggers on `src/**` paths. Hosted CI itself was not observed.

## Byte-identity and source equivalence

* Wiring test blob `c1b7fa962e0b945655da3a5ffa35701a5adaee38` is identical at C5 `52f9b61bb`, `9b1e2567`, tested head `59d8ad8a` and `HEAD`; main `8d6f029c` has `a109ef26`. `pyproject.toml` blob `9b261f29fdcc99c84aafaad4a4705cfcd08c2355` is identical at all refs. The C5 lint failure is therefore inherited byte for byte.
* `server.py` (`36b9b963...`) and `test_case_journey.py` (`e7e6ad6e...`) differ from C5 (`14c4727c`, `8d1a92ad`) because of the main integration, and are lint-clean.
* Non-tracking manifests (every tracked path except `.copilot-tracking/`, 1358 files) are identical for `9b1e2567`, tested head `59d8ad8a` and `HEAD`: SHA-256 `99f6a7076e177f784c028a4d4b0bab15937ba68b596c35d378e3615beba910d0`. Frozen tree `b88cc90f`, tested tree `f3c6ccc4`.

## Why the earlier invocation matches, not differs

The pinned check does not pass, so there is no differing pass to explain. The sql-main record (10 errors: 9 E501, 1 I001) is reproduced exactly with pinned 0.17.1 and, in a research probe, with the host 0.17.3. The C5 "ruff clean" statement covered only the adapter, core test and fixture, not this API test, so the gap pre-existed.
