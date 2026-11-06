# Issue 86 formal-complaints typing correction: changes

Scope: jmservera/ama#86 only (`Refs #86`). Plan `.copilot-tracking/plans/2026-11-06/issue-86-formal-complaints-typing-plan.md`; critique `.copilot-tracking/challenges/2026-11-06/issue-86-formal-complaints-typing-critique.md`. Base `b69afe33267022356da626998d04c42922416cf6` (preserved as local branch `issue86-pre-typing-b69afe3`); prospective records committed as `7cc0d461f` before any source edit.

## Error to correction map

| R2 error (14) | Correction |
| --- | --- |
| `complaints_route.py:30,34,41,56` no-untyped-def | Annotated `UnconfiguredReceiver.submit -> NoReturn`, `receiver_from_env(Mapping[str, str]) -> ComplaintsReceiver`, `build_envelope(str, Mapping[str, Any], str, int) -> dict[str, Any]`, `parse_acknowledgement(Any) -> dict[str, Any]`; added `ComplaintsReceiver` Protocol (`submit(dict[str, Any]) -> object`). |
| `test_resident_decisions.py:3237,3242` no-any-return | `route()` and `request_without_route()` bind the untyped Store value to a locally annotated `dict[str, Any]` before returning. |
| `test_resident_decisions.py:3262,3271,3297,3312,3333,3347,3357,3380` attr-defined | `Store` declares `complaints_receiver: ComplaintsReceiver | None` under `TYPE_CHECKING` only (annotation, no runtime attribute), import also under `TYPE_CHECKING`. |

Formatting: `ruff format` was applied to the two files I touched after the first Ruff run reported E501 and format drift on my own new lines (adverse intermediate result, kept in `/mnt/ama-gates/restart-1106-86-typing/ruff-check.txt` and `ruff-format.txt`).

Deviations from the first plan, from the critique: `parse_acknowledgement` takes `Any` (not `object`, which fails strict mypy), and the Store declaration is annotation-only (a `= None` default would change `hasattr`/`getattr` semantics). No `type: ignore`, `cast`, config change, runtime logic, default, persistence, authorization or web change.

## Results (from `src/core`, R2 core venv tools read-only, scratch `/mnt/ama-gates/restart-1106-86-typing/`)

| Command | Result |
| --- | --- |
| `python -m mypy` before change | exit 1, 14 errors in 267 files (`red.txt`), identical to R2 log |
| `python -m mypy` after | exit 0, no issues in 267 files |
| `python -m ruff check .` first run | exit 1, 2 E501 on new lines (fixed by formatting those two files); after: exit 0 |
| `python -m ruff format --check .` first run | exit 1, 2 files; after: exit 0, 214 formatted |
| `PYTHONPATH=src:tests python -m unittest test_resident_decisions` | exit 0, 281 run, OK, 101 skipped (SQL-backed cases; no SQL service started) |
| `git diff --check` | exit 0 |

Import origin proof: `zava_forward.core.store` and `complaints_route` load from this worktree's `src/core/src`. `PYTHONDONTWRITEBYTECODE=1`; mypy and Ruff caches and TMPDIR in scratch.

## Not run

No full core suite, API suite, SQL Server, browser, image build, scanner or FULL gate. Old R2 receipt is a failed receipt and is not passing, covered or verified. R3 FULL, independent exact-head assessment, hosted CI and human gates are pending.
